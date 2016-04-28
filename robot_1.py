#actions

#custom_ruggeduino

WHEEL_RADIUS = 0.04875 #0.04826 #0.05134
ENCODER_RESOLUTION = 96

#debug

#limits

#lut

#map

ZONE_0_INITIAL_CAMERA_LOCATION = {'x': 1, 'y': 7, 'z': 0.125 + 0.315, 'yaw': - 45 - 90, 'pitch': - 13.6, 'roll': 2, 'time': None}
ZONE_1_INITIAL_CAMERA_LOCATION = {'x': 7, 'y': 7, 'z': 0.125 + 0.315, 'yaw': - 135 - 90, 'pitch': - 13.6, 'roll': 2, 'time': None}
ZONE_2_INITIAL_CAMERA_LOCATION = {'x': 7, 'y': 1, 'z': 0.125 + 0.315, 'yaw': 135 - 90, 'pitch': - 13.6, 'roll': 2, 'time': None}
ZONE_3_INITIAL_CAMERA_LOCATION = {'x': 1, 'y': 1, 'z': 0.125 + 0.315, 'yaw': 45 - 90, 'pitch': - 13.6, 'roll': 2, 'time': None}

ROBOT_TO_CAMERA_VECTOR = {'alpha': 0, 'beta': 0, 'gamma': 0.372} #alpha forwards, beta left to right, gamma up 47.7 - 12.5 #0.315
ROBOT_TO_DEFAULT_CAMERA_YAW = - 90
ROBOT_TO_CAMERA_PITCH = - 13.6# -11 #deg
ROBOT_TO_CAMERA_ROLL = 2 #1.7 #deg

#map_thread

#method

APPROACH_LOCATION_INDENT = 0.75

ENEMY_ROBOT_RADIUS = 2.5 #meters
MAX_NUMBER_OF_ENEMY_IN_CUBE_RADIUS = 2 #inclusive (2 is ok)
MAX_NUMBER_OF_ENEMY_IN_APPROACH_RADIUS = 1 #inclusive (1 is ok)
MIN_ENEMY_DISTANCE_TO_CUBE = 0.75 #meters
MIN_ENEMY_DISTANCE_TO_APPROACH = 1 #meters

MOVING_SPEED = 1  #meter/sec
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
MAX_STEERING_ACCEL = 150 #units %/sec
MAX_SPEED_ACCEL = 200 #units %/sec
LINEAR_POWER_POINT = 20
MIN_LINEAR_POWER = 20

#multi

INITIAL_MPU_YAW_OFFSET = 9 #degrees   

WHEEL_BASE = 0.333 #meters

#noise

#pid

#polar

#positions

GRAB = 35

INITIALISATION = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 1}
ARMS_UP_OUT_THE_WAY = {'rotate': 0, 'lift': 100, 'grab': - 75, 'time': 1}
ARMS_UP_OUT_THE_WAY_WAIT = {'rotate': 0, 'lift': 100, 'grab': - 75, 'time': 2}
ARMS_CLOSED_PROTECTED = {'rotate': 0, 'lift': 100, 'grab': 40, 'time': 2}

ARMS_WIDE_ZERO = {'rotate': 0, 'lift': - 100, 'grab': - 70, 'time': 1}
ARMS_ON_CUBE_ZERO = {'rotate': 0, 'lift': - 100, 'grab': GRAB, 'time': 1}
LIFT_CUBE_ZERO = {'rotate': 60, 'lift': 0, 'grab': GRAB, 'time': 1}
RELEASE_CUBE_ZERO = {'rotate': 60, 'lift': 0, 'grab': -20, 'time': 0.5}

ARMS_WIDE_POSTIVE = {'rotate': - 100, 'lift': - 60, 'grab': - 70, 'time': 1}
ARMS_ON_CUBE_90 = {'rotate': - 100, 'lift': - 60, 'grab': GRAB, 'time': 1}
LIFT_CUBE_90 = {'rotate': - 100, 'lift': 80, 'grab': GRAB, 'time': 1}
TURN_CUBE_90 = {'rotate': 100, 'lift': 80, 'grab': GRAB, 'time': 2}
DOWN_CUBE_90 = {'rotate': 100, 'lift': -20, 'grab': GRAB, 'time': 1}
RELEASE_CUBE_90 = {'rotate': 100, 'lift': -20, 'grab': -20, 'time': 0.5}

