import threading
import time
 
import noise

from limits import mapToLimits
from debug import DEBUG_STEADYCAM

from robot_1 import MAX_CAMERA_ANGLE, MIN_CAMERA_ANGLE, CAMERA_TURN_RATE, CAMERA_STABILISATION_TIME

MAX_CAMERA_OUTPUT = 180
MIN_CAMERA_OUTPUT = 0
# MAX_CAMERA_ANGLE = 180 #deg
# MIN_CAMERA_ANGLE = 0 #deg
# CAMERA_TURN_RATE = 180 #output/sec
# CAMERA_STABILISATION_TIME = 0.1 #sec
CAMERA_PAN_SEQUENCE = [0.5, 0.75, 1, 0.75, 0.5, 0.25, 0, 0.25]
START_PAN_INDEX = 0

class SteadyThread(threading.Thread):
    
    def __init__(self, ruggeduino, power, steady_time_period = 0.01, pan_time_period = 0.1): #100hz, 10hz
        threading.Thread.__init__(self)
        self.name = "Steadycam"
        self.ruggeduino = ruggeduino
        self.power = power
        self.steady_time_period = steady_time_period
        self.pan_time_period = pan_time_period
        self.camera_angle = MIN_CAMERA_ANGLE
        self.last_output = 0
        self.steady_targets = None
        self.next_pan = False
        self.current_pan_index = START_PAN_INDEX
        self.camera_moving_lock = threading.Lock()
        
        self.setPan()
        
    def nextPan(self):
        self.steady_targets = None
        self.next_pan = True
        
    def moveCameraServo(self, new_camera_angle):
        new_camera_angle = mapToLimits(new_camera_angle, MIN_CAMERA_ANGLE, MAX_CAMERA_ANGLE)
        new_output = int(mapToLimits(((((new_camera_angle - MIN_CAMERA_ANGLE) / (MAX_CAMERA_ANGLE - MIN_CAMERA_ANGLE)) * (MAX_CAMERA_OUTPUT - MIN_CAMERA_OUTPUT)) + MIN_CAMERA_OUTPUT), MAX_CAMERA_OUTPUT, MIN_CAMERA_OUTPUT))
        change_in_output = abs(new_output - self.last_output)
        self.ruggeduino.setCameraServoAngle(new_output)
        self.camera_angle = new_camera_angle
        return change_in_output
    
    def run(self):
        print "Starting " + self.name
        
        while (True):
            
            if (self.steady_targets == None):
                self.panBehaviour()
                time.sleep(self.pan_time_period)
                
            else: # self.steady_targets != None
                self.steadyBehaviour()
                time.sleep(self.steady_time_period)
        
        print "Exiting " + self.name
        
    def panBehaviour(self):
        
        if (self.next_pan == True):
            
            self.next_pan = False
            self.pan_index = (self.current_pan_index + 1) % len(CAMERA_PAN_SEQUENCE)
            
            with self.camera_moving_lock:
                self.setPan()
            
    def setPan(self):
        pan_fraction = CAMERA_PAN_SEQUENCE[self.pan_index]
        new_camera_angle = ((MAX_CAMERA_ANGLE - MIN_CAMERA_ANGLE) * pan_fraction) + MIN_CAMERA_ANGLE
        change_in_output = self.moveCameraServo(new_camera_angle)
        time_to_sleep = (change_in_output / CAMERA_TURN_RATE) + CAMERA_STABILISATION_TIME
        time.sleep(time_to_sleep)
    
    def steadyBehaviour(self):
        pass
        
    def debug(self):
        
        if (DEBUG_STEADYCAM == True):
            
            print self.name
            
            print "camera_angle = " + str(self.camera_angle) + ", last_output = " + str(self.last_output)
            print "steady_targets = " + str(self.steady_targets)
                    
        