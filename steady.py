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
CAMERA_PAN_SEQUENCE = [0, 0.2, 0.6, 1, 0.8, 0.4]
CAMERA_MEASUREMENTS = [[-6.97, 0], [35.3, 0.2], [74.22, 0.4], [110.38, 0.6], [147.81, 0.8], [184.47, 180]] #[[0, 0], [192, 180]]
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
        self.steady_target = None
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
        time.sleep(0.5)
        self.moveCameraServo((MAX_CAMERA_ANGLE + MIN_CAMERA_ANGLE) / 2)
        time.sleep(0.5)
        self.moveCameraServo(MIN_CAMERA_ANGLE)
        time.sleep(0.5)
        
    def nextPan(self):
        self.steady_target = None
        self.next_pan = True
        
    def moveCameraServo(self, new_camera_angle):
        print "new_camera_angle = " + str(new_camera_angle)
        new_camera_angle = mapToLimits(new_camera_angle, MAX_CAMERA_ANGLE, MIN_CAMERA_ANGLE)
        #new_output = int(mapToLimits(((((new_camera_angle - MIN_CAMERA_ANGLE) / (MAX_CAMERA_ANGLE - MIN_CAMERA_ANGLE)) * (MAX_CAMERA_OUTPUT - MIN_CAMERA_OUTPUT)) + MIN_CAMERA_OUTPUT), MAX_CAMERA_OUTPUT, MIN_CAMERA_OUTPUT))
        
        print "new_camera_angle = " + str(new_camera_angle)
        new_output = self.getOutputFromAngle(new_camera_angle)
        print "new_output = " + str(new_output)
        
        change_in_output = abs(new_output - self.last_output)
        self.last_output = new_output
        print "new_output = " + str(new_output)
        self.ruggeduino.setCameraServoAngle(new_output)
        self.camera_angle = new_camera_angle
        return change_in_output
        
    def getOutputFromAngle(self, new_camera_angle):
        appropriate_lower_measurement_index = 0
        appropriate_upper_measurement_index = len(CAMERA_MEASUREMENTS) - 1
        
        lower_measurement_index = 0
        upper_measurement_index = 1
        
        while (upper_measurement_index < len(CAMERA_MEASUREMENTS)):
            
            if (new_camera_angle <= CAMERA_MEASUREMENTS[upper_measurement_index][0] and new_camera_angle >= CAMERA_MEASUREMENTS[lower_measurement_index][0]):
                appropriate_lower_measurement_index = lower_measurement_index
                appropriate_upper_measurement_index = upper_measurement_index
             
            lower_measurement_index += 1
            upper_measurement_index += 1
        
        print str(appropriate_lower_measurement_index)
        print str(appropriate_upper_measurement_index)
            
        lower_measurement_angle = CAMERA_MEASUREMENTS[appropriate_lower_measurement_index][0]
        upper_measurement_angle = CAMERA_MEASUREMENTS[appropriate_upper_measurement_index][0]
        lower_measurement_output = CAMERA_MEASUREMENTS[appropriate_lower_measurement_index][1]
        upper_measurement_output = CAMERA_MEASUREMENTS[appropriate_upper_measurement_index][1]
        
        print "lower_measurement_angle " + str(lower_measurement_angle)
        print "upper_measurement_angle " + str(upper_measurement_angle)
        print "lower_measurement_output " + str(lower_measurement_output)
        print "upper_measurement_output " + str(upper_measurement_output)
        
        gradient = (upper_measurement_output - lower_measurement_output) / (upper_measurement_angle - lower_measurement_angle)
        d_angle = (new_camera_angle - lower_measurement_angle)
        output = lower_measurement_output + (gradient * d_angle)
        
        print "gradient " + str(gradient)
        print "d_angle " + str(d_angle)
        print "output " + str(output)
        
        # output = (((new_camera_angle - lower_measurement_angle) / (upper_measurement_angle - lower_measurement_angle)) * (upper_measurement_output - lower_measurement_output)) + lower_measurement_output
        output = int(mapToLimits(output, MAX_CAMERA_OUTPUT, MIN_CAMERA_OUTPUT))
        
        return output
        
    def run(self):
        print "Starting " + self.name
        
        while (True):
            
            if (self.steady_target == None):
                self.panBehaviour()
                time.sleep(self.pan_time_period)
                
            elif (self.preparedForTargetting == True): # self.steady_target != None
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
        default_camera_location = cameraLocationFromRobotLocation(self.MotionThread.robot_location)
        
        desired_camera_yaw = getPolarT(default_camera_location, self.steady_target)
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
            print "steady_target = " + str(self.steady_target)
                    
        