ARMS_WIDE_NEGATIVE= {'rotate': 100, 'lift': - 50, 'grab': - 70, 'time': 1}
ARMS_ON_CUBE_NEGATIVE_90 = {'rotate': 100, 'lift': - 50, 'grab': GRAB, 'time': 1}
LIFT_CUBE_NEGATIVE_90 = {'rotate': 100, 'lift': 60, 'grab': GRAB, 'time': 1}
TURN_CUBE_NEGATIVE_90 = {'rotate': 10, 'lift': 60, 'grab': GRAB, 'time': 2}
DOWN_CUBE_NEGATIVE_90 = {'rotate': -80, 'lift': -10, 'grab': GRAB, 'time': 1}
RELEASE_CUBE_NEGATIVE_90 = {'rotate': -80, 'lift': -10, 'grab': -20, 'time': 0.5}

PREPARE_SECOND_ROTATE_180 = {'rotate': - 100, 'lift': - 60, 'grab': -20, 'time': 0.5}
ARMS_ON_CUBE_180_FAST = {'rotate': -100, 'lift': - 60, 'grab': GRAB, 'time': 0.5}

ARMS_ON_CUBE_NEGATIVE_180 = {'rotate': 100, 'lift': - 70, 'grab': GRAB, 'time': 2}
LIFT_CUBE_NEGATIVE_180 = {'rotate': 100, 'lift': 40, 'grab': GRAB, 'time': 2}
TURN_CUBE_NEGATIVE_180 = {'rotate': - 100, 'lift': 40, 'grab': GRAB, 'time': 2}
DOWN_CUBE_NEGATIVE_180 = {'rotate': - 100, 'lift': -35, 'grab': GRAB, 'time': 1}
RELEASE_CUBE_NEGATIVE_180 = {'rotate': - 100, 'lift': 0, 'grab': -20, 'time': 0.5}
PREPARE_SECOND_ROTATE_NEGATIVE_180 = {'rotate': 100, 'lift': - 40, 'grab': -20, 'time': 0.5}
ARMS_ON_CUBE_NEGATIVE_180_FAST = {'rotate': 100, 'lift': - 50, 'grab': GRAB, 'time': 0.5}

LIFT_TIME_INDENT = - 0.5

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


#servos

ARMS_SERVO_BOARD = 0

LEFT_ROTATE_PIN = 5
LEFT_ROTATE_DIRECTION = - 1
LEFT_ROTATE_OFFSET = 0

LEFT_LIFT_PIN = 4
LEFT_LIFT_DIRECTION = - 1
LEFT_LIFT_OFFSET = 0

LEFT_GRAB_PIN = 0
LEFT_GRAB_DIRECTION = - 1
LEFT_GRAB_OFFSET = - 7

RIGHT_ROTATE_PIN = 2
RIGHT_ROTATE_DIRECTION = 1
RIGHT_ROTATE_OFFSET = 0

RIGHT_LIFT_PIN = 1
RIGHT_LIFT_DIRECTION = 1
RIGHT_LIFT_OFFSET = 10
 
RIGHT_GRAB_PIN = 3
RIGHT_GRAB_DIRECTION = 1
RIGHT_GRAB_OFFSET = 0

#steady_thread
ADJUST = - 10 + 7 - 1 + 3

MAX_CAMERA_ANGLE = 184.47 + ADJUST #deg
MIN_CAMERA_ANGLE = - 6.97 + ADJUST #deg
CAMERA_TURN_RATE = 180 #output/sec
CAMERA_STABILISATION_TIME = 0.2 #sec

CAMERA_MEASUREMENTS = [[-6.97 + ADJUST, 0], [35.3 + ADJUST, 36], [74.22 + ADJUST, 72], [110.38 + ADJUST, 98], [147.81 + ADJUST, 134], [184.47 + ADJUST, 180]] #[[0, 0], [192, 180]]

#target

#turn

