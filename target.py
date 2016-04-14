import threading
import time
import math
from limits import mapToLimits
from actions import *
from debug import DEBUG_TARGET

class TargetThread(threading.Thread):
    
    def __init__(self, MotionThread, target_timeperiod = 0.1, move_timeperiod = 0.01, target_reached_radius = 0.1): #default 10hz target, 100hz move, 10cm target radius
        threading.Thread.__init__(self)
        
        self.name = "TargetThread"
        self.MotionThread = MotionThread
        self.move_timeperiod = move_timeperiod
        self.target_timeperiod = target_timeperiod
        self.target_reached_radius = target_reached_radius
        self.path_lock = threading.Lock()
        self.emergency_lock = threading.Lock()
        self.path = []
        self.target = None
        self.polar_r = None
        self.polar_t = None
        self.emergency_stop = False 
        
    def clearPath(self):
        
        with self.path_lock:
            self.path = []
    
    def setTarget(self, new_target):
        
        self.clearPath()
        self.addTarget(new_target)
    
    def addTarget(self, new_target):
        
        with self.path_lock:
            self.path.append(new_target)
    
    def setPath(self, new_path):
        
        self.clearPath()
        self.addPath(new_path)
            
    def addPath(self, new_path):
        
        with self.path_lock:
            self.path.extend(new_path)
            
    def calculatePolar(self):
        robot_location = self.MotionThread.robot_location ##needs attention
        dx = self.target['x'] - robot_location['x']
        dy = self.target['y'] - robot_location['y']
        self.polar_r = (dx**2 + dy**2)**0.5
        self.polar_t = math.degrees(math.atan2(dy, dx))
    
    def processNextTarget(self):
        
        self.target = None
        
        with self.path_lock:
            
            if (len(self.path) != 0):
                self.target = self.path.pop(0)
            
        if (self.target != None):
            
            self.moveToTarget()
            
    def setEmergencyStop(self, new_emergency_stop):
        
        with self.emergency_lock:
            self.emergency_stop = new_emergency_stop
            
    def checkEmergencyStop(self):
        
        with self.emergency_lock:
            return self.emergency_stop
            
    def checkIfTargetReached(self):
        reached = False
        
        if (self.polar_r < self.target_reached_radius):
            reached = True
            print 'target reached'
            
        return reached
            
    def moveToTarget(self):
        
        self.setupMoveToTarget()
        
        while ((self.checkEmergencyStop() == False) and (self.checkIfTargetReached == False)):
            time.sleep(self.move_timeperiod) 
            self.calculatePolar()
            self.MotionThread.setAction(MOVE_AND_TURN_TO_CHANGE, self.polar_r, self.polar_t)
    
    def setupMoveToTarget(self):
        
        if (self.checkEmergencyStop() == False):
            self.calculatePolar()
            self.MotionThread.setAction(MOVE_AND_TURN_TO, self.polar_r, self.polar_t)
        
            
    def run(self):
        print "Starting " + self.name
        
        while(True):
            self.processNextTarget()
            time.sleep(self.target_timeperiod)
            
        print "Exiting " + self.name
        
#    def run(self):
#        print "Starting " + self.name
#        
#        wake_up_time = time.time() + self.time_period
#
#        while (True):     
#            self.time_to_sleep = mapToLimits(wake_up_time - time.time(), self.time_period, 0)
#            wake_up_time += self.time_period
#            time.sleep(self.time_to_sleep)  
#            with self.lock:
#                
#                if (self.target == None):
#                    self.MotionThread.setAction(STILL)
#                
#                else:
#                    self.calculatePolar()
#                    self.MotionThread.setAction(MOVE_AND_TURN_TO, self.polar_r, self.polar_t)
#                    
#                    while (True):
#                        self.time_to_sleep = mapToLimits(wake_up_time - time.time(), self.time_period, 0)
#                        wake_up_time += self.time_period
#                        time.sleep(self.time_to_sleep) 
#                        self.calculatePolar()
#                        self.MotionThread.setAction(MOVE_AND_TURN_TO_CHANGE, self.polar_r, self.polar_t)
#                        
#                        
#        print "Exiting " + self.name
    
    def debug(self):
        
        if (DEBUG_TARGET == True):
            
            print self.name
            print "target = " + str(self.target)
            print "len(path) = " + str(len(self.path))
            print "polar_r = " + str(self.polar_r) + ", polar_t = " + str(self.polar_t)
            