# Motor Specs.
# ----------------------------------------
# DC3V-6V Geared Motor
# ----------------------------------------
from sunfounder.pwm import PWM
from sunfounder.pin import Pin
from sunfounder.servo import Servo

from hot_rod_db import Database

# Setup database and table
Database.createDirectionTable()

class Motor:
    PERIOD = 4095
    PRESCALER = 10
    FORWARD = 0
    BACKWARD = 1
    def __init__(self, rear_power_pin:PWM, rear_direction_pin:Pin):
        self._forward = 0
        self._backward = 1
        self.rear_power_pin = rear_power_pin
        self.rear_direction_pin = rear_direction_pin
        self.rear_power_pin.period(self.PERIOD)
        self.rear_power_pin.prescaler(self.PRESCALER)

    def _speedCorrection(self, speed):
        speed = abs(speed)
        if speed > 100:
            speed = 100
        if speed > 0:
            speed = int(speed /2 ) + 50
        return speed

    def setDirection(self, direction:int):
        if direction == self.FORWARD:
            self.rear_direction_pin.high()
        else:
            self.rear_direction_pin.low()

    # speed 0 - 100
    def drive(self, speed:int, direction:int):
        c_speed = self._speedCorrection(speed)
        self.setDirection(direction)
        self.rear_power_pin.pulse_width_percent(c_speed)

class LeftMotor(Motor):
    def __init__(self):
        super().__init__(PWM('P12'), Pin('D4'))
        self._forward = 1
        self._backward = 0

class RightMotor(Motor):
    def __init__(self):
        super().__init__(PWM('P13'), Pin('D5'))
        self._forward = 0
        self._backward = 1

class DirectionMotor:
    PIN = 'P2'
    def __init__(self):
        self.direction_pin = Servo(PWM(self.PIN))
        self.current_angle = Database.getLastDirectionMotorAngle()
        self.calibration_offset = -5

    def setAngle(self, angle:int):
        self.current_angle = angle
        self.direction_pin.angle(angle + self.calibration_offset)

    def save(self):
        Database.saveLastDirectionMotorAngle(self.current_angle)
        

