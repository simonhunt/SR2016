import threading
import time
import math
from limits import angleMod

STILL = 0
TURN = 1
MOVE_HOLD = 2
MOVE = 3
INITIAL_OFFSET = 9

def displacementByArcApproximation(length, theta_1, theta_2):
    theta_1 = math.radians(theta_1) #convert angles into radians
    theta_2 = math.radians(theta_2)
    dtheta = theta_2 - theta_1
    radius = length / dtheta
    dx = radius * (math.sin(theta_2) - math.sin(theta_1))
    dy = radius * (math.cos(theta_1) - math.cos(theta_2))
    return {'x': dx, 'y': dy}

def displacementByLineApproximation(length, theta_1, theta_2):
    theta_1 = math.radians(theta_1) #convert angles into radians
    theta_2 = math.radians(theta_2)
    average_theta = (theta_1 + theta_2) / 2
    dx = length * math.cos(average_theta)
    dy = length * math.sin(average_theta)
    return {'x': dx, 'y': dy}

class MotionThread(threading.Thread):
    
    def __init__(self, MpuHandler, YawPid, MotorHandler, DistancePid, EncoderHandler, time_period = 0.01):
        
        threading.Thread.__init__(self)
        
        self.name = "MotionThread"
        
        self.steering = 0
        self.speed = 0
        
        self.yaw = 0
        self.last_yaw = 0
        self.desired_yaw = 0
        
        self.distance = 0
        self.last_distance = 0
        self.desired_distance = 0
        
        self.location_lock = threading.Lock()
        self.arc_displacement = {'x': 0, 'y': 0}
        self.line_displacement = {'x': 0, 'y': 0}
        
        self.D = MpuHandler
        self.Y = YawPid
        self.M = MotorHandler
        self.S = DistancePid
        self.E = EncoderHandler
        
        self.time_period = time_period
        
        self.offset_lock = threading.Lock()
        self.mpu_yaw_offset = INITIAL_OFFSET
        self.new_mpu_yaw_offset = 0
        
        self.action_lock = threading.Lock()
        self.action = STILL
        self.action_value = 0
        self.action_needs_processing = True
        
    def setRobotLocation(self, robot_location):
        
        with self.location_lock:
            self.robot_location = robot_location
            self.arc_displacement = {'x': 0, 'y': 0}
            self.line_displacement = {'x': 0, 'y': 0}
            
        with self.offset_lock:
            self.
        
    def setAction(self, action, action_value = 0):
        
        with self.action_lock:
            self.action = action
            self.action_value = action_value
            self.action_needs_processing = True
    
    def processAction(self):
        
        with self.action_lock:
            
            if (self.action_needs_processing == True):
                
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
                    self.desired_distance = self.distance + self.action_value
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE, with value: " + str(self.action_value)
                
                elif (self.action == MOVE_HOLD):
                    self.Y.restart()
                    self.desired_yaw = self.yaw
                    self.S.restart()
                    self.desired_distance = self.distance + self.action_value
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE_HOLD, with value: " + str(self.action_value)
                    
                else:
                    print "ERROR: unknown action processed in motionThread.processAction"
                   
                self.action_needs_processing = False
            
    def displacementManager(self):
        theta_1 = self.last_yaw
        theta_2 = self.yaw
        length = self.distance - self.last_distance
        
        dline_displacement = displacementByLineApproximation(length, theta_1, theta_2)
        
        if (theta_2 == theta_1): #error case for arc length /0 err
            darc_displacement = dline_displacement
        else:
            darc_displacement = displacementByArcApproximation(length, theta_1, theta_2)
        
        with self.location_lock:
            self.line_displacement['x'] += dline_displacement['x']
            self.line_displacement['y'] += dline_displacement['y']
            self.arc_displacement['x'] += darc_displacement['x']
            self.arc_displacement['y'] += darc_displacement['y']
    
    def debug(self):
        print self.name
        
        print "desired_yaw = " + str(self.desired_yaw) + ", yaw = " + str(self.yaw) + ", D.yaw = " + str(self.D.yaw) + ", D.error = " + str(self.D.error)
        self.Y.debug()
        print "steering " + str(self.steering)
        
        print "desired_distance = " + str(self.desired_distance) + ", distance = " + str(self.distance)  
        self.S.debug()
        print "speed = " + str(self.speed)
        
        self.M.debug()
        
        print "arc_displacement = " + str(self.arc_displacement), ", line_displacement = " + str(self.line_displacement)
    
    def run(self):
        print "Starting " + self.name
        
        while (True):
            
            new_steering = False
            new_speed = False
            
            if (self.D.updateAll() == True):
                self.last_yaw = self.yaw
                self.yaw = self.D.yaw_without_drift - self.mpu_yaw_offset
                
            else:
                print "ERROR: D returned false in Motion Thread"
                
            if (self.E.update() == True):
                self.last_distance = self.distance
                self.distance = self.E.distance
                
            else:
                print "ERROR: E returned false in Motion Thread"
            
            self.processAction()
            
            self.displacementManager()
            
            yaw_pid_input = angleMod(self.desired_yaw - self.yaw)
            
            if (self.Y.run(yaw_pid_input) == True):
                self.steering = self.Y.output
                new_steering = True
                
            else:
                print "ERROR: Y returned false in Motion Thread"
            
            
            if (self.S.run(self.distance) == True):
                self.speed = self.S.output
                new_speed = True
                
            else:
                print "ERROR: S returned false in Motion Thread"
            
            if (new_steering == True or new_speed == True):
                self.M.setDesiredSpeedAndSteering(self.speed, self.steering)
            else:
                print "ERROR: speed and steering not set in Motion Thread"
            
            time.sleep(self.time_period)
                
        print "Exiting " + self.name
