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
        self.steering = 0
        self.steering_updated = True
        self.Y = YawPid
        self.D = MpuHandler
    
    def run(self):
        print "Starting YawThread"
        
        while (True):
            
            if (self.D.updateAll() == True or heading_updated == True):
                pid_input = angleMod(D.yawWithoutDrift - heading)
                global heading_updated
                heading_updated = False
                
            if (Y.run(pid_input) == True):
                self.steering = Y.output
                self.steering_updated = True
                
        print "Exiting " + self.name


    
    
        
        