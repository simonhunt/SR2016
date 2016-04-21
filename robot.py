print "Main thread started"

import time

import custom_ruggeduino
import pid
import motors
import map
import multi
import map_thread
import debug
import target
import servos
import noise
import method
import store

from limits import mapToLimits
from actions import *
from positions import *

from robot_1 import YAW_DRIFT, YKP, YKI, YKD, Y_I_LIMIT, SKP, SKI, SKD, S_I_LIMIT, MAX_STEERING, MAX_SPEED, MIN_SPEED

from sr.robot import *

DEBUG_YAW_DRIFT = False
DEBUG_TEST_DRIFT = 0
DEBUG_TIMEPERIOD = 5
DEBUG_SPEED = 0
DEBUG_STEERING = 0

# YAW_DRIFT = 0.00417 #degrees per second 
# YKP = 3
# YKI = 2
# YKD = 3
# Y_I_LIMIT = 10
# SKP = 250
# SKI = 0
# SKD = 0
# S_I_LIMIT = 0
# MAX_STEERING = 80
# MAX_SPEED = 80
# MIN_SPEED = 0

ORIGIN = {'x': 0, 'y': 0, 'z': 0}

if (DEBUG_YAW_DRIFT == True):
    YAW_DRIFT = DEBUG_TEST_DRIFT
    MAX_STEERING = DEBUG_STEERING

return_location_0 = {'x': 1, 'y': 7}
 
print "packages imported"

R = Robot.setup()
print "Robot.setup ran"

# Register the custom class with the Robot object
R.ruggeduino_set_handler_by_fwver("SRcustom", custom_ruggeduino.MpuSonarEncoderRuggeduino)
print "Ruggeduino handler ran"

R.init()
print "R.init ran"

# MPU Handler
D = custom_ruggeduino.MpuHandler(R.ruggeduinos[0], YAW_DRIFT)
print "MpuHandler initialised"

# Encoder Handler
E = custom_ruggeduino.EncoderHandler(R.ruggeduinos[0])
print "EncoderHandler initialised"

# Yaw PID
Y = pid.PidController("YawPID", YKP, YKI, YKD, MAX_STEERING, - MAX_STEERING, Y_I_LIMIT) #p, i, d, setpoint, iLimit, startingI
print "YawPID setup"

# Distance PID
S = pid.PidController("DistancePID", SKP, SKI, SKD, MAX_SPEED, MIN_SPEED, S_I_LIMIT)
print "DistancePID setup"

# Setup Servo Thread
ServoThread = servos.ServoThread(R.servos, R.power)
print "ServoThread setup"

# Setup Motion Thread
MotionThread = multi.MotionThread(R.power, D, Y, S, E)
print "MotionThread setup"

MotionThread.calibrationCheck()

# Setup Map Thread
MapThread = map_thread.MapThread(R.power)
print "MapThread setup"

# Setup Target Thread
TargetThread = target.TargetThread(MotionThread, R.power)
print "TargetThread setup"

# Setup Debug Thread
DebugThread = debug.DebugThread((MotionThread, MapThread, TargetThread, ServoThread))
print "DebugThread setup"

#Signal that the start button is ready to be pressed by making a sound
noise.signalReady(R.power)
print "signalReady ran"

# Wait for start button press
print "wait_start..."
R.wait_start()
print "wait_start returned"

# Initialise Core Processes

DebugThread.start()
print "DebugThread started"

M = motors.MotorHandler(R.motors)
print "MotorHandler setup"

MotionThread.prepareForStart(M)
print "MotionThread prepared for start"

MapThread.prepareForStart(R.see, R.zone, MotionThread)
print "MapThread prepared for start"

MotionThread.start()
print "MotionThread started" 

MapThread.start()
print "MapThread started"

TargetThread.start()
print "TargetThread started"

ServoThread.start()
print "ServoThread started"

StoreManager = store.StoreManager(R.zone)
print "StoreManager setup"

#Signal that the robot has successfully started!
noise.signalGood(R.power)
print "signalGood ran"

# Functions

