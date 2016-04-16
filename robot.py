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
MAX_SPEED = 80
MIN_SPEED = 0

if (DEBUG_YAW_DRIFT == True):
    YAW_DRIFT = DEBUG_TEST_DRIFT
    MAX_STEERING = DEBUG_STEERING

from sr.robot import *

from limits import mapToLimits

from actions import *
from positions import *

import time
import ruggeduino
import pid
import motors
import map
import multi
import map_thread
import debug
import target
import servos
import power
import method

test_target = {'x': 1, 'y': 0, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0}

origin = {'x': 0, 'y': 0, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0}

test_target_1 = {'x': 1, 'y': 0, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0}

test_target_2 = {'x': 1, 'y': 1, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0}

test_target_3 = {'x': 0, 'y': 1, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0}
 
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

# Setup Servo Thread
ServoThread = servos.ServoThread(R.servos)
print "ServoThread setup"

# Setup Motion Thread
MotionThread = multi.MotionThread(D, Y, S, E)
print "MotionThread setup"

MotionThread.calibrationCheck()

# Setup Map Thread
MapThread = map_thread.MapThread()
print "MapThread setup"

# Setup Target Thread
TargetThread = target.TargetThread(MotionThread)
print "TargetThread setup"

# Setup Debug Thread
DebugThread = debug.DebugThread((MotionThread, MapThread, TargetThread, ServoThread))
print "DebugThread setup"

#Signal that the start button is ready to be pressed by making a sound
power.signalReady(R.power)
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

#Signal that the robot has successfully started!
power.signalGood(R.power)
print "signalGood ran"

#MotionThread.setAction(MOVE_AND_TURN_TO, 1, 0)




# Functions
        
# if (DEBUG_YAW_DRIFT == True):
#     print "debugging yaw drift"
#     MotionThread.setAction(STILL)
#     wake_up_time = time.time()
    
#     while (True):
#         wake_up_time += DEBUG_TIMEPERIOD
#         print str(MotionThread.yaw)
#         sleep_time = mapToLimits(wake_up_time - time.time(), DEBUG_TIMEPERIOD, 0) 
#         time.sleep(DEBUG_TIMEPERIOD)

while (True):
    ServosThread.addPosition(ARMS_WIDE_90)
    time.sleep(5)
    ServosThread.addPosition(ARMS_ON_CUBE_90)
    time.sleep(5)
    ServosThread.addPosition(LIFT_CUBE_90)
    time.sleep(5)
    ServosThread.addPosition(TURN_CUBE_90)
    time.sleep(5)
    ServosThread.addPosition(DOWN_CUBE_90)
    time.sleep(10)

# TargetThread.addTarget(test_target_1)
# TargetThread.addTarget(test_target_2)
# TargetThread.addTarget(test_target_3)
# TargetThread.addTarget(origin)

ServoThread.setPosition(ARMS_WIDE_ZERO)

#TargetThread.addTarget(origin)




while (len(MapThread.a_cube_locations) == 0):
    time.sleep(1)
    
time.sleep(1)

while (True):
    
    if (len(MapThread.a_cube_locations) != 0):        
        cube_to_approach = method.decideCubeToApproach(MapThread.a_cube_locations, MapThread.b_cube_locations, MapThread.c_cube_locations) 
        break

TargetThread.addTarget(cube_to_approach['approach_location'])
power.signalActivity(R.power)

print "setting turn_location: " + str(cube_to_approach['approach_location'])

time.sleep(15)

MotionThread.setAction(TURN_TO, cube_to_approach['approach_location']['yaw'])
power.signalActivity(R.power)

time.sleep(15)


TargetThread.addTarget(cube_to_approach)
power.signalActivity(R.power)

print "setting cube_to_approach: " + str(cube_to_approach)

time.sleep(15)

if (cube_to_approach['approach_location']['degrees'] == 90):
    ServoThread.setSequence(TEST_SEQUENCE_90)

elif (cube_to_approach['approach_location']['degrees'] == - 90):
    ServoThread.setSequence(TEST_SEQUENCE_NEGATIVE_90)
    
elif (cube_to_approach['approach_location']['degrees'] == 0):
    ServoThread.setSequence(TEST_SEQUENCE_ZERO)

else: #  (cube_to_approach['approach_location']['degrees'] = 180)
    ServoThread.setSequence(TEST_SEQUENCE_180)
power.signalActivity(R.power)
    
print "turning with degrees = " + str(cube_to_approach['approach_location']['degrees'])
    
time.sleep(5)
TargetThread.addTarget(origin)
power.signalActivity(R.power)



#while (True):
#    ServoThread.addSequence(TEST_SEQUENCE_90)
#    time.sleep(20)
#    ServoThread.addSequence(TEST_SEQUENCE_NEGATIVE_90)
#    time.sleep(20)
#    ServoThread.addSequence(TEST_SEQUENCE_180)
#    time.sleep(30)

#TargetThread.setTarget(test_target)

        
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

        
