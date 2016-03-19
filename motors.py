MAX_STEERING = 200
MIN_STEERING = - 200
MAX_SPEED = 100
MIN_SPEED = - 100
MAX_OUTPUT = 100
MIN_OUTPUT = -100
MAX_STEERING_ACCEL = 50 #units %/sec
MAX_SPEED_ACCEL = 100 #units %/sec

import time
from limits import mapToLimits

def accelerationRestrictor(dt, last_value, desired_value, max_accel):
    max_change = dt * max_accel
    value_upper_limit = last_value + max_change
    value_lower_limit = last_value - max_change
    output = mapToLimits(desired_value, value_upper_limit, value_lower_limit)
    return output

class MotorHandler():
    
    def __init__(self, LeftMotor, RightMotor, time_period = 0.01): #100hz default
        self.LeftMotor = LeftMotor
        self.RightMotor = RightMotor
        self.time_period = time_period
        self.last_time = time.time() - self.time_period
        self.desired_speed = 0
        self.last_speed = 0
        self.desired_steering = 0
        self.last_steering = 0
        #self.update()        #dont think this line is needed (not sure why I ever used it)
        
    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        updated = False
        
        if (dt >= self.time_period):
            speed = accelerationRestrictor(dt, self.last_speed, self.desired_speed, MAX_SPEED_ACCEL)
            steering = accelerationRestrictor(dt, self.last_steering, self.desired_steering, MAX_STEERING_ACCEL)
            
            left_speed = mapToLimits((speed - steering), MAX_OUTPUT, MIN_OUTPUT)
            right_speed = mapToLimits((speed + steering), MAX_OUTPUT, MIN_OUTPUT)
            
            self.LeftMotor.power = left_speed
            self.RightMotor.power = right_speed
            
            self.last_speed = speed
            self.last_steering = steering
            self.last_time = current_time
            updated = True   
        return updated
        
    def setTimePeriod(self, time_period):
        self.time_period = time_period
        
    def setDesiredSpeed(self, desired_speed):
        self.desired_speed = mapToLimits(desired_speed, MAX_SPEED, MIN_SPEED)
        return self.update()
    
    def setDesiredSteering(self, desired_steering):
        self.desired_steering = mapToLimits(desired_steering, MAX_STEERING, MIN_STEERING)
        return self.update()
        
    def setDesiredSpeedAndSteering(self, desired_speed, desired_steering):
        self.desired_speed = mapToLimits(desired_speed, MAX_SPEED, MIN_SPEED)
        self.desired_steering = mapToLimits(desired_steering, MAX_STEERING, MIN_STEERING)
        return self.update()