print "Main thread started"

import time
import copy

from sr.robot import *

import custom_ruggeduino
import pid
import motors
import map
import multi
import map_thread
import debug
import target
import servos
import positions
import noise
import method
import store
import steady

from limits import mapToLimits
from actions import *

from robot_1 import YAW_DRIFT, YKP, YKI, YKD, Y_I_LIMIT, SKP, SKI, SKD, S_I_LIMIT, MAX_STEERING, MAX_SPEED, MIN_SPEED, MAX_CUBE_SONAR_DISTANCE

DEBUG_YAW_DRIFT = False
DEBUG_TEST_DRIFT = 0
DEBUG_TIMEPERIOD = 5
DEBUG_SPEED = 0
DEBUG_STEERING = 0

DEFAULT_SONAR_TEST_LENGTH = 2 #seconds

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
THREEFIVE = {'x': 2.5, 'y': 5.5, 'z': 0}

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

# Setup Steadycam Thread
SteadycamThread = steady.SteadycamThread(R.ruggeduinos[0], R.power)
print "SteadycamThread setup"

# Setup Motion Thread
MotionThread = multi.MotionThread(R.power, D, Y, S, E)
print "MotionThread setup"

MotionThread.calibrationCheck()

# Setup Map Thread
MapThread = map_thread.MapThread(SteadycamThread, R.power)
print "MapThread setup"

# Setup Target Thread
TargetThread = target.TargetThread(MotionThread, R.power)
print "TargetThread setup"

# Setup Debug Thread
DebugThread = debug.DebugThread((MotionThread, MapThread, TargetThread, ServoThread, SteadycamThread))
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

SteadycamThread.start()
print "SteadycamThread started"

M = motors.MotorHandler(R.motors)
print "MotorHandler setup"

MotionThread.prepareForStart(M)
print "MotionThread prepared for start"

MapThread.prepareForStart(R.see, R.zone, MotionThread)
print "MapThread prepared for start"

SteadycamThread.prepareForTargetting(MotionThread)
print "MapThread prepared for targetting"

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
    

def getToCube():
    next_cube_location = StoreManager.next_cube_location
    return_location = StoreManager.getReturnLocation()
    store_location = StoreManager.getStoreLocation()
    current_time = time.time()
    
    while ((len(MapThread.a_cube_locations) == 0) and (len(MapThread.b_cube_locations) == 0) and (len(MapThread.c_cube_locations) == 0)):
        time.sleep(1)
    
    while (True):
        
        if ((len(MapThread.a_cube_locations) != 0) or (len(MapThread.b_cube_locations) != 0) or (len(MapThread.c_cube_locations) != 0)):        
            cube_approach_path = method.decideCubeApproachPath(MapThread.a_cube_locations, MapThread.b_cube_locations, MapThread.c_cube_locations, return_location, MotionThread.robot_location, R.zone, MapThread.robot_locations, current_time) 
            break
    
    arm_phases = positions.PHASES[cube_approach_path['approach_location']['degrees']]
    lift_time = positions.LIFT_TIMES[cube_approach_path['approach_location']['degrees']]
    down_time = positions.DOWN_TIMES[cube_approach_path['approach_location']['degrees']]
    
    MapThread.setTargetedCube(cube_approach_path)
    print "setting targetted_cube: " + str(cube_approach_path)
    
    TargetThread.setTarget(cube_approach_path['approach_location'])
    
    print "setting turn_location: " + str(cube_approach_path['approach_location'])

    TargetThread.addTarget(cube_approach_path['cube_location'])
    
    print "adding cube_to_approach: " + str(cube_approach_path)
    
    while(TargetThread.target != cube_approach_path['cube_location']):
        time.sleep(0.1)
        
    ServoThread.setSequence(arm_phases[0])
        
    while(TargetThread.target != None):
        
        if (MapThread.updated_targeted_cube == True):
            MapThread.updated_targeted_cube = False
            TargetThread.changeCurrentTarget(copy.deepcopy(MapThread.targeted_cube['cube_location']))
            print "changing current target: " + str(MapThread.targeted_cube['cube_location'])
            noise.signalActivity(R.power)
            noise.signalActivity(R.power)
            noise.signalActivity(R.power)
            
        else:
            time.sleep(0.1)
            
    MapThread.removeTargetedCube()
            
    if (sonarTest() == True):
        storeCube()

