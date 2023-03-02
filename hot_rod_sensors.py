from sunfounder.pin import Pin
from sunfounder.modules import (Ultrasonic)

class UltrasonicSensor(Ultrasonic):
    # Pin locations
    TRING = 'D2'
    ECHO = 'D3'
    def __init__(self):
        super().__init__(Pin(self.TRING), Pin(self.ECHO))

    def read(self):
        raw = []
        reading_count = 3
        for _ in range(reading_count):
            raw.append(super().read())
        corrected = sum(raw)/reading_count
        return corrected
