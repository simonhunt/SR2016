import time
import math

import threading
import polar
import noise

from limits import mapToLimits, angleMod
from actions import *
from debug import DEBUG_TARGET

class TargetThread(threading.Thread):
    
    def __init__(self, MotionThread, power, target_timeperiod = 0.1, move_timeperiod = 0.1, target_reached_radius = 0.1): #default 10hz target, 10hz move, 10cm target radius
        threading.Thread.__init__(self)
        
        self.name = "TargetThread"
        self.MotionThread = MotionThread
        self.power = power
        self.move_timeperiod = move_timeperiod
        self.target_timeperiod = target_timeperiod
        self.target_reached_radius = target_reached_radius
        self.path_lock = threading.Lock()
        self.emergency_lock = threading.Lock()
        self.path = []
        self.target = None
        self.polar_r = None
        self.scaled_polar_r = None
        self.polar_t = None
        self.d_theta = None
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
        self.polar_r = polar.getPolarR(robot_location, self.target)
        self.polar_t = polar.getPolarT(robot_location, self.target)
        self.d_theta = angleMod(self.polar_t - robot_location['yaw'])
        self.scaled_polar_r = math.cos(math.radians(self.d_theta)) * self.polar_r
    
    def processNextTarget(self):
        
        self.target = None
        
        with self.path_lock:
            
            if (len(self.path) != 0):
                self.target = self.path.pop(0)  #return first item in array and remove it from array

        if (self.target != None):    
            self.turnToTarget()
            self.moveToTarget()
            
    def setEmergencyStop(self, new_emergency_stop):
        
        with self.emergency_lock:
            self.emergency_stop = new_emergency_stop
            
    def checkEmergencyStop(self):
        
        with self.emergency_lock:
            return self.emergency_stop
            
    def checkIfTurnedToTarget(self):
        turned = False
        
        max_d_theta = self.target.get('max_d_theta', 180)
        
        if (abs(self.d_theta) <= max_d_theta):
            turned = True
            noise.signalTarget(self.power)
            
        return turned
        
    def turnToTarget(self):        
        self.calculatePolar()
        
        if ((self.checkEmergencyStop() == False) and (self.checkIfTurnedToTarget() == False)):
            self.MotionThread.setAction(TURN_TO, self.polar_t)
            time.sleep(self.move_timeperiod)
            
            while ((self.checkEmergencyStop() == False) and (self.checkIfTurnedToTarget() == False)):
                self.calculatePolar() 
                self.MotionThread.addAction(TURN_TO_CHANGE, self.polar_t)
            
    def checkIfTargetReached(self):
        reached = False
        
        if (self.polar_r < self.target_reached_radius):
            reached = True
            noise.signalTarget(self.power)
            
        return reached
        
    def changeCurrentTarget(self, new_current_target):
        self.target = new_current_target
            
    def moveToTarget(self):        
        self.calculatePolar()
        
        if ((self.checkEmergencyStop() == False) and (self.checkIfTargetReached() == False)):
            self.MotionThread.setAction(MOVE_AND_TURN_TO, self.scaled_polar_r, self.polar_t)
            time.sleep(self.move_timeperiod)
            
            while ((self.checkEmergencyStop() == False) and (self.checkIfTargetReached() == False)):
                self.calculatePolar() 
                self.MotionThread.addAction(MOVE_AND_TURN_TO_CHANGE, self.scaled_polar_r, self.polar_t)
                time.sleep(self.move_timeperiod) 
            
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
            print "polar_r = " + str(self.polar_r) + ", polar_t = " + str(self.polar_t) + ", scaled_polar_r = " + str(self.scaled_polar_r) + ", d_theta = " + str(self.d_theta)
            