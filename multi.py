import threading
from limits import angleMod

heading = 0
heading_updated = False

def changeHeading(angle):
    global heading
    global heading_updated
    heading = angleMod(heading + angle)
    heading_updated = True
    

class YawThread(threading.Thread):
    
    def __init__(self, YawPid, MpuHandler):
        threading.Thread.__init__(self)
        self.name = "YawThread"
        self.steering = 0
        self.steering_updated = True
        self.Y = YawPid
        self.D = MpuHandler
    
    def run(self):
        print "Starting" + self.name
        
        while (True):
            
            if (self.D.updateAll() == True or heading_updated == True):
                pid_input = angleMod(self.D.yaw_without_drift - heading)
                global heading_updated
                heading_updated = False
                
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
        

    
    
        
        