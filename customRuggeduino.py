from sr.robot import *
import time
from mapToLimits import angleMod

class mpuSonarRuggeduino(Ruggeduino):
    
    def mpuGetYaw(self):
        
        with self.lock:
            yaw = float(self.command('x'))
        return yaw
    
    def mpuGetPitch(self):
        
        with self.lock:
            pitch = float(self.command('y'))
        return pitch
        
    def mpuGetRoll(self):
        
        with self.lock:
            roll = float(self.command('z'))
        return roll
    
    def mpuGetError(self):
        
        with self.lock:
            error = float(self.command('w'))
            
            if (error == 0):
                return False
            
            else:
                return True
        
    def mpuInit(self):
        
        with self.lock:
            self.command('m')
            
    def sonar(self, trigPin, echoPin):   #pin = trig, pin+1=echo
    
        with self.lock:
            trigPinChar = chr(trigPin + 97) 
            echoPinChar = chr(echoPin + 97)
            duration = int(self.command("s" + trigPinChar + echoPinChar))  # s for sonar
        return duration
        
class mpuHandler():
    
    def __init__(self, mpuRuggeduino, yawDrift, timePeriod = 0.025, mpuStartTimeout = 2): # default 40Hz
        currentTime = time.time()
        self.innitTime = currentTime()
        self.timePeriod = timePeriod
        self.mpuRuggeduino = mpuRuggeduino
        self.mpuRuggeduino.mpuInit()
        self.yaw = 0
        self.yawWithoutDrift = 0
        self.yawDrift = yawDrift
        self.pitch = 0
        self.roll = 0
        self.error = 0
        self.lastYawTime = currentTime + mpuStartTimeout - timePeriod
        self.lastPitchTime = currentTime + mpuStartTimeout - timePeriod
        self.lastRollTime = currentTime + mpuStartTimeout - timePeriod
        self.lastErrorTime = currentTime + mpuStartTimeout - timePeriod
        
    def setTimePeriod(self, timePeriod):
        self.timePeriod = timePeriod
        
    def updateAll(self):
        currentTime = time.time()
        dyt = currentTime - self.lastYawTime
        dpt = currentTime - self.lastPitchTime
        drt = currentTime - self.lastRollTime
        det = currentTime - self.lastErrorTime
        updated = False
        
        if ((dyt >= self.timePeriod) and (dpt >= self.timePeriod) and (drt >= self.timePeriod) and (det >= self.timePeriod)):
            self.yaw = self.mpuRuggeduino.mpuGetYaw()
            self.pitch = self.mpuRuggeduino.mpuGetPitch()
            self.roll = self.mpuRuggeduino.mpuGetRoll()
            self.error = self.mpuRuggeduino.mpuGetError()
            self.lastYawTime = currentTime
            self.lastPitchTime = currentTime
            self.lastRollTime = currentTime
            self.lastErrorTime = currentTime
            updated = True 
        self.updateYawWithoutDrift()
        return updated
        
    def updateYawWithoutDrift(self):
        elapsedTime = self.lastYawTime - self.innitTime
        drift = self.yawDrift * elapsedTime
        self.yawWithoutDrift = angleMod(self.yaw - drift)
                
    def updateYaw(self):
        currentTime = time.time()
        dyt = currentTime - self.lastYawTime
        updated = False
        
        if (dyt >= self.timePeriod):
            self.yaw = self.mpuRuggeduino.mpuGetYaw()
            self.lastYawTime = currentTime
            updated = True
        return updated
        
    def updatePitch(self):
        currentTime = time.time()
        dpt = currentTime - self.lastPitchTime
        updated = False
        
        if (dpt >= self.timePeriod):
            self.pitch = self.mpuRuggeduino.mpuGetPitch()
            self.lastPitchTime = currentTime
            updated = True
        return updated
        
    def updateRoll(self):
        currentTime = time.time()
        drt = currentTime - self.lastRollTime
        updated = False
        
        if (drt >= self.timePeriod):
            self.roll = self.mpuRuggeduino.mpuGetRoll()
            self.lastRollTime = currentTime            
            updated = True
        return updated
        
    def updateError(self):
        currentTime = time.time()
        det = currentTime - self.lastErrorTime
        updated = False
        
        if (det >= self.timePeriod):
            self.error = self.mpuRuggeduino.mpuGetError()
            self.lastErrorTime = currentTime
            updated = True
        return updated