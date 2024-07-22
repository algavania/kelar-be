import joblib

def calculate_aqi(concentration, breakpoints):
    for (ConcLow, ConcHigh, IndexLow, IndexHigh) in breakpoints:
        if ConcLow <= concentration <= ConcHigh:
            return ((IndexHigh - IndexLow) / (ConcHigh - ConcLow)) * (concentration - ConcLow) + IndexLow
    return None

def categorize_air_quality(sensor_data):
    pm25 = sensor_data.pm25
    co = sensor_data.co
    co2 = sensor_data.co2

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

def give_advice(sensor_data):
    pm25 = sensor_data.pm25
    co = sensor_data.co
    co2 = sensor_data.co2

    advice = []

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

def process_latest_data(sensor_data):
    air_quality = categorize_air_quality(sensor_data)

    advice = give_advice(sensor_data)

    print(f"Kualitas udara sekarang: {air_quality}")
    print(f"PM2.5: {sensor_data.pm25}, CO: {sensor_data.co}, CO2: {sensor_data.co2}")
    if advice:
        print("Saran:")
        for a in advice:
            print(f"- {a}")
    else:
        print("Tidak ada saran khusus.")

    return air_quality, advice
