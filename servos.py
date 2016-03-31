import threading
from limits import mapToLimits

SERVO_BOARD = 0

LEFT_ROTATE_PIN = 5
LEFT_ROTATE_DIRECTION = -1
LEFT_ROTATE_OFFSET = 0

LEFT_LIFT_PIN = 4
LEFT_LIFT_DIRECTION = -1
LEFT_LIFT_OFFSET = 0

LEFT_GRAB_PIN = 0
LEFT_GRAB_DIRECTION = -1
LEFT_GRAB_OFFSET = 0

RIGHT_ROTATE_PIN = 2
RIGHT_ROTATE_DIRECTION = 1
RIGHT_ROTATE_OFFSET = 0

RIGHT_LIFT_PIN = 1
RIGHT_LIFT_DIRECTION = 1
RIGHT_LIFT_OFFSET = 0
 
RIGHT_GRAB_PIN = 3
RIGHT_GRAB_DIRECTION = 1
RIGHT_GRAB_OFFSET = 0

#POSITIONS

INITIALISATION = {'rotate': 0, 'lift': 0, 'grab': 0}
ARMS_U

class ServosThread(threading.Thread):
    
    def __init__(self, servos, position_timeperiod = 0.1, move_timeperiod = 0.01): # default 10hz postition, 100hz move    
        threading.Thread.__init__(self)
        self.name = "ServosThread"
        self.servos = servos 
        self.postition_timeperiod = position_timeperiod
        self.move_timeperiod = move_timeperiod
        self.position = INITIALISATION
        self.initialiseOffsets()
        
    def moveTo(self, new_positions, move_time = 1):
        drotate = new_position['rotate'] - self.position['rotate']
        dlift = new_position['lift'] - self.position['lift']
        dgrab = new_position['grab'] - self.position['grab']
        rotate_increment = drotate * self.move_timeperiod / move_time
        
    def initialiseOffsets(self):
        self.setRotate(0)
        self.setLift(0)
        self.setGrab(0)
    
    def setRotate(self, rotate):
        self.position['rotate'] = rotate
        self.servos[SERVO_BOARD][LEFT_ROTATE_PIN] = mapToLimits((self.rotate + LEFT_ROTATE_OFFSET)  * LEFT_ROTATE_DIRECTION)
        self.servos[SERVO_BOARD][RIGHT_ROTATE_PIN] = mapToLimits((self.rotate + RIGHT_ROTATE_OFFSET) * RIGHT_ROTATE_DIRECTION)
    
    def setLift(self, lift):
        self.position['lift'] = lift
        self.servos[SERVO_BOARD][LEFT_LIFT_PIN] = mapToLimits((self.lift + LEFT_LIFT_OFFSET)  * LEFT_LIFT_DIRECTION)
        self.servos[SERVO_BOARD][RIGHT_LIFT_PIN] = mapToLimits((self.lift + RIGHT_LIFT_OFFSET) * RIGHT_LIFT_DIRECTION)
        
    def setGrab(self, grab):
        self.position['grab'] = grab
        self.servos[SERVO_BOARD][LEFT_GRAB_PIN] = mapToLimits((self.grab + LEFT_GRAB_OFFSET)  * LEFT_GRAB_DIRECTION)
        self.servos[SERVO_BOARD][RIGHT_GRAB_PIN] = mapToLimits((self.grab + RIGHT_GRAB_OFFSET) * RIGHT_GRAB_DIRECTION)
    
    def run(self):
        print "Starting " + self.name
        print "Exiting " + self.name

from sr.robot import *
import time

lr = 5 #back is positive
rr = 2 #forth is positive
lt = 4 #left hand top servo (positive is down)
rt = 1 #right hand top servo  (positive up)
lb = 0 #right hand bottom servo (positive is out)
rb = 3 #left hand bottom servo (positive is in)


R.servos[0][lr] = -20
R.servos[0][rr] = 20
R.servos[0][lt] = -20
R.servos[0][rt] = 20
R.servos[0][lb] = -20
R.servos[0][rb] = 20

time.sleep(5)

R.servos[0][lr] = 0
R.servos[0][rr] = 0
R.servos[0][lt] = 0
R.servos[0][rt] = 0
R.servos[0][lb] = 0
R.servos[0][rb] = 0

time.sleep(5)

R.servos[0][lr] = 0
R.servos[0][rr] = 0
R.servos[0][lt] = 40
R.servos[0][rt] = -40
R.servos[0][lb] = 0
R.servos[0][rb] = 0

time.sleep(5)

R.servos[0][lr] = 0
R.servos[0][rr] = 0
R.servos[0][lt] = 40
R.servos[0][rt] = -40
R.servos[0][lb] = -20
R.servos[0][rb] = 20

time.sleep(5)

R.servos[0][lr] = 0
R.servos[0][rr] = 0
R.servos[0][lt] = 40
R.servos[0][rt] = -40
R.servos[0][lb] = -40
R.servos[0][rb] = 40


i = 0
while (i < 100):
    i += 0.1
    time.sleep(0.01)
    R.servos[0][lt] = 40 - i
    R.servos[0][rt] = -40 + i
    
i = 0
while (i < 100):
    i += 0.1
    time.sleep(0.01)
    R.servos[0][lr] =  - i
    R.servos[0][rr] =  i






