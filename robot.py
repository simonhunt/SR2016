print "Main thread started"

DEBUG_YAW_DRIFT = False
DEBUG_TEST_DRIFT = 0
DEBUG_TIMEPERIOD = 5
DEBUG_SPEED = 0
DEBUG_STEERING = 20

YAW_DRIFT = 0.00417 #degrees per second 
YKP = 3
YKI = 2
YKD = 3
Y_I_LIMIT = 10
SKP = 250
SKI = 0
SKD = 0
S_I_LIMIT = 0
MAX_STEERING = 80
MAX_SPEED = 30
MIN_SPEED = 0

if (DEBUG_YAW_DRIFT == True):
    YAW_DRIFT = DEBUG_TEST_DRIFT
    MAX_STEERING = DEBUG_STEERING

from sr.robot import *
from limits import mapToLimits
from multi import STILL, TURN, MOVE_HOLD, MOVE
import time
import ruggeduino
import pid
import motors
import map
import multi


distance_setpoint = 0
yaw_setpoint = 0
speed = 0 
 
print "packages imported"

R = Robot.setup()
print "Robot.setup ran"

# Register the custom class with the Robot object
R.ruggeduino_set_handler_by_fwver("SRcustom", ruggeduino.MpuSonarEncoderRuggeduino)
print "Ruggeduino handler ran"

R.init()
print "R.init ran"

D = ruggeduino.MpuHandler(R.ruggeduinos[0], YAW_DRIFT)
print "MpuHandler initialised"

E = ruggeduino.EncoderHandler(R.ruggeduinos[0])
print "EncoderHandler initialised"

R.wait_start()
print "wait_start ran"

currentTime = time.time()
zone = R.zone
A = map.MapHandler(zone, currentTime)

Y = pid.PidController("YawPID", YKP, YKI, YKD, MAX_STEERING, - MAX_STEERING, yaw_setpoint, Y_I_LIMIT) #p, i, d, setpoint, iLimit, startingI
print "YawPID setup"

S = pid.PidController("DistancePID", SKP, SKI, SKD, MAX_SPEED, MIN_SPEED, distance_setpoint, S_I_LIMIT)
print "DistancePID setup"

M = motors.MotorHandler(R.motors[0].m0, R.motors[0].m1) #left motor, right motor
print "MotorHandler setup"

MotionThread = multi.MotionThread(D, Y, M, S, E)

MotionThread.start()
print "MotionThread started" 

def squareDemo():
    MotionThread.setAction(MOVE_HOLD, 0.5)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(TURN, 90)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(MOVE_HOLD, 0.5)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        
    MotionThread.setAction(TURN, 90)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(MOVE_HOLD, 0.5)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(TURN, 90)
        

    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        
    MotionThread.setAction(MOVE_HOLD, 0.5)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        
    MotionThread.setAction(TURN, 90)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(STILL)
    
def turnDemo():
    MotionThread.setAction(TURN, 10)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(TURN, -10)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(TURN, 45)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(TURN, -45)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        
    MotionThread.setAction(TURN, 90)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(TURN, -90)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(TURN, 180)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(TURN, -180)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
    
    MotionThread.setAction(STILL)
        
if (DEBUG_YAW_DRIFT == True):
    print "debugging yaw drift"
    MotionThread.setAction(STILL)
    wake_up_time = time.time()
    
    while (True):
        wake_up_time += DEBUG_TIMEPERIOD
        print str(MotionThread.yaw)
        sleep_time = mapToLimits(wake_up_time - time.time(), DEBUG_TIMEPERIOD, 0) 
        time.sleep(DEBUG_TIMEPERIOD)
        
i = 0
while (i < 10):
    i += 1
    time.sleep(1)
    MotionThread.debug()


#turnDemo()

while (True):
    time.sleep(1)
    MotionThread.debug()


#while True:
    
    
    #if (D.updateAll() == True):
    #    
    #    if (P.run(D.yawWithoutDrift) == True):
    #        steering = P.output
    #        
    #        if (S.setSpeedAndSteering(speed, steering) == True):
    #            print "yaw: ", D.yaw, " yaw without drift: ", D.yaw_without_drift, " pitch:", D.pitch, " roll: ", D.roll, " error: ", D.error, " speed: ", S.speed, " steering: ", S.steering
    #
    #if ((S.steering < 2) and (S.steering > -2)):
    #    current_time = time.time()
    #    markers = R.see( res=(1280,960) )         ## Takes a picture and analyses it at a resolution. For information on which resolutions can vbe used: https://www.studentrobotics.org/docs/programming/sr/vision/#ChoosingResolution
    #    print "I can see", len(markers), "markers:"       ## Prints out how many markers by taking the length of the markers array
    #    print " "       ##line clear
    #     
    #    M.update(markers, current_time, zone)
    #    M.filterCubes(current_time)
    #     
    #    print "camera location: ", M.camera_location
    #    print "a cube locations: ", M.a_cube_locations
    #    print "b cube locations: ", M.b_cube_locations
    #    print "c cube locations: ", M.c_cube_locations
    #    print "robot locations: ", M.robot_locations
    #    print " "       ##line clear
    
    #current_time = time.time()
    #markers = R.see( res=(1280,960) )         ## Takes a picture and analyses it at a resolution. For information on which resolutions can vbe used: https://www.studentrobotics.org/docs/programming/sr/vision/#ChoosingResolution
    #print "I can see", len(markers), "markers:"       ## Prints out how many markers by taking the length of the markers array
    #print " "       ##line clear
    #
    #M.update(markers, current_time, zone)
    #M.filterCubes(current_time)
    #print "aCubeLocations: ", M.a_cube_locations
    #print "bCubeLocations: ", M.b_cube_locations
    #print "cCubeLocations: ", M.c_cube_locations
         
    #print "Cameralocation: ", M.cameraLocation
    #print "aCubeLocations: ", M.aCubeLocations
    #print "bCubeLocations: ", M.bCubeLocations
    #print "cCubeLocations: ", M.cCubeLocations
    #print "robotLocations: ", M.robotLocations
    #print " "       ##line clear
    
print "Main thread exited"
        

        
