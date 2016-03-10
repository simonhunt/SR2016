import threading
import time
from limits import angleMod

class MotionThread(threading.Thread):
    
    def __init__(self, MpuHandler, YawPid, MotorHandler, timePeriod = 0.01):
        threading.Thread.__init__(self)
        self.name = "MotionThread"
        self.steering = 0
        self.yaw = 0
        self.heading = 0
        self.heading_available = True
        self.speed = 0
        self.speed_available = True
        self.new_speed = False
        self.D = MpuHandler
        self.Y = YawPid
        self.M = MotorHandler
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
            #print "ran while loop in motionThread"
            
            new_steering = False
            
            if (self.D.updateAll == True):
                print "D.ua = true"
                self.yaw = self.D.yaw_without_drift
            
            self.heading_available = False
            heading = self.heading
            self.heading_available = True
            
            pid_input = angleMod(self.yaw - heading)
            
            if (self.Y.run(pid_input) == True):
                self.steering = self.Y.output
                new_steering = True
            
            self.speed_available = False
            speed = self.speed
            self.speed_available = True
            
            if (new_steering == True or self.new_speed == True):
                self.M.setSpeedAndSteering(speed, self.steering)
                self.new_speed = False
            
            time.sleep(self.timePeriod)
                
        print "Exiting " + self.name

#import threading
#from limits import angleMod

#heading = 0
#heading_updated = False
#
#def changeHeading(angle):
#    global heading
#    global heading_updated
#    heading = angleMod(heading + angle)
#    heading_updated = True
    
#class MotionThread(threading.Thread):
#    
#    def __init__(self, YawThread, MotorThread):
#        threading.Thread.__init__(self)
#        self.name = "MotionThread"
#        self.heading = 0
#        self.speed_updated = False
#        self.speed = 0
#        self.YT = YawThread
#        self.MT = MotorThread
#    
#    def changeHeading(self, angle):
#        self.heading = angleMod(self.heading + angle)
#        self.YT.heading = self.heading
#        self.YT.heading_updated = True
#        
#    def setSpeed(self, speed):
#        self.speed = speed
#        self.speed_updated = True
#    
#    def run(self):
#        print "Starting" + self.name
#        
#        self.YT.start()
#        print "YawThread started"
#        
#        self.MT.start()
#        print "MotorThread started"
#        
#        while (True):
#            
#            if (self.YT.steering_updated == True):
#                self.MT.steering = self.YT.steering
#            
#            if (self.speed_updated == True):
#                self.MT.speed = self.speed            
#                
#        print "Exiting " + self.name
#
#
#
#class YawThread(threading.Thread):
#    
#    def __init__(self, YawPid, MpuHandler):
#        threading.Thread.__init__(self)
#        self.name = "YawThread"
#        self.heading = 0
#        self.heading_updated = False
#        self.steering = 0
#        self.steering_updated = True
#        self.Y = YawPid
#        self.D = MpuHandler
#        
#    def run(self):
#        print "Starting" + self.name
#        
#        while (True):
#            
#            if (self.D.updateAll() == True or self.heading_updated == True):
#                pid_input = angleMod(self.D.yaw_without_drift - self.heading)
#                self.heading_updated = False
#                
#            if (self.Y.run(pid_input) == True):
#                self.steering = self.Y.output
#                self.steering_updated = True
#                
#        print "Exiting " + self.name
#        
#class MotorThread(threading.Thread):
#    
#    def __init__(self, MotorHandler):
#        threading.Thread.__init__(self)
#        self.name = "MotorThread"
#        self.steering = 0
#        self.speed = 0
#        self.S = MotorHandler
#    
#    def run(self):
#        print "Starting" + self.name
#        while (True):
#            
#           self.S.setSpeedAndSteering(self.speed, self.steering)
#                
#        print "Exiting " + self.name
#        

    
    
        
        