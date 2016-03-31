import threading
import time
import math
from limits import mapToLimits
from actions import *

class TargetThread(threading.Thread):
    
    def __init__(self, MotionThread, time_period = 5): #default 10hz
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
        self.polar_t = math.degrees(math.atan2(dy, dx)) 
    
    def setTarget(self, target):
        
        with self.lock:
            self.target = target
        
    def run(self):
        print "Starting " + self.name
        
        wake_up_time = time.time() + self.time_period

        while (True):     
            self.time_to_sleep = mapToLimits(wake_up_time - time.time(), self.time_period, 0)
            wake_up_time += self.time_period
            time.sleep(self.time_to_sleep)  
            with self.lock:
                
                if (self.target == None):
                    self.MotionThread.setAction(STILL)
                
                else:
                    self.calculatePolar()
                    self.MotionThread.setAction(MOVE_AND_TURN_TO, self.polar_r, self.polar_t)
                    
                    while(True):
                        self.time_to_sleep = mapToLimits(wake_up_time - time.time(), self.time_period, 0)
                        wake_up_time += self.time_period
                        time.sleep(self.time_to_sleep)
                        self.calculatePolar()
                        self.MotionThread.setAction(MOVE_AND_TURN_TO_CHANGE, self.polar_r, self.polar_t)
        print "Exiting " + self.name
    
    def debug(self):
        pass