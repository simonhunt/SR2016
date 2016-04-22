import threading
import time
 
import noise

from limits import mapToLimits

from robot_1 import CAMERA_SERVO_BOARD, CAMERA_SERVO_PIN

#temp consts
MAX_CAMERA_OUTPUT = 0
MIN_CAMERA_OUTPUT = 180
MID_CAMERA_ANGLE = 6
MAX_CAMERA_ANGLE = 180 #deg
MIN_CAMERA_ANGLE = 0 #deg
CAMERA_TURN_RATE = 180 #deg/sec

class SteadycamThread(threading.Thread):
    
    def __init__(self, ruggeduino, power):        
        threading.Thread.__init__(self)
        self.name = "Steadycam"
        self.last_output = 0
        self.ruggeduino = ruggeduino
        self.camera_angle = MID_CAMERA_ANGLE
        self.power = power
        
        self.changeCameraAngle()
        self.changeCameraAngle()
        self.changeCameraAngle()
        self.changeCameraAngle()
        self.changeCameraAngle()
        self.changeCameraAngle()
        
    def changeCameraAngle(self):
        
        
        
        if (self.camera_angle == MID_CAMERA_ANGLE):
            self.servos[CAMERA_SERVO_BOARD][CAMERA_SERVO_PIN] = 100
            self.ruggeduino.setCameraServoAngle(180)
            time.sleep(0.5)
            self.camera_angle = MAX_CAMERA_ANGLE
            print "changed to 100"
        
        elif (self.camera_angle == MAX_CAMERA_ANGLE):
            self.servos[CAMERA_SERVO_BOARD][CAMERA_SERVO_PIN] = -100
            self.ruggeduino.setCameraServoAngle(0)
            time.sleep(1)
            self.camera_angle = MIN_CAMERA_ANGLE
            print "changed to -100"
        
        elif (self.camera_angle == MIN_CAMERA_ANGLE):
            self.servos[CAMERA_SERVO_BOARD][CAMERA_SERVO_PIN] = 0
            self.ruggeduino.setCameraServoAngle(90)
            time.sleep(0.5)
            self.camera_angle = MID_CAMERA_ANGLE
            print "changed to 0"
            
        
    def moveCameraServo(self, new_camera_angle):
        
        new_camera_angle = mapToLimits(new_camera_angle, MIN_CAMERA_ANGLE, MAX_CAMERA_ANGLE)]
        new_output = mapToLimits(((((new_camera_angle - MIN_CAMERA_ANGLE) / (MAX_CAMERA_ANGLE - MIN_CAMERA_ANGLE)) * (MAX_CAMERA_OUTPUT - MIN_CAMERA_OUTPUT)) + MIN_CAMERA_OUTPUT), MAX_CAMERA_OUTPUT, MIN_CAMERA_OUTPUT)
        self.ruggeduino.setCameraServoAngle(180)
        
    
    def run(self):
        print "Starting " + self.name
        
        while (True):
            
        
        print "Exiting " + self.name
        
    def debug(self):
        
        if (DEBUG_MAP == True):
            
            print self.name
            
            print "length of a_cube_locations = " + str(len(self.a_cube_locations))
            print "length of b_cube_locations = " + str(len(self.b_cube_locations))
            print "length of c_cube_locations = " + str(len(self.c_cube_locations))        
        