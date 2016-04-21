import threading
import time

import noise

from limits import mapToLimits
from positions import *
from debug import DEBUG_SERVO

from robot_1 import ARMS_SERVO_BOARD, LEFT_ROTATE_PIN, LEFT_ROTATE_DIRECTION, LEFT_ROTATE_OFFSET, LEFT_LIFT_PIN, LEFT_LIFT_DIRECTION, LEFT_LIFT_OFFSET, LEFT_GRAB_PIN, LEFT_GRAB_DIRECTION, LEFT_GRAB_OFFSET, RIGHT_ROTATE_PIN, RIGHT_ROTATE_DIRECTION, RIGHT_ROTATE_OFFSET, RIGHT_LIFT_PIN, RIGHT_LIFT_DIRECTION, RIGHT_LIFT_OFFSET, RIGHT_GRAB_PIN, RIGHT_GRAB_DIRECTION, RIGHT_GRAB_OFFSET

# SERVO_BOARD = 0

# LEFT_ROTATE_PIN = 5
# LEFT_ROTATE_DIRECTION = - 1
# LEFT_ROTATE_OFFSET = 0

# LEFT_LIFT_PIN = 4
# LEFT_LIFT_DIRECTION = - 1
# LEFT_LIFT_OFFSET = 0

# LEFT_GRAB_PIN = 0
# LEFT_GRAB_DIRECTION = - 1
# LEFT_GRAB_OFFSET = - 7

# RIGHT_ROTATE_PIN = 2
# RIGHT_ROTATE_DIRECTION = 1
# RIGHT_ROTATE_OFFSET = 0

# RIGHT_LIFT_PIN = 1
# RIGHT_LIFT_DIRECTION = 1
# RIGHT_LIFT_OFFSET = 10
 
# RIGHT_GRAB_PIN = 3
# RIGHT_GRAB_DIRECTION = 1
# RIGHT_GRAB_OFFSET = 0

class ServoThread(threading.Thread):
    
    def __init__(self, servos, power, position_timeperiod = 0.1, move_timeperiod = 0.01): # default 10hz postition, 100hz move    
        threading.Thread.__init__(self)
        self.name = "ServoThread"
        self.servos = servos
        self.power = power
        self.position_timeperiod = position_timeperiod
        self.move_timeperiod = move_timeperiod
        
        self.lock = threading.Lock()
        
        self.position = INITIALISATION
        self.initialiseOffsets()
        self.sequence = []
        
        self.moveTo(ARMS_UP_OUT_THE_WAY)
        
    def processNewPosition(self):
        
        new_position_local_copy = None
        
        with self.lock:
            
            if (len(self.sequence) != 0):
                new_position_local_copy = self.sequence.pop(0)
        
        if (new_position_local_copy != None):
            self.moveTo(new_position_local_copy)
            
    def clearSequence(self):
        
        with self.lock:
            self.sequence = []
            
    def setPosition(self, new_position):
        
        self.clearSequence()
        self.addPosition(new_position)
    
    def addPosition(self, new_position):
        
        with self.lock:
            self.sequence.append(new_position)
    
    def setSequence(self, new_sequence):
        
        self.clearSequence()
        self.addSequence(new_sequence)
            
    def addSequence(self, new_sequence):
        
        with self.lock:
            self.sequence.extend(new_sequence)
        
    def moveTo(self, new_position):
        noise.signalServo(self.power)
        
        start_rotate = self.position['rotate']
        start_lift = self.position['lift']
        start_grab = self.position['grab']
        
        movement_time = new_position['time']        
        finish_rotate = new_position['rotate']
        finish_lift = new_position['lift']
        finish_grab = new_position['grab']
        
        drotate = finish_rotate - start_rotate
        dlift = finish_lift - start_lift
        dgrab = finish_grab - start_grab
        
        increments = movement_time / self.move_timeperiod
        
        if (increments == 0):
            fraction_per_increment = 1
         
        else:
            fraction_per_increment = 1 / increments
        
        rotate_increment = drotate * fraction_per_increment
        lift_increment = dlift * fraction_per_increment
        grab_increment = dgrab * fraction_per_increment

        i = 1
        while (i < increments):
            new_rotate = start_rotate + i * rotate_increment
            new_lift = start_lift + i * lift_increment 
            new_grab = start_grab + i * grab_increment
            
            self.setRotate(new_rotate)
            self.setLift(new_lift)
            self.setGrab(new_grab)
            
            time.sleep(self.move_timeperiod)
            
            i += 1
        
        self.setRotate(finish_rotate)
        self.setLift(finish_lift)
        self.setGrab(finish_grab)
        time.sleep(self.move_timeperiod)
                
    def initialiseOffsets(self):
        self.setRotate(0)
        self.setLift(0)
        self.setGrab(0)
    
    def setRotate(self, rotate):
        self.position['rotate'] = rotate
        self.servos[ARMS_SERVO_BOARD][LEFT_ROTATE_PIN] = int(mapToLimits((self.position['rotate'] + LEFT_ROTATE_OFFSET)  * LEFT_ROTATE_DIRECTION))
        self.servos[ARMS_SERVO_BOARD][RIGHT_ROTATE_PIN] = int(mapToLimits((self.position['rotate'] + RIGHT_ROTATE_OFFSET) * RIGHT_ROTATE_DIRECTION))
    
    def setLift(self, lift):
        self.position['lift'] = lift
        self.servos[ARMS_SERVO_BOARD][LEFT_LIFT_PIN] = int(mapToLimits((self.position['lift'] + LEFT_LIFT_OFFSET)  * LEFT_LIFT_DIRECTION))
        self.servos[ARMS_SERVO_BOARD][RIGHT_LIFT_PIN] = int(mapToLimits((self.position['lift'] + RIGHT_LIFT_OFFSET) * RIGHT_LIFT_DIRECTION))
        
    def setGrab(self, grab):
        self.position['grab'] = grab
        self.servos[ARMS_SERVO_BOARD][LEFT_GRAB_PIN] = int(mapToLimits((self.position['grab'] + LEFT_GRAB_OFFSET)  * LEFT_GRAB_DIRECTION))
        self.servos[ARMS_SERVO_BOARD][RIGHT_GRAB_PIN] = int(mapToLimits((self.position['grab'] + RIGHT_GRAB_OFFSET) * RIGHT_GRAB_DIRECTION))
    
    def run(self):
        print "Starting " + self.name
        
        while(True):
            self.processNewPosition()
            time.sleep(self.position_timeperiod)
            
        print "Exiting " + self.name
        
    def debug(self):
        
        if (DEBUG_SERVO == True):
            
            print self.name
            
            print "position = " + str(self.position) 
            print "len(sequence) = " + str(len(self.sequence))

