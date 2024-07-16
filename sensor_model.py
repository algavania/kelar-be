from firebase_admin import firestore
from datetime import datetime

class SensorModel:
    def __init__(self, value, date, type):
        self.value = value
        self.date = date
        self.type = type
        
    def to_dict(self):
        date = datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S')
        return {
            'value': self.value,
            'date': date,
            'type': self.type
        }

