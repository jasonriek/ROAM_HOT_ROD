from time import sleep

from hot_rod_motors import (
    LeftMotor, 
    RightMotor, 
    DirectionMotor
)

DELAY = 0.01

class Driver:
    def __init__(self):
        self.left_motor = LeftMotor()
        self.right_motor = RightMotor()
        self.direction_motor = DirectionMotor()

    def driveForward(self, speed:int):
        self.left_motor.drive(speed, self.left_motor._forward)
        self.right_motor.drive(speed, self.right_motor._forward)
    
    def driveBackward(self, speed:int):
        self.left_motor.drive(speed, self.left_motor._backward)
        self.right_motor.drive(speed, self.right_motor._backward)
    
    def stop(self):
        self.left_motor.drive(0, self.left_motor._forward)
        self.right_motor.drive(0, self.right_motor._forward)
    
    def center(self):
        last_angle = self.direction_motor.current_angle
        if last_angle < 0:
            for angle in range(last_angle, 0):
                self.direction_motor.setAngle(angle)
                sleep(DELAY)
        else:
            for angle in range(last_angle, 0, -1):
                self.direction_motor.setAngle(angle)
                sleep(DELAY)

    def turnSharpRight(self):
        last_angle = self.direction_motor.current_angle
        for angle in range(last_angle, 35):
            self.direction_motor.setAngle(angle)
            sleep(DELAY)
    
    def turnSharpLeft(self):
        last_angle = self.direction_motor.current_angle
        for angle in range(last_angle, -35, -1):
            self.direction_motor.setAngle(angle)
            sleep(DELAY)
    
    def saveMotorSettings(self):
        self.direction_motor.save()