def debugYawDrift():
    
    if (DEBUG_YAW_DRIFT == True):
        print "debugging yaw drift"
        MotionThread.setAction(STILL)
        wake_up_time = time.time()
    
        while (True):
            wake_up_time += DEBUG_TIMEPERIOD
            print str(MotionThread.yaw)
            sleep_time = mapToLimits(wake_up_time - time.time(), DEBUG_TIMEPERIOD, 0) 
            time.sleep(DEBUG_TIMEPERIOD)
            
def squareDemo():
    square_target_1 = {'x': 1, 'y': 0}
    square_target_2 = {'x': 1, 'y': 1}
    square_target_3 = {'x': 0, 'y': 1}
    TargetThread.addTarget(square_target_1)
    TargetThread.addTarget(square_target_2)
    TargetThread.addTarget(square_target_3)
    TargetThread.addTarget(ORIGIN)
    
def targetDemo():
    test_target_1 = {'x': 2, 'y': 7}
    TargetThread.addTarget(test_target_1)
    
def storeCubeDemo(cubes_stored = 0):
    store_target_1 = {'x': 2, 'y': 6}
    i = 0
    
    while (i <= cubes_stored):
        i += 1
        return_location = StoreManager.getReturnLocation()
        store_location = StoreManager.getStoreLocation()
    TargetThread.addTarget(store_target_1) 
    TargetThread.addTarget(return_location)
    TargetThread.addTarget(store_location)
    

def getCubeDemo():
    return_location = StoreManager.getReturnLocation()
    store_location = StoreManager.getStoreLocation()
    current_time = time.time()
    
    while ((len(MapThread.a_cube_locations) == 0) and (len(MapThread.b_cube_locations) == 0) and (len(MapThread.c_cube_locations) == 0)):
        time.sleep(1)
    
    while (True):
        
        if ((len(MapThread.a_cube_locations) != 0) or (len(MapThread.b_cube_locations) != 0) or (len(MapThread.c_cube_locations) != 0)):        
            cube_approach_path = method.decideCubeApproachPath(MapThread.a_cube_locations, MapThread.b_cube_locations, MapThread.c_cube_locations, return_location, MotionThread.robot_location, R.zone, MapThread.robot_locations, current_time) 
            break
    
    arm_phases = PHASES[cube_approach_path['approach_location']['degrees']]
    
    TargetThread.addTarget(cube_approach_path['approach_location'])
    noise.signalActivity(R.power)
    
    print "setting turn_location: " + str(cube_approach_path['approach_location'])

    TargetThread.addTarget(cube_approach_path['cube_location'])
    noise.signalActivity(R.power)
    
    print "setting cube_to_approach: " + str(cube_approach_path)
    
    while(TargetThread.target != cube_approach_path['cube_location']):
        time.sleep(0.1)
        
    while(TargetThread.target != None):
        time.sleep(0.1)
    
    arm_phases
    
    # if (cube_approach_path['approach_location']['degrees'] == 90):
    #     ServoThread.setSequence(TEST_SEQUENCE_90)
    
    # elif (cube_approach_path['approach_location']['degrees'] == - 90):
    #     ServoThread.setSequence(TEST_SEQUENCE_NEGATIVE_90)
        
    # elif (cube_approach_path['approach_location']['degrees'] == 0):
    #     ServoThread.setSequence(TEST_SEQUENCE_ZERO)
    
    # else: #  (cube_to_approach['approach_location']['degrees'] = 180)
    #     ServoThread.setSequence(TEST_SEQUENCE_180)
    noise.signalActivity(R.power)
    
    print "turning with degrees = " + str(cube_approach_path['approach_location']['degrees'])
    
    time.sleep(3)
    
    TargetThread.addTarget(return_location)
    TargetThread.addTarget(store_location)
    noise.signalActivity(R.power)

def testArms():
    while (True):
        ServoThread.addSequence(TEST_SEQUENCE_ZERO)
        time.sleep(10)
        ServoThread.addSequence(TEST_SEQUENCE_90)
        time.sleep(20)
        ServoThread.addSequence(TEST_SEQUENCE_NEGATIVE_90)
        time.sleep(20)
        ServoThread.addSequence(TEST_SEQUENCE_180)
        time.sleep(30)

time.sleep(5)

MotionThread.setAction(TURN_TO, - 45)

time.sleep(10)

noise.signalGood(R.power)

getCubeDemo()
    
print "Main thread exited"

        
