import threading
import time
from limits import angleMod

STILL = 0
TURN = 1
MOVE_HOLD = 2
MOVE = 3

class MotionThread(threading.Thread):
    
    def __init__(self, MpuHandler, YawPid, MotorHandler, DisplacementPid, EncoderHandler, time_period = 0.01):
        threading.Thread.__init__(self)
        self.name = "MotionThread"
        self.steering = 0
        self.speed = 0
        self.yaw = 0
        self.desired_yaw = 0
        self.forced_speed = 0
        self.forced_speed_available = True
        self.new_forced_speed = False
        self.displacement = 0
        self.desired_displacement = 0
        self.D = MpuHandler
        self.Y = YawPid
        self.M = MotorHandler
        self.S = DisplacementPid
        self.E = EncoderHandler
        self.time_period = time_period
        
        self.action = STILL
        self.action_value = 0
        self.action_needs_processing = True
        
    def setForcedSpeed(self, speed):
        updated = False
        
        if (self.forced_speed_available == True):
            self.forced_speed = speed
            self.new_forced_speed = True
            updated = True
        return updated
        
    def setAction(self, action, action_value):
        self.action_needs_processing = False
        self.action = action
        self.action_value = action_value
        self.action_needs_processing = True
    
    def processAction(self):
        
        if (self.action_needs_processing == True):
            
            if (self.action == STILL):
                self.Y.stop()
                self.S.stop() 
            
            elif (self.action == TURN):
                self.Y.restart()
                self.deired_yaw = self.yaw + self.action_value
                self.S.stop()
                
            
            elif (self.action == MOVE):
                self.Y.stop()
                self.S.restart()
                self.desired_displacement = self.displacement + action.value
            
            elif (self.action == MOVE_HOLD):
                self.Y.restart()
                self.desired_heading = self.yaw
                self.S.restart()
                self.desired_displacement = self.displacement + action.value
                
    
    def run(self):
        print "Starting " + self.name
        
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
            
            self.processAction()
            
            yaw_pid_input = angleMod(self.yaw - self.desired_yaw)
            
            if (self.Y.run(yaw_pid_input) == True):
                self.steering = self.Y.output
                new_steering = True
                
            else:
                print "Y returned false in Motion Thread"
            
            
            if (self.S.run(self.displacement) == True):
                self.speed = self.S.output
                self.new_speed = True
                
            else:
                print "S returned false in Motion Thread"
            
            
            if (self.new_forced_speed == True):
                self.forced_speed_available = False
                self.speed = self.forced_speed
                self.forced_speed_available = True
                new_speed = True
                self.new_forced_speed = False
            
            if (new_steering == True or new_speed == True):
                self.M.setSpeedAndSteering(self.speed, self.steering)
            else:
                print "speed and steering not set in Motion Thread"
                
            
            
            time.sleep(self.time_period)
                
        print "Exiting " + self.name
