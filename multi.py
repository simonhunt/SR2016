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
        self.action_available = True
        self.action_needs_processing = True
        
    def setAction(self, action, action_value):
        
        if (self.action_available == True):
            self.action_needs_processing = False
            self.action = action
            self.action_value = action_value
            self.action_needs_processing = True
        
        else: #self.action_available == False
            print "ERROR: no action set in MotionThread.setAction()"
    
    def processAction(self):
        
        if (self.action_needs_processing == True):
            self.action_available = False
            
            if (self.action == STILL):
                self.Y.stop()
                self.S.stop()
                print "New Action: STILL"
            
            elif (self.action == TURN):
                self.Y.restart()
                self.desired_yaw = self.yaw + self.action_value
                self.S.stop() 
                print "New Action: TURN, with value: " + str(self.action_value)
            
            elif (self.action == MOVE):
                self.Y.stop()
                self.S.restart()
                self.desired_displacement = self.displacement + self.action_value
                self.S.setSetpoint(self.desired_displacement)
                print "New Action: MOVE, with value: " + str(self.action_value)
            
            elif (self.action == MOVE_HOLD):
                self.Y.restart()
                self.desired_yaw = self.yaw
                self.S.restart()
                self.desired_displacement = self.displacement + self.action_value
                self.S.setSetpoint(self.desired_displacement)
                print "New Action: MOVE_HOLD, with value: " + str(self.action_value)
                
            else:
                print "ERROR: unknown action processed in motionThread.processAction"
            
            self.action_available = True                
            self.action_needs_processing = False
                
    
    def run(self):
        print "Starting " + self.name
        
        while (True):
            
            new_steering = False
            new_speed = False
            
            if (self.D.updateAll() == True):
                self.yaw = self.D.yaw_without_drift
                
            else:
                print "ERROR: D returned false in Motion Thread"
                
            if (self.E.update() == True):
                self.displacement = self.E.displacement
                
            else:
                print "ERROR: E returned false in Motion Thread"
            
            self.processAction()
            
            yaw_pid_input = angleMod(self.yaw - self.desired_yaw)
            
            if (self.Y.run(yaw_pid_input) == True):
                self.steering = self.Y.output
                new_steering = True
                
            else:
                print "ERROR: Y returned false in Motion Thread"
            
            
            if (self.S.run(self.displacement) == True):
                self.speed = self.S.output
                new_speed = True
                
            else:
                print "ERROR: S returned false in Motion Thread"
            
            if (new_steering == True or new_speed == True):
                self.M.setSpeedAndSteering(self.speed, self.steering)
            else:
                print "ERROR: speed and steering not set in Motion Thread"
            
            time.sleep(self.time_period)
                
        print "Exiting " + self.name
