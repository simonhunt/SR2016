import threading
import time
from limits import angleMod

class MotionThread(threading.Thread):
    
    def __init__(self, MpuHandler, YawPid, MotorHandler, EncoderHandler, timePeriod = 0.01):
        threading.Thread.__init__(self)
        self.name = "MotionThread"
        self.steering = 0
        self.yaw = 0
        self.heading = 0
        self.heading_available = True
        self.speed = 0
        self.speed_available = True
        self.new_speed = False
        self.displacement = 0
        self.D = MpuHandler
        self.Y = YawPid
        self.M = MotorHandler
        self.E = EncoderHandler
        self.timePeriod = timePeriod
    
    def changeHeading(self, angle):
        updated = False
        
        if (self.heading_available == True):
            self.heading = self.heading + angle
            updated = True
        return updated
        
    def setSpeed(self, speed):
        updated = False
        
        if (self.speed_available == True):
            self.speed = speed
            updated = True
        self.new_speed = updated
        return updated
    
    def run(self):
        print "Starting" + self.name
        
        while (True):
            
            new_steering = False
            
            if (self.D.updateAll() == True):
                self.yaw = self.D.yaw_without_drift
                
            else:
                print "D returned false in Motion Thread"
                
            if (self.E.update() == True):
                self.displacement = self.E.displacement
                
            else:
                print "E returned false in Motion Thread"
            
            self.heading_available = False
            heading = self.heading
            self.heading_available = True
            
            pid_input = angleMod(self.yaw - heading)
            
            if (self.Y.run(pid_input) == True):
                self.steering = self.Y.output
                new_steering = True
                
            else:
                print "Y returned false in Motion Thread"
            
            self.speed_available = False
            speed = self.speed
            self.speed_available = True
            
            if (new_steering == True or self.new_speed == True):
                self.M.setSpeedAndSteering(speed, self.steering)
                self.new_speed = False
            else:
                print "speed and steering not set in Motion Thread"
                
            
            
            time.sleep(self.timePeriod)
                
        print "Exiting " + self.name
