import threading
import time
import math
from limits import angleMod

STILL = 0
TURN = 1
MOVE_HOLD = 2
MOVE = 3
INITIAL_MPU_YAW_OFFSET = 9
INITIAL_ROBOT_ACTION = STILL

WHEEL_BASE = 0.45 #meters

def robotDisplacementByArcApproximation(length, theta_1, theta_2):
    theta_1 = math.radians(theta_1) #convert angles into radians
    theta_2 = math.radians(theta_2)
    dtheta = theta_2 - theta_1
    radius = (length / dtheta) + (WHEEL_BASE / 2)
    dx = radius * (math.sin(theta_2) - math.sin(theta_1))
    dy = radius * (math.cos(theta_1) - math.cos(theta_2))
    return {'x': dx, 'y': dy}

def wheelDisplacementByLineApproximation(length, theta_1, theta_2):
    theta_1 = math.radians(theta_1) #convert angles into radians
    theta_2 = math.radians(theta_2)
    average_theta = (theta_1 + theta_2) / 2
    dx = length * math.cos(average_theta)
    dy = length * math.sin(average_theta)
    return {'x': dx, 'y': dy}

class MotionThread(threading.Thread):
    
    def __init__(self, initial_robot_location, MpuHandler, YawPid, DistancePid, EncoderHandler, time_period = 0.01):
        
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
        
        self.location_update_lock = threading.Lock()
        self.robot_location = initial_robot_location
        
        self.D = MpuHandler
        self.Y = YawPid
        self.S = DistancePid
        self.E = EncoderHandler
        
        self.time_period = time_period
        
        self.mpu_yaw_offset = INITIAL_MPU_YAW_OFFSET
        
        self.action_lock = threading.Lock()
        self.action = INITIAL_ROBOT_ACTION
        self.action_value = 0
        self.action_needs_processing = True
        
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
                
    def setRobotLocation(self, robot_location):
        
        with self.location_update_lock:
            self.robot_location = robot_location
            self.last_distance = self.distance
            self.mpu_yaw_offset += self.yaw - self.robot_location['yaw']
            self.yaw = self.robot_location['yaw']
            self.last_yaw = self.yaw
                    
    def locationChangeManager(self):
        
        with self.location_update_lock:
            theta_1 = self.last_yaw        
            theta_2 = self.yaw
            length = self.distance - self.last_distance
            
            if (theta_2 == theta_1): #error case for arc length /0 err
                displacement = wheelDisplacementByLineApproximation(length, theta_1, theta_2)
                
            else:
                displacement = robotDisplacementByArcApproximation(length, theta_1, theta_2)
            
            self.robot_location['x'] += displacement['x']
            self.robot_location['y'] += displacement['y']
            self.robot_location['yaw'] = self.yaw
            #self.robot_location['pitch'] = self.pitch
            #self.robot_location['roll'] = self.roll
                
            self.last_yaw = self.yaw
            self.last_distance = self.distance
        
    def updateYaw(self):
        
        if (self.D.updateAll() == True):
                
            with self.location_update_lock:
                self.yaw = self.D.yaw_without_drift - self.mpu_yaw_offset
              
        else: #self.D.update() == False
            print "ERROR: D returned false in Motion Thread"
    
    def updateDistance(self):
        
        if (self.E.update() == True):
            
            with self.location_update_lock:
                self.distance = self.E.distance
        
        else: #self.E.update() == False
                print "ERROR: E returned false in Motion Thread"
                
    def runYawPid(self):
        new_steering = False
        yaw_pid_input = angleMod(self.desired_yaw - self.yaw)
            
            if (self.Y.run(yaw_pid_input) == True):
                self.steering = self.Y.output
                new_steering = True
                
            else:
                print "ERROR: Y returned false in Motion Thread"
        return new_steering
    
    def runDistancePid(self):
        new_speed = False
        disptance_pid_input = self.distance
            
            if (self.S.run(distance_pid_input) == True):
                self.speed = self.S.output
                new_speed = True
                
            else:
                print "ERROR: S returned false in Motion Thread"
        return new_speed
        
    
    def run(self, MotorHandler):
        self.M = MotorHandler
        print "Starting " + self.name
        
        while (True):        
            
            self.processAction()
            
            self.updateYaw()
                
            self.updateDistance()
                
            self.locationChangeManager()
                
            new_steering = self.runYawPid()
            
            new_speed = self.runDistancePid()
            
                
            if (new_steering == True or new_speed == True):
                self.M.setDesiredSpeedAndSteering(self.speed, self.steering)
            else:
                print "ERROR: speed and steering not set in Motion Thread"
                
            time.sleep(self.time_period)
            
        print "Exiting " + self.name
    
    def debug(self):
        print self.name
        
        print "desired_yaw = " + str(self.desired_yaw) + ", yaw = " + str(self.yaw) + ", D.yaw = " + str(self.D.yaw) + ", D.error = " + str(self.D.error)
        self.Y.debug()
        print "steering " + str(self.steering)
        
        print "desired_distance = " + str(self.desired_distance) + ", distance = " + str(self.distance)  
        self.S.debug()
        print "speed = " + str(self.speed)
        
        self.M.debug()
        
        print "robot_location = " + str(self.robot_location)
