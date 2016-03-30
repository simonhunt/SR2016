import threading
import time
import math
from limits import angleMod, mapToLimits
from actions import *

MOVE_CHANGE = 5

SAMPLE_SIZE = 40
SAMPLE_TIMEPERIOD = 0.1 #seconds
MAX_YAW_SAMPLE_RANGE = 0.05 #degrees

INITIAL_MPU_YAW_OFFSET = 9 #degrees   
INITIAL_ROBOT_ACTION = STILL
INITIAL_ROBOT_ACTION_VALUE_1 = 0
INITIAL_ROBOT_ACTION_VALUE_2 = 0

DEFAULT_ROBOT_LOCATION = None

WHEEL_BASE = 0.45 #meters

class MotorHandlerPlaceholder():
    
    def setDesiredSpeedAndSteering(self, desired_speed, desired_steering):
        return False
    
    def debug(self):
        print "MotorHandler not passed to MotionThread yet"

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
    
    def __init__(self, MpuHandler, YawPid, DistancePid, EncoderHandler, time_period = 0.02): #50hz default
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
        self.robot_location = DEFAULT_ROBOT_LOCATION
        
        self.D = MpuHandler
        self.Y = YawPid
        self.S = DistancePid
        self.E = EncoderHandler
        self.M = MotorHandlerPlaceholder()
        
        self.time_period = time_period
        self.time_to_sleep = time_period
        
        self.mpu_yaw_offset = INITIAL_MPU_YAW_OFFSET
        
        self.action_lock = threading.Lock()
        self.action = INITIAL_ROBOT_ACTION
        self.action_value_1 = INITIAL_ROBOT_ACTION_VALUE_1
        self.action_value_2 = INITIAL_ROBOT_ACTION_VALUE_2
        self.action_needs_processing = True
        
    def setAction(self, action, action_value_1 = 0, action_value_2 = 0):
        
        with self.action_lock:
            self.action = action
            self.action_value_1 = action_value_1
            self.action_value_2 = action_value_2
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
                    self.desired_yaw = self.yaw + self.action_value_1
                    self.S.stop() 
                    print "New Action: TURN, with value = " + str(self.action_value_1)
                
                elif (self.action == TURN_CHANGE):
                    self.desired_yaw = self.yaw + self.action_value_1
                    print "New Action: TURN_CHANGE, with value = " + str(self.action_value_1)
                
                elif (self.action == TURN_TO):
                    self.Y.restart()
                    self.desired_yaw = self.action_value_1
                    self.S.stop() 
                    print "New Action: TURN_TO, with value = " + str(self.action_value_1)
                
                elif (self.action == TURN_TO_CHANGE):
                    self.desired_yaw = self.action_value_1
                    print "New Action: TURN_TO_CHANGE, with value = " + str(self.action_value_1)
                
                elif (self.action == MOVE):
                    self.Y.stop()
                    self.S.restart()
                    self.desired_distance = self.distance + self.action_value_1
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE, with value = " + str(self.action_value_1)
                    
                elif (self.action == MOVE_CHANGE):
                    self.desired_distance = self.distance + self.action_value_1
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE_CHANGE, with value = " + str(self.action_value_1)
                
                elif (self.action == MOVE_TO):
                    self.Y.stop()
                    self.S.restart()
                    self.desired_distance = self.action_value_1
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE_TO, with value = " + str(self.action_value_1)
                    
                elif (self.action == MOVE_TO_CHANGE):
                    self.desired_distance = self.action_value_1
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE_TO_CHANGE, with value = " + str(self.action_value_1)
                
                elif (self.action == MOVE_HOLD):
                    self.Y.restart()
                    self.desired_yaw = self.yaw
                    self.S.restart()
                    self.desired_distance = self.distance + self.action_value_1
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE_HOLD, with value = " + str(self.action_value_1)
                
                elif (self.action == MOVE_TO_HOLD):
                    self.Y.restart()
                    self.desired_yaw = self.yaw
                    self.S.restart()
                    self.desired_distance = self.action_value_1
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE_TO_HOLD, with value = " + str(self.action_value_1)
                
                elif (self.action == MOVE_AND_TURN_TO):
                    self.Y.restart()
                    self.desired_yaw = self.action_value_2
                    self.S.restart()
                    self.desired_distance = self.action_value_1
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE_AND_TURN_TO, with value_1 = " + str(self.action_value_1) + ", value_2 = " + str(self.action_value_2)
                
                elif (self.action == MOVE_AND_TURN_TO_CHANGE):
                    self.desired_yaw = self.action_value_2
                    self.desired_distance = self.action_value_1
                    self.S.setSetpoint(self.desired_distance)
                    print "New Action: MOVE_AND_TURN_TO_CHANGE, with value_1 = " + str(self.action_value_1) + ", value_2 = " + str(self.action_value_2)           
                    
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
            
    def updateRobotLocation(self):
        
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
    
    def updateSensors(self):
        self.updateDistance()
        self.updateYaw()
                
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
        distance_pid_input = self.distance
            
        if (self.S.run(distance_pid_input) == True):
            self.speed = self.S.output
            new_speed = True
            
        else:
            print "ERROR: S returned false in Motion Thread"
        return new_speed
        
    def updateMotors(self, new_steering, new_speed):
        
        if (new_steering == True or new_speed == True):
            
            if (self.M.setDesiredSpeedAndSteering(self.speed, self.steering) == False):
                print "ERROR: speed and steering not set in MotorHandler"
            
        else:
            print "ERROR: speed and steering not set in Motion Thread"
        
    def calibrationCheck(self):
        
        def check():
            yaws = ()
            distances = ()
            
            for x in range(0, SAMPLE_SIZE):
                self.updateYaw()
                self.updateDistance()
                yaws += (self.yaw,)
                distances += (self.distance,)
                time.sleep(SAMPLE_TIMEPERIOD)
                
            yaw_range = abs(angleMod(max(yaws) - min(yaws)))
            distance_range = max(distances) - min(distances)
            
            passed = True
            
            if (yaw_range < MAX_YAW_SAMPLE_RANGE):
                print "MPU calibration test passed with yaw_range = " + str(yaw_range)
            
            else: #range >= MAX_YAW_SAMPLE_RANGE
                print "MPU calibration test failed with yaw_range = " + str(yaw_range) + ", yaws = " + str(yaws)
                passed = False
                
            if (distance_range == 0):
                print "encoder calibration test passed"
            
            else: #distance_range != 0
                print "encoder calibration test failed with distance_range = " + str(distance_range) + ", distances = " + str(distances)
                passed = False
            return passed
        
        print "Running MPU and encoder calibration check..."
        attempts = 1
        
        while (check() == False):
            print "Test failed, trying again attempts = " +str(attempts)
            attempts += 1
            
        print "Test passed with attempts = " +str(attempts)
        
    def prepareForStart(self, MotorHandler): #def prepareForStart(self, MotorHandler, start_robot_location):
        self.M = MotorHandler
        self.updateSensors() # freshen up sensor readings so that offsets can be set correctly
        
    def run(self):
        print "Starting " + self.name
        wake_up_time = time.time() + self.time_period

        while (True):     
            self.time_to_sleep = mapToLimits(wake_up_time - time.time(), self.time_period, 0)
            wake_up_time += self.time_period
            time.sleep(self.time_to_sleep)
            
            self.updateSensors()               
            self.updateRobotLocation()
            self.processAction()               
            new_steering = self.runYawPid()
            new_speed = self.runDistancePid()           
            self.updateMotors(new_steering, new_speed)              
            
            
        print "Exiting " + self.name
    
    def debug(self):
        print self.name + ", time_to_sleep = " + str(self.time_to_sleep)
        
        print "desired_yaw = " + str(self.desired_yaw) + ", yaw = " + str(self.yaw) + ", D.yaw = " + str(self.D.yaw) + ", D.error = " + str(self.D.error)
        self.Y.debug()
        print "steering " + str(self.steering)
        
        print "desired_distance = " + str(self.desired_distance) + ", distance = " + str(self.distance)  
        self.S.debug()
        print "speed = " + str(self.speed)
        
        self.M.debug()
        
        print "robot_location = " + str(self.robot_location)
