MAX_STEERING = 200
MIN_STEERING = - 200
MAX_SPEED = 100
MIN_SPEED = - 100
MAX_OUTPUT = 100
MIN_OUTPUT = -100

import time
from limits import mapToLimits

class MotorHandler():
    
    def __init__(self, LeftMotor, RightMotor, time_period = 0.01): #100hz default
        self.LeftMotor = LeftMotor
        self.RightMotor = RightMotor
        self.time_period = time_period
        self.last_time = time.time() - self.time_period
        self.speed = 0
        self.steering = 0
        self.update()        
        
    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        updated = False
        
        if (dt >= self.time_period):
            self.left_speed = mapToLimits((self.speed - self.steering), MAX_OUTPUT, MIN_OUTPUT)
            self.right_speed = mapToLimits((self.speed + self.steering), MAX_OUTPUT, MIN_OUTPUT)
            
            self.LeftMotor.power = self.left_speed
            self.RightMotor.power = self.right_speed
            self.last_time = current_time
            updated = True
            
        return updated
        
    def setTimePeriod(self, time_period):
        self.time_period = time_period
        
    def setSpeed(self, speed):
        self.speed = mapToLimits(speed, MAX_SPEED, MIN_SPEED)
        return self.update()
    
    def setSteering(self, steering):
        self.steering = mapToLimits(steering, MAX_STEERING, MIN_STEERING)
        return self.update()
        
    def setSpeedAndSteering(self, speed, steering):
        self.speed = mapToLimits(speed, MAX_SPEED, MIN_SPEED)
        self.steering = mapToLimits(steering, MAX_STEERING, MIN_STEERING)
        return self.update()