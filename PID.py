import time
from mapToLimits import mapToLimits

class pidController():
    
    def __init__(self, name, kp = 0, ki = 0, kd = 0, setpoint = 0, iLimit = 0, startingI = 0, timePeriod = 0.05): # default 20Hz
        self.name = name
        self.kp = kp
        self.ki = ki    
        self.kd = kd
        self.setpoint = setpoint
        self.timePeriod = timePeriod
        self.lastTime = 0
        self.lastError = 0
        self.i = startingI
        self.iLimit = iLimit
        self.output = 0
        self.firstRun = True
    
    def setCoefficients(self, newKp, newKi, newKd):
        self.kp = newKp
        self.ki = newKi
        self.kd = newKd
    
    def setTimeperiod(self, timePeriod):
        self.timePeriod = timePeriod
        
    def setSetpoint(self, newSetpoint):
        self.Setpoint = newSetpoint
        
    def restart(self):
        self.firstRun = True
        
    def run(self, value):
        currentTime = time.time()
        dt = currentTime - self.lastTime
        outputCalculated = False
        
        if (self.firstRun == False):
            
            if (dt >= self.timePeriod): 
                error = value - self.setpoint
                
                p = self.kp * error
                self.i += self.ki * error * dt
                d = (error - self.lastError) / dt
                
                if (self.iLimit != 0):
                    self.i = mapToLimits(self.i, self.iLimit, - self.iLimit)
                
                self.output = p + self.i + d
                outputCalculated = True
        
                self.lastTime = currentTime
                self.lastError = error
                
        else: #self.firstRun == True
            error = value - self.setpoint
            
            p = self.kp * error
            self.i += 0
            d = 0
            
            if (self.iLimit != 0):
                self.i = mapToLimits(self.i, self.iLimit, - self.iLimit)
            
            self.output = p + self.i + d
            outputCalculated = True
        
            self.lastTime = currentTime
            self.lastError = error
            self.firstRun = False
        
        return outputCalculated
        
        