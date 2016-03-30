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
from multi import STILL, TURN, MOVE_HOLD, MOVE, TURN_CHANGE, MOVE_CHANGE
import time
import ruggeduino
import pid
import motors
import map
import multi
import map_thread
import debug

test_location = {'x': 100, 'y': 100, 'z': 100, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
 
print "packages imported"

R = Robot.setup()
print "Robot.setup ran"

# Register the custom class with the Robot object
R.ruggeduino_set_handler_by_fwver("SRcustom", ruggeduino.MpuSonarEncoderRuggeduino)
print "Ruggeduino handler ran"

R.init()
print "R.init ran"

# MPU Handler
D = ruggeduino.MpuHandler(R.ruggeduinos[0], YAW_DRIFT)
print "MpuHandler initialised"

# Encoder Handler
E = ruggeduino.EncoderHandler(R.ruggeduinos[0])
print "EncoderHandler initialised"

# Yaw PID
Y = pid.PidController("YawPID", YKP, YKI, YKD, MAX_STEERING, - MAX_STEERING, Y_I_LIMIT) #p, i, d, setpoint, iLimit, startingI
print "YawPID setup"

# Distance PID
S = pid.PidController("DistancePID", SKP, SKI, SKD, MAX_SPEED, MIN_SPEED, S_I_LIMIT)
print "DistancePID setup"

# Setup Motion Thread
MotionThread = multi.MotionThread(D, Y, S, E)
print "MotionThread setup"

MotionThread.calibrationCheck()

# Setup Map Thread
MapThread = map_thread.MapThread()
print "MapThread setup"

# Setup Debug Thread
DebugThread = debug.DebugThread((MotionThread, MapThread))
print "DebugThread setup"
    
# Wait for start button press
print "wait_start..."
R.wait_start()
print "wait_start returned"

# Initialise Core Processes

DebugThread.start()
print "DebugThread started"

M = motors.MotorHandler(R.motors[0].m0, R.motors[0].m1) #left motor, right motor
print "MotorHandler setup"

MotionThread.prepareForStart(M)
print "MotionThread prepared for start"

MapThread.prepareForStart(R.see, R.zone, MotionThread)
print "MapThread prepared for start"

MotionThread.start()
print "MotionThread started" 

MapThread.start()
print "MapThread started"

# Functions

def squareDemo():
    MotionThread.setAction(MOVE_HOLD, 1.5)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
    
    MotionThread.setAction(TURN, 90)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
    
    MotionThread.setAction(MOVE_HOLD, 1.5)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
        
    MotionThread.setAction(TURN, 90)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
    
    MotionThread.setAction(MOVE_HOLD, 1.5)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
    
    MotionThread.setAction(TURN, 90)
        

    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
        
    MotionThread.setAction(MOVE_HOLD, 1.5)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
        
    MotionThread.setAction(TURN, 90)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
    
    MotionThread.setAction(STILL)
    
def turnDemo():
    MotionThread.setAction(TURN, 10)
    
    i = 0
    while (i < 10):
        i += 1
        time.sleep(1)
        MotionThread.debug()
        MapThread.debug()
    
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
        
#i = 0
#while (i < 20):
#    i += 1
#    time.sleep(1)
#    MotionThread.debug()
#
#MotionThread.setRobotLocation(test_location)
#squareDemo()


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

rt = 1 #right hand top servo  (positive up)
rb = 0 #right hand bottom servo (positive is inwards)
lt = 4 #left hand top servo (positive is down)
lb = 3 #left hand bottom servo (positive is out)
lr = 5
rr = 2
angle = 0
pitch = 0

#R.servos[0][lt] = 20

def initialiseTurn(): #sets all servos to a starting point and sets some varibles allocated t thier angle however I have not et implicated any way of ensureing that this is the real angle as if the bt crashes it's arms may be turned without influecne from the porgram
    
    R.servos[0][lr] = 1
    R.servos[0][rr] = 1
    R.servos[0][lt] = -20
    R.servos[0][rt] = 20
    R.servos[0][lb] = 20
    R.servos[0][rb] = 20
    angle = 1
    pitch = 20
    time.sleep(2)

def setTurn(turn,res,delay,angle): #turn: angle you wish to turn to     res: resoloution fo turn, how much it turns each step     delay: how long to wiat between steps for the mtoro to finish turning and slow its movement   angle: the current angle of the servo
    
    while (angle < turn):
        angle = angle + res 
        R.servos[0][lr] = -angle
        R.servos[0][rr] = angle
        time.sleep(delay)
        
    while (angle > turn):
        angle = angle - res 
        R.servos[0][lr] = -angle
        R.servos[0][rr] = angle
        time.sleep(delay)
        
    return angle
    

def closeArms():
    
    R.servos[0][lb] = -19
    R.servos[0][rb] = 19
    
    return

def openArms():
    
    R.servos[0][lb] = 33
    R.servos[0][rb] = -33
    
    return

def holdArms(ang): #moves the arms in the smae way as open/close but to a specified angle
    
    R.servos[0][lb] = ang
    R.servos[0][rb] = -ang
    
    return

def liftArms(height,res,delay,pitch):
    
    
   while (pitch < height):
        pitch = pitch + res 
        R.servos[0][lt] = -pitch
        R.servos[0][rt] = pitch
        time.sleep(delay)
        
   while (pitch > height):
        pitch = pitch - res 
        R.servos[0][lt] = -pitch
        R.servos[0][rt] = pitch
        time.sleep(delay)
   
        
    
    
   return

while (True):
    
    angle = 0
    pitch = 20
    initialiseTurn()
    angle = setTurn(0,10,0.1,angle)
    time.sleep(0.5)
    liftArms(20,2.5,0.05,pitch)
    time.sleep(0.5)
    openArms()
    time.sleep(3)   
    closeArms()
    time.sleep(2)
    liftArms(100,2.5,0.05,pitch)
    time.sleep(1)
    angle = setTurn(80,10,0.1,angle)
    time.sleep(1)
    angle = setTurn(0,10,0.1,angle)
    time.sleep(1)
    openArms()
    liftArms(20,2.5,0.05,pitch)
    time.sleep(1)
        

        
