#actions

#debug

#limits

#lut

#map

ZONE_0_INITIAL_CAMERA_LOCATION = {'x': 1, 'y': 7, 'z': 0.125, 'yaw': -45, 'pitch': 0, 'roll': 0, 'time': None}
ZONE_1_INITIAL_CAMERA_LOCATION = {'x': 7, 'y': 7, 'z': 0.125, 'yaw': -135, 'pitch': 0, 'roll': 0, 'time': None}
ZONE_2_INITIAL_CAMERA_LOCATION = {'x': 7, 'y': 1, 'z': 0.125, 'yaw': 135, 'pitch': 0, 'roll': 0, 'time': None}
ZONE_3_INITIAL_CAMERA_LOCATION = {'x': 1, 'y': 1, 'z': 0.125, 'yaw': 45, 'pitch': 0, 'roll': 0, 'time': None}

ROBOT_TO_CAMERA_VECTOR = {'alpha': 0, 'beta': 0, 'gamma': 0} #alpha forwards, beta left to right, gamma up
ROBOT_TO_CAMERA_YAW = 0
ROBOT_TO_CAMERA_PITCH = 0# -11 #deg
ROBOT_TO_CAMERA_ROLL = 0 #1.7 #deg

#map_thread

APPROACH_LOCATION_INDENT = 0.75

ENEMY_ROBOT_RADIUS = 2.5 #meters
MAX_NUMBER_OF_ENEMY_IN_CUBE_RADIUS = 2 #inclusive (2 is ok)
MAX_NUMBER_OF_ENEMY_IN_APPROACH_RADIUS = 1 #inclusive (1 is ok)
MIN_ENEMY_DISTANCE_TO_CUBE = 0.75 #meters
MIN_ENEMY_DISTANCE_TO_APPROACH = 1 #meters

MOVING_SPEED = 1 #meter/sec
ANGULAR_SPEED = 90 #deg/sec

TURN_ZERO_TIME = 0.5 #sec
TURN_90_TIME = 1 #sec
TURN_180_TIME = 5 #sec
TURN_NEGATIVE_90_TIME = 1 #sec
TURN_TIMES = {0: TURN_ZERO_TIME, 90: TURN_90_TIME, 180: TURN_180_TIME, - 90: TURN_NEGATIVE_90_TIME}

#motors

MOTOR_BOARD = 0

MAX_STEERING = 160
MIN_STEERING = - 160
MAX_SPEED = 80
MIN_SPEED = - 80
MAX_OUTPUT = 100
MIN_OUTPUT = - 100
MAX_STEERING_ACCEL = 50 #units %/sec
MAX_SPEED_ACCEL = 100 #units %/sec
LINEAR_POWER_POINT = 20
MIN_LINEAR_POWER = 20

#multi

INITIAL_MPU_YAW_OFFSET = 9 #degrees   

WHEEL_BASE = 0.33 #meters

#pid

#polar

#robot

YAW_DRIFT = 0.00417 #degrees per second 
YKP = 3
YKI = 2
YKD = 3
Y_I_LIMIT = 10
SKP = 250
SKI = 0
SKD = 0
S_I_LIMIT = 0
#MAX_STEERING = 80
#MAX_SPEED = 80
#MIN_SPEED = 0

#ruggeduino

WHEEL_RADIUS = 0.04875 #0.04826 #0.05134
ENCODER_RESOLUTION = 96



