import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pickle
import warnings
warnings.filterwarnings("ignore")

def categorize_time_of_day(hour):
    if 3 <= hour < 12:
        return 'Pagi'
    elif 12 <= hour < 15:
        return 'Siang'
    elif 15 <= hour < 18:
        return 'Sore'
    else:
        return 'Malam'

def sarima_forecast(data, order, seasonal_order, steps, min_value):
    model = SARIMAX(data, order=order, seasonal_order=seasonal_order)
    model_fit = model.fit(disp=False)
    forecast = model_fit.get_forecast(steps=steps)
    forecast_mean = forecast.predicted_mean
    forecast_mean = np.maximum(forecast_mean, min_value)
    return model_fit, forecast_mean

def calculate_aqi(concentration, breakpoints):
    for (ConcLow, ConcHigh, IndexLow, IndexHigh) in breakpoints:
        if ConcLow <= concentration <= ConcHigh:
            return ((IndexHigh - IndexLow) / (ConcHigh - ConcLow)) * (concentration - ConcLow) + IndexLow
    return None

def categorize_air_quality(row):
    pm25 = row['PM2.5 Density (ug/m3)']
    co = row['CO (ppm)']
    co2 = row['CO2 (ppm)']

    pm25_breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500)
    ]

    co_breakpoints = [
        (0.0, 4.4, 0, 50),
        (4.5, 9.4, 51, 100),
        (9.5, 12.4, 101, 150),
        (12.5, 15.4, 151, 200),
        (15.5, 30.4, 201, 300),
        (30.5, 40.4, 301, 400),
        (40.5, 50.4, 401, 500)
    ]

    co2_breakpoints = [
        (0.0, 1000, 0, 50),
        (1001, 2000, 51, 100),
        (2001, 3000, 101, 150),
        (3001, 4000, 151, 200),
        (4001, 5000, 201, 300),
        (5001, 6000, 301, 400),
        (6001, 10000, 401, 500)
    ]

    pm25_aqi = calculate_aqi(pm25, pm25_breakpoints)
    co_aqi = calculate_aqi(co, co_breakpoints)
    co2_aqi = calculate_aqi(co2, co2_breakpoints)

    aqi_values = [value for value in [pm25_aqi, co_aqi, co2_aqi] if value is not None]
    if not aqi_values:
        return 'Tidak Tersedia'

    overall_aqi = max(aqi_values)

    if overall_aqi <= 100:
        return 'Baik'
    elif 101 <= overall_aqi <= 200:
        return 'Sedang'
    else:
        return 'Buruk'

def give_advice(row):
    pm25 = row['PM2.5 Density (ug/m3)']
    co = row['CO (ppm)']
    co2 = row['CO2 (ppm)']
    air_quality = row['Air Quality']

    advice = []

    if air_quality == 'Baik':
        advice.append("Kualitas udara baik, Anda dapat melanjutkan aktivitas harian tanpa kekhawatiran.")
    elif air_quality == 'Sedang':
        advice.append("Kualitas udara sedang, disarankan untuk membatasi aktivitas luar ruangan bagi individu sensitif.")
    else:
        advice.append("Kualitas udara buruk, hindari aktivitas luar ruangan yang berat dan gunakan masker.")

    if pm25 <= 12.0:
        advice.append("PM2.5 dalam kategori baik, tetap lanjutkan aktivitas harian Anda.")
    elif 12.1 <= pm25 <= 35.4:
        advice.append("PM2.5 dalam kategori sedang, disarankan untuk membatasi aktivitas luar ruangan bagi individu sensitif.")
    else:
        advice.append("PM2.5 dalam kategori buruk, hindari aktivitas luar ruangan yang berat dan gunakan masker.")

    if co <= 4.4:
        advice.append("CO dalam kategori baik, tetap lanjutkan aktivitas harian Anda.")
    elif 4.5 <= co <= 9.4:
        advice.append("CO dalam kategori sedang, disarankan untuk memastikan ventilasi yang baik di dalam ruangan.")
    else:
        advice.append("CO dalam kategori buruk, hindari area dengan polusi kendaraan dan pastikan ventilasi yang baik.")

    if co2 <= 1000:
        advice.append("CO2 dalam kategori baik, tetap lanjutkan aktivitas harian Anda.")
    elif 1001 <= co2 <= 2000:
        advice.append("CO2 dalam kategori sedang, disarankan untuk memastikan sirkulasi udara yang baik di dalam ruangan.")
    else:
        advice.append("CO2 dalam kategori buruk, pastikan sirkulasi udara yang baik dan batasi aktivitas di dalam ruangan tertutup.")

    return advice

def print_predictions():
    time_mapping = {
        'Pagi': 'Pada Pagi Hari',
        'Siang': 'Pada Siang Hari',
        'Sore': 'Pada Sore Hari',
        'Malam': 'Pada Malam Hari'
    }

    result = ""

    for index, row in predictions.iterrows():
        result += f"Prediksi Kualitas Udara {time_mapping[row['Time of Day']]}: {row['Air Quality']}\n"
        result += f"PM2.5: {row['PM2.5 Density (ug/m3)']:.2f}, CO: {row['CO (ppm)']:.2f}, CO2: {row['CO2 (ppm)']:.2f}\n"
        result += "Saran:\n"
        for advice in row['Advice']:
            result += f"- {advice}\n"
        result += "\n"

    return result


with open('air_quality_model.pkl', 'rb') as file:
    data = pickle.load(file)

models = data['models']

path = 'https://docs.google.com/spreadsheets/d/11Tp3mY7JkAnLTMw4JIXu5cmaMpIOx7xcjgHwt6xPT80/export?format=csv'
df = pd.read_csv(path)

print(df.columns)

numerical_columns = ['Humidity (%)', 'Temperature (°C)', 'CO2 (ppm)', 'CO (ppm)', 'PM2.5 Density (ug/m3)']
for col in numerical_columns:
    df[col] = df[col].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

df['Date and Time'] = pd.to_datetime(df['Date and Time'])
df['Time of Day'] = df['Date and Time'].dt.hour.apply(categorize_time_of_day)
df['Date'] = df['Date and Time'].dt.date
grouped = df.groupby(['Date', 'Time of Day']).mean().reset_index()

features = ['Humidity (%)', 'Temperature (°C)', 'CO2 (ppm)', 'CO (ppm)', 'PM2.5 Density (ug/m3)']
min_values = grouped[features].min()

predictions = pd.DataFrame()

for feature in features:
    feature_data = grouped.set_index('Date')[feature]
    min_value = min_values[feature]
    model_fit, forecast_mean = sarima_forecast(feature_data, (1, 1, 1), (1, 1, 1, 4), steps=4, min_value=min_value)
    predictions[feature] = forecast_mean

future_dates = pd.date_range(start=grouped['Date'].max() + pd.Timedelta(days=1), periods=4, freq='D')
future_time_of_day = ['Pagi', 'Siang', 'Sore', 'Malam']
predictions['Date'] = future_dates.repeat(4)[:len(predictions)]
predictions['Time of Day'] = future_time_of_day * (len(predictions) // 4)

predictions['Air Quality'] = predictions.apply(categorize_air_quality, axis=1)
predictions['Advice'] = predictions.apply(give_advice, axis=1)

predictions_to_print = predictions.drop(columns=['Advice'])

print("Data Prediksi Masa Depan:")
print(predictions_to_print)

print(print_predictions())