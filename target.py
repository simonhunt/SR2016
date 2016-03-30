import threading
import time
import math
from actions import *

class TargetThread(threading.Thread):
    
    def __init__(self, Threads, MotionThread, time_period = 0.1): #default 10hz
        threading.Thread.__init__(self)
        
        self.name = "TargetThread"
        self.MotionThread = MotionThread
        self.time_period = time_period
        self.lock = threading.Lock()
        self.target = None
        self.polar_r = None
        self.polar_t = None
        
    def calculatePolar(self):
        robot_location = self.MotionThread.robot_location
        dx = self.target['x'] - robot_location['x']
        dy = self.target['y'] - robot_location['y']
        self.polar_r = (dx**2 + dy**2)**0.5
        self.polar_t = math.atan2(math.radians(robot_location['yaw']))
        
        
        
    def run(self):
        print "Starting " + self.name
        
        wake_up_time = time.time() + self.time_period

        while (True):     
            self.time_to_sleep = mapToLimits(wake_up_time - time.time(), self.time_period, 0)
            wake_up_time += self.time_period
            time.sleep(self.time_to_sleep)             
            
            if (self.target == None):
                MotionThread.setAction(STILL)
                
            else:
                
                
            
        
        print "Exiting " + self.name
    
    def debug(self):
        pass