import threading
from limits import angleMod

heading = [True, 0]

def changeHeading(angle):
    global heading
    heading[0] = True
    heading[0] = angleMod(

class YawThread(threading.Thread):
    
    def __init__(self, YawPid, MpuHandler):
        threading.Thread.__init__(self)
        self.Y = YawPid
        self.D = MpuHandler
    
    def run(self):
        print "Starting YawThread"
        
        if (self.D.updateAll() == True):
            pass
            
        print "Exiting " + self.name


    
    
        
        