#from sr.robot import *
#import time
#R = Robot()
#lr = 5 #back is positive
#rr = 2 #forth is positive
#lt = 4 #left hand top servo (positive is down)
#rt = 1 #right hand top servo  (positive up)
#lb = 0 #right hand bottom servo (positive is out)
#rb = 3 #left hand bottom servo (positive is in)
#
#
#R.servos[0][lr] = -20
#R.servos[0][rr] = 20
#R.servos[0][lt] = -20
##R.servos[0][rt] = 20
#R.servos[0][lb] = -20
#R.servos[0][rb] = 20

#time.sleep(5)
#
#R.servos[0][lr] = 0
#R.servos[0][rr] = 0
#R.servos[0][lt] = 0
#R.servos[0][rt] = 0
#R.servos[0][lb] = 0
#R.servos[0][rb] = 0
#
#time.sleep(5)
#
#R.servos[0][lr] = 0
#R.servos[0][rr] = 0
#R.servos[0][lt] = 40
#R.servos[0][rt] = -40
#R.servos[0][lb] = 0
#R.servos[0][rb] = 0
#
#time.sleep(5)
#
#R.servos[0][lr] = 0
#R.servos[0][rr] = 0
#R.servos[0][lt] = 40
#R.servos[0][rt] = -40
#R.servos[0][lb] = -20
#R.servos[0][rb] = 20
#
#time.sleep(5)
#
#R.servos[0][lr] = 0
#R.servos[0][rr] = 0
#R.servos[0][lt] = 40
#R.servos[0][rt] = -40
#R.servos[0][lb] = -40
#R.servos[0][rb] = 40
#
#
#i = 0
#while (i < 100):
#    i += 0.1
#    time.sleep(0.01)
#    R.servos[0][lt] = 40 - i
#    R.servos[0][rt] = -40 + i
#    
#i = 0
#while (i < 100):
#    i += 0.1
#    time.sleep(0.01)
#    R.servos[0][lr] =  - i
#    R.servos[0][rr] =  i
#