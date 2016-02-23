from mapToLimits import mapToLimits

class motorHandler():
    
    def __init__(self, leftMotor, rightMotor, timePeriod = 0.01): #100hz default
        self.timePeriod = timePeriod
        self.lastTime = time.time() - self.timePeriod
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor
        self.speed = 0
        self.steering = 0
        self.update()        
        
    def update(self):
        currentTime = time.time()
        dt = currentTime - self.lastTime
        updated = False
        
        if (dt >= self.timePeriod):
            self.leftSpeed = mapToLimits(self.speed + self.steering)
            self.rightSpeed = mapToLimits(self.speed - self.steering)
            
            self.leftMotor.power = self.leftSpeed
            self.rightMotor.power = self.rightSpeed
            self.lastTime = currentTime
            updated = True
            
        return updated
        
    def setTimePeriod(self, timePeriod):
        self.timePeriod = timePeriod
        
    def setSpeed(self, speed):
        self.speed = mapToLimits(speed)
        return self.update()
    
    def setSteering(self, steering):
        self.steering = mapToLimits(steering, 200, - 200)
        return self.update()
        
    def setSpeedAndSteering(self, speed, steering):
        self.speed = mapToLimits(speed)
        self.steering = mapToLimits(steering, 200, - 200)
        return self.update()