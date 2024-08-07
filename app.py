from flask import Flask, jsonify, request
from sensor_model import SensorModel
from firebase_admin import credentials, firestore, initialize_app
import air_quality
import forecasting
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Firebase Initialization
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
sensor_refs = db.collection('sensors')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/sensors", methods=['POST'])
def route_sensors():
        date = request.json.get('date')
        humidity = request.json.get('humidity')
        temperature = request.json.get('temperature')
        co2 = request.json.get('co2')
        co = request.json.get('co')
        pm25 = request.json.get('pm25')
        data = SensorModel(date, humidity, temperature, co2, co, pm25)
        sensor_refs.add(data.to_dict())
        return send_response("success", data)
    


@app.route("/api/predict", methods=['POST'])
def predict():
    date = request.json.get('date')
    humidity = request.json.get('humidity')
    temperature = request.json.get('temperature')
    co2 = request.json.get('co2')
    co = request.json.get('co')
    pm25 = request.json.get('pm25')

    data = SensorModel(date, humidity, temperature, co2, co, pm25)

    quality, advice = air_quality.process_latest_data(data)

    return jsonify({
        "status": "success",
        "data": {
            "quality": quality,
            "advice": advice
        }
    })
    
@app.route("/api/forecast", methods=['GET'])
def forecast():

    advice = forecasting.print_predictions()

    return jsonify({
        "status": "success",
        "data": advice,
    })
    
def send_response(status, data):
    if isinstance(data, list):
        data = [item.to_dict() for item in data]
    else:
        data = data.to_dict()
    return jsonify({
        "status": status,
        "data": data
    })
    
if __name__ == "__main__":
    port = int(os.getenv("PORT", 4000))
    app.run(host='0.0.0.0', port=port)