from datetime import datetime

class SensorModel:
    def __init__(self, date, humidity, temperature, co2, co, pm25):
        self.date = date
        self.humidity = humidity
        self.temperature = temperature
        self.co2 = co2
        self.co = co
        self.pm25 = pm25
        
    def to_dict(self):
        date = datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S')
        return {
            'date': date,
            'humidity': self.humidity,
            'temperature': self.temperature,
            'co2': self.co2,
            'co': self.co,
            'pm25': self.pm25,
        }

