import time
from limits import mapToLimits

class MotorHandler():
    
    def __init__(self, LeftMotor, RightMotor, maxSteering = 200, time_period = 0.01): #100hz default
        self.LeftMotor = LeftMotor
        self.RightMotor = RightMotor
        self.maxSteering = maxSteering
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
            self.left_speed = mapToLimits(self.speed - self.steering)
            self.right_speed = mapToLimits(self.speed + self.steering)
            
            self.LeftMotor.power = self.left_speed
            self.RightMotor.power = self.right_speed
            self.last_time = current_time
            updated = True
            
        return updated
        
    def setTimePeriod(self, time_period):
        self.time_period = time_period
        
    def setSpeed(self, speed):
        self.speed = mapToLimits(speed)
        return self.update()
    
    def setSteering(self, steering):
        self.steering = mapToLimits(steering, self.maxSteering, - self.maxSteering)
        return self.update()
        
    def setSpeedAndSteering(self, speed, steering):
        self.speed = mapToLimits(speed)
        self.steering = mapToLimits(steering, 200, - 200)
        return self.update()