def storeCube():
    
    time.sleep(2)
    
    print "removing targetted_cube"
    
    ServoThread.setSequence(arm_phases[1])
    ServoThread.addSequence(arm_phases[2])  
    print "turning with degrees = " + str(cube_approach_path['approach_location']['degrees'])
    time.sleep(lift_time)
    
    TargetThread.setTarget(return_location)
    print "setting return_location: " + str(return_location)
    
    TargetThread.addTarget(store_location)
    print "adding store_location: " + str(store_location)
    
    while(TargetThread.target != store_location):
        time.sleep(0.1)
    
    ServoThread.setSequence(arm_phases[3])
    ServoThread.addSequence(arm_phases[4])
    
    time.sleep(down_time)
    
    while(TargetThread.target != None):
        time.sleep(0.1)
    
    MotionThread.setAction(MOVE, - 1)
    time.sleep(3)
    TargetThread.setTarget(next_cube_location)
    time.sleep(5)

def testArms():
    
    while (True):
        ServoThread.addSequence(positions.TEST_SEQUENCE_ZERO)
        time.sleep(10)
        ServoThread.addSequence(positions.TEST_SEQUENCE_90)
        time.sleep(20)
        ServoThread.addSequence(positions.TEST_SEQUENCE_NEGATIVE_90)
        time.sleep(20)
        ServoThread.addSequence(positions.TEST_SEQUENCE_180)
        time.sleep(30)
        
def steadyTest():
    return_location = StoreManager.getReturnLocation()
    store_location = StoreManager.getStoreLocation()
    current_time = time.time()
    
    while ((len(MapThread.a_cube_locations) == 0) and (len(MapThread.b_cube_locations) == 0) and (len(MapThread.c_cube_locations) == 0)):
        time.sleep(1)
    
    while (True):
        
        if ((len(MapThread.a_cube_locations) != 0) or (len(MapThread.b_cube_locations) != 0) or (len(MapThread.c_cube_locations) != 0)):        
            cube_approach_path = method.decideCubeApproachPath(MapThread.a_cube_locations, MapThread.b_cube_locations, MapThread.c_cube_locations, return_location, MotionThread.robot_location, R.zone, MapThread.robot_locations, current_time) 
            break
    
    arm_phases = positions.PHASES[cube_approach_path['approach_location']['degrees']]
    
    MapThread.setTargetedCube(cube_approach_path)
    print "setting targetted_cube: " + str(cube_approach_path)
    
    time.sleep(20)
    
    cube_target = copy.deepcopy(MapThread.targeted_cube['cube_location'])
    
    TargetThread.setTarget(cube_target)
    
    ServoThread.setSequence(arm_phases[0])
    
    while(TargetThread.target != cube_target):
        time.sleep (0.1)
    
    while(TargetThread.target != None):
        
        print "UPDATED"
        
        if (MapThread.updated_targeted_cube == True):
            MapThread.updated_targeted_cube = False
            TargetThread.changeCurrentTarget(copy.deepcopy(MapThread.targeted_cube['cube_location']))
            print "changing current target: " + str(MapThread.targeted_cube['cube_location'])
            noise.signalActivity(R.power)
            noise.signalActivity(R.power)
            noise.signalActivity(R.power)
            
        time.sleep(0.1)
        
def sonarTest(test_start_time = time.time(), test_length = DEFAULT_SONAR_TEST_LENGTH):
    
    test_passed = False
    
    while(time.time() < (test_start_time - test_length)):
        test_passed = sonarCheckCube()
        
        if (test_passed == True):
            break
        
    return test_passed
        
        
def sonarCheckCube():
    
    cube_is_in_reach = False
    
    if (R.ruggeduinos[0].sonar() <= MAX_CUBE_SONAR_DISTANCE):
        
        if (R.ruggeduinos[0].sonar() <= MAX_CUBE_SONAR_DISTANCE):
            
            if (R.ruggeduinos[0].sonar() <= MAX_CUBE_SONAR_DISTANCE):
                cube_is_in_reach = True
         
    return cube_is_in_reach
        
        
        

    
time.sleep(5)


noise.signalGood(R.power)

getCubeDemo()

time.sleep(5)

noise.signalGood(R.power)

getCubeDemo()

time.sleep(5)

noise.signalGood(R.power)

getCubeDemo()

time.sleep(5)

noise.signalGood(R.power)

getCubeDemo()

time.sleep(5)

noise.signalGood(R.power)

getCubeDemo()

time.sleep(5)

print "Main thread exited"

        
