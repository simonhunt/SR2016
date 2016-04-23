import threading
import time
 
import noise

from limits import angleMod, mapToLimits
from debug import DEBUG_STEADYCAM
from map import cameraLocationFromRobotLocation
from polar import *

from robot_1 import MAX_CAMERA_ANGLE, MIN_CAMERA_ANGLE, CAMERA_TURN_RATE, CAMERA_STABILISATION_TIME, ROBOT_TO_DEFAULT_CAMERA_YAW

MAX_CAMERA_OUTPUT = 180
MIN_CAMERA_OUTPUT = 0
# MAX_CAMERA_ANGLE = 180 #deg
# MIN_CAMERA_ANGLE = 0 #deg
# CAMERA_TURN_RATE = 180 #output/sec
# CAMERA_STABILISATION_TIME = 0.1 #sec
CAMERA_PAN_SEQUENCE = [0, 0.25, 0.5, 0.75, 1, 0.75, 0.5, 0.25]
START_PAN_INDEX = 0

TEST_TARGET = {'x': 0, 'y': 7}

class SteadycamThread(threading.Thread):
    
    def __init__(self, ruggeduino, power, steady_time_period = 0.01, pan_time_period = 0.1): #100hz, 10hz
        threading.Thread.__init__(self)
        self.name = "Steadycam"
        self.ruggeduino = ruggeduino
        self.power = power
        self.steady_time_period = steady_time_period
        self.pan_time_period = pan_time_period
        self.camera_angle = MIN_CAMERA_ANGLE
        self.last_output = 0
        self.steady_targets = []
        self.next_pan = False
        self.pan_index = START_PAN_INDEX
        self.camera_moving_lock = threading.Lock()
        self.preparedForTargetting = False
        
        self.testServo()
        
        self.setPan()
        
    def prepareForTargetting(self, MotionThread):
        self.MotionThread = MotionThread
        self.preparedForTargetting = True
        
    def testServo(self):
        self.moveCameraServo(MAX_CAMERA_ANGLE)
        time.sleep(1)
        self.moveCameraServo(MIN_CAMERA_ANGLE)
        time.sleep(1)
        
    def nextPan(self):
        self.steady_target = None
        self.next_pan = True
        
    def moveCameraServo(self, new_camera_angle):
        new_camera_angle = mapToLimits(new_camera_angle, MAX_CAMERA_ANGLE, MIN_CAMERA_ANGLE)
        new_output = int(mapToLimits(((((new_camera_angle - MIN_CAMERA_ANGLE) / (MAX_CAMERA_ANGLE - MIN_CAMERA_ANGLE)) * (MAX_CAMERA_OUTPUT - MIN_CAMERA_OUTPUT)) + MIN_CAMERA_OUTPUT), MAX_CAMERA_OUTPUT, MIN_CAMERA_OUTPUT))
        new_output = mapToLimits(((((new_camera_angle - MIN_CAMERA_ANGLE) / (MAX_CAMERA_ANGLE - MIN_CAMERA_ANGLE)) * (MAX_CAMERA_OUTPUT - MIN_CAMERA_OUTPUT)) + MIN_CAMERA_OUTPUT), MAX_CAMERA_OUTPUT, MIN_CAMERA_OUTPUT)
        new_output = int(new_output)
        
        change_in_output = abs(new_output - self.last_output)
        self.last_output = new_output
        self.ruggeduino.setCameraServoAngle(new_output)
        self.camera_angle = new_camera_angle
        return change_in_output
    
    def run(self):
        print "Starting " + self.name
        
        while (True):
            
            if (len(self.steady_targets) == 0):
                self.panBehaviour()
                time.sleep(self.pan_time_period)
                
            elif (self.preparedForTargetting == True): # len(self.steady_targets) != 0
                self.steadyBehaviour()
                time.sleep(self.steady_time_period)
        
        print "Exiting " + self.name
        
    def panBehaviour(self):
        
        if (self.next_pan == True):
            
            self.next_pan = False
            self.pan_index = (self.pan_index + 1) % len(CAMERA_PAN_SEQUENCE)
            
            with self.camera_moving_lock:
                self.setPan()
            
    def setPan(self):
        pan_fraction = CAMERA_PAN_SEQUENCE[self.pan_index]
        print str(pan_fraction)
        new_camera_angle = ((MAX_CAMERA_ANGLE - MIN_CAMERA_ANGLE) * pan_fraction) + MIN_CAMERA_ANGLE
        print str(new_camera_angle)
        change_in_output = self.moveCameraServo(new_camera_angle)
        time_to_sleep = (change_in_output / CAMERA_TURN_RATE) + CAMERA_STABILISATION_TIME
        time.sleep(time_to_sleep)
    
    def steadyBehaviour(self):
        selected_target = TEST_TARGET
        default_camera_location = cameraLocationFromRobotLocation(self.MotionThread.robot_location, ROBOT_TO_DEFAULT_CAMERA_YAW)
        desired_camera_yaw = getPolarT(default_camera_location, selected_target)
        desired_camera_angle = angleMod(desired_camera_yaw - default_camera_location['yaw'])
        
        if ((desired_camera_angle > MAX_CAMERA_ANGLE) or (desired_camera_angle < MIN_CAMERA_ANGLE)):
            angle_to_max = angleMod(desired_camera_angle - MAX_CAMERA_ANGLE)
            angle_to_min = angleMod(desired_camera_angle - MIN_CAMERA_ANGLE)
            
            if (abs(angle_to_max) > abs(angle_to_min)):
                desired_camera_angle = MIN_CAMERA_ANGLE
                
            else: #abs(angle_to_max) <= abs(angle_to_min)
                desired_camera_angle = MAX_CAMERA_ANGLE
        
        self.moveCameraServo(desired_camera_angle)
        
        
    def debug(self):
        
        if (DEBUG_STEADYCAM == True):
            
            print self.name
            
            print "camera_angle = " + str(self.camera_angle) + ", last_output = " + str(self.last_output)
            print "steady_targets = " + str(self.steady_targets)
                    
        