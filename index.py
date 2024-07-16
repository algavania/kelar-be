from flask import Flask, jsonify, request
from sensor_model import SensorModel
from firebase_admin import credentials, firestore, initialize_app

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
def routeSensors():
        value = request.json.get('value')
        date = request.json.get('date')
        humidity = request.json.get('humidity')
        temperature = request.json.get('temperature')
        co2 = request.json.get('co2')
        co = request.json.get('co')
        pm25 = request.json.get('pm25')
        data = SensorModel(value, date, humidity, temperature, co2, co, pm25)
        sensor_refs.add(data.to_dict())
        return sendResponse("success", data)

def sendResponse(status, data):
    if isinstance(data, list):
        data = [item.to_dict() for item in data]
    else:
        data = data.to_dict()
    return jsonify({
        "status": status,
        "data": data
    })
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)