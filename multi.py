import threading
from limits import angleMod

#heading = 0
#heading_updated = False
#
#def changeHeading(angle):
#    global heading
#    global heading_updated
#    heading = angleMod(heading + angle)
#    heading_updated = True
    
class MotionThread(threading.Thread):
    
    def __init__(self, YawThread, MotorThread):
        threading.Thread.__init__(self)
        self.name = "MotionThread"
        self.heading = 0
        self.speed_updated = False
        self.speed = 0
        self.YT = YawThread
        self.MT = MotorThread
    
    def changeHeading(self, angle):
        self.heading = angleMod(self.heading + angle)
        self.YT.heading = self.heading
        self.YT.heading_updated = True
        
    def setSpeed(self, speed):
        self.speed = speed
        self.speed_updated = True
    
    def run(self):
        print "Starting" + self.name
        
        self.YT.start()
        print "YawThread started"
        
        self.MT.start()
        print "MotorThread started"
        
        while (True):
            
            if (self.YT.steering_updated == True):
                self.MT.steering = self.YT.steering
            
            if (self.speed_updated == True):
                self.MT.speed = self.speed            
                
        print "Exiting " + self.name
    

class YawThread(threading.Thread):
    
    def __init__(self, YawPid, MpuHandler):
        threading.Thread.__init__(self)
        self.name = "YawThread"
        self.heading = 0
        self.heading_updated = False
        self.steering = 0
        self.steering_updated = True
        self.Y = YawPid
        self.D = MpuHandler
        
    def run(self):
        print "Starting" + self.name
        
        while (True):
            
            if (self.D.updateAll() == True or self.heading_updated == True):
                pid_input = angleMod(self.D.yaw_without_drift - self.heading)
                self.heading_updated = False
                
            if (self.Y.run(pid_input) == True):
                self.steering = self.Y.output
                self.steering_updated = True
                
        print "Exiting " + self.name
        
class MotorThread(threading.Thread):
    
    def __init__(self, MotorHandler):
        threading.Thread.__init__(self)
        self.name = "MotorThread"
        self.steering = 0
        self.speed = 0
        self.S = MotorHandler
    
    def run(self):
        print "Starting" + self.name
        while (True):
            
           self.S.setSpeedAndSteering(self.speed, self.steering)
                
        print "Exiting " + self.name
        

    
    
        
        