MAX_STEERING = 160
MIN_STEERING = - 160
MAX_SPEED = 80
MIN_SPEED = - 80
MAX_OUTPUT = 80
MIN_OUTPUT = - 80
MAX_STEERING_ACCEL = 50 #units %/sec
MAX_SPEED_ACCEL = 100 #units %/sec
LINEAR_POWER_POINT = 20
MIN_LINEAR_POWER = 20

import time
from limits import mapToLimits

def accelerationRestrictor(dt, last_value, desired_value, max_accel):
    max_change = dt * max_accel
    value_upper_limit = last_value + max_change
    value_lower_limit = last_value - max_change
    output = mapToLimits(desired_value, value_upper_limit, value_lower_limit)
    return output

def powerDeadzoneHandler(power):
    
    if ((power < LINEAR_POWER_POINT) and (power > - LINEAR_POWER_POINT)):
        power += (MIN_LINEAR_POWER) * (power / LINEAR_POWER_POINT)
    
    elif (power > 0): #positive
        power += MIN_LINEAR_POWER
    
    else: #negative
        power -= MIN_LINEAR_POWER
        
    return power

class MotorHandler():
    
    def __init__(self, LeftMotor, RightMotor, time_period = 0.005): #200hz default
        self.name = "MotorHandler"
        self.LeftMotor = LeftMotor
        self.RightMotor = RightMotor
        self.time_period = time_period
        self.last_time = time.time() - self.time_period
        self.speed = 0
        self.desired_speed = 0
        self.last_speed = 0
        self.steering = 0
        self.desired_steering = 0
        self.last_steering = 0
        self.left_power = 0
        self.right_power = 0
        
    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        updated = False
        
        if (dt >= self.time_period):
            self.speed = accelerationRestrictor(dt, self.last_speed, self.desired_speed, MAX_SPEED_ACCEL)
            self.steering = accelerationRestrictor(dt, self.last_steering, self.desired_steering, MAX_STEERING_ACCEL)
            
            left_power = mapToLimits((self.speed - self.steering), MAX_OUTPUT, MIN_OUTPUT)
            right_power = mapToLimits((self.speed + self.steering), MAX_OUTPUT, MIN_OUTPUT)
            
            self.left_power = powerDeadzoneHandler(left_power)
            self.right_power = powerDeadzoneHandler(right_power)
            
            self.LeftMotor.power = int(self.left_power)
            self.RightMotor.power = int(self.right_power)
            
            self.last_speed = self.speed
            self.last_steering = self.steering
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
        
    def debug(self):
        print self.name + ": desired_speed = " + str(self.desired_speed) + ", speed = " + str(self.speed) + ", desired_steering = " + str(self.desired_steering) + ", steering = " + str(self.steering) + ", left_power = " + str(self.left_power) + ", right_power = " + str(self.right_power)
        