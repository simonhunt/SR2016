import threading
import time
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

INITIALISATION = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 1}
ARMS_UP_OUT_THE_WAY = {'rotate': 0, 'lift': 100, 'grab': 0, 'time': 1}

ARMS_WIDE_POSITIVE_TURN = {'rotate': - 100, 'lift': - 40, 'grab': - 50, 'time': 1}
ARMS_WIDE_NEGATIVE_TURN = {'rotate': 100, 'lift': - 40, 'grab': - 50, 'time': 1}

ARMS_ON_CUBE_POSITIVE_TURN = {'rotate': - 100, 'lift': - 40, 'grab': 20, 'time': 1}
ARMS_ON_CUBE_NEGATIVE_TURN = {'rotate': 100, 'lift': - 40, 'grab': 20, 'time': 1}

LIFT_CUBE_POSITIVE_TURN = {'rotate': - 100, 'lift': 40, 'grab': 20, 'time': 1}
LIFT_CUBE_NEGATIVE_TURN = {'rotate': 100, 'lift': 40, 'grab': 20, 'time': 1}

TURN_CUBE_90 = {'rotate': 0, 'lift': 40, 'grab': 20, 'time': 1}
TURN_CUBE_180 = {'rotate': 100, 'lift': 40, 'grab': 20, 'time': 1}
TURN_CUBE_MINUS_90 = {'rotate': 0, 'lift': 40, 'grab': 20, 'time': 1}
TURN_CUBE_MINUS_180 = {'rotate': - 100, 'lift': 40, 'grab': 20, 'time': 1}

DOWN_CUBE_90 = {'rotate': 0, 'lift': 0, 'grab': 20, 'time': 1}
DOWN_CUBE_180 = {'rotate': 100, 'lift': 0, 'grab': 20, 'time': 1}
DOWN_CUBE_MINUS_90 = {'rotate': 0, 'lift': 0, 'grab': 20, 'time': 1}
DOWN_CUBE_MINUS_180 = {'rotate': - 100, 'lift': 0, 'grab': 20, 'time': 1}

RELEASE_CUBE_90 = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 1}
RELEASE_CUBE_180 = {'rotate': 100, 'lift': 0, 'grab': 0, 'time': 1}
RELEASE_CUBE_MINUS_90 = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 1}
RELEASE_CUBE_MINUS_180 = {'rotate': - 100, 'lift': 0, 'grab': 0, 'time': 1}

class ServosThread(threading.Thread):
    
    def __init__(self, servos, position_timeperiod = 0.01, move_timeperiod = 0.01): # default 100hz postition, 100hz move    
        threading.Thread.__init__(self)
        self.name = "ServosThread"
        self.servos = servos 
        self.position_timeperiod = position_timeperiod
        self.move_timeperiod = move_timeperiod
        
        self.lock = threading.Lock()
        
        self.position = INITIALISATION
        self.initialiseOffsets()
        self.new_position = None
        
        self.moveTo(ARMS_UP_OUT_THE_WAY)
        
    def processNewPosition(self):
        
        with self.lock:
            new_position_local_copy = self.new_position
            
        if (new_position_local_copy != None):
            
            with self.lock:
                self.new_position = None
            
            self.moveTo(new_position_local_copy)
    
    def setNewPosition(self, new_position):
        
        with self.lock:
            self.new_position = new_position
        
    def moveTo(self, new_position):
        drotate = new_position['rotate'] - self.position['rotate']
        dlift = new_position['lift'] - self.position['lift']
        dgrab = new_position['grab'] - self.position['grab']
        
        increments = new_position['time'] / self.move_timeperiod
        
        if (increments == 0):
            fraction_per_increment = 1
         
        else:
            fraction_per_increment = 1 / increments
        
        rotate_increment = drotate * fraction_per_increment
        lift_increment = dlift * fraction_per_increment
        grab_increment = dgrab * fraction_per_increment
        
        i = 1
        while (i < increments):
            new_rotate = self.position['rotate'] + i * rotate_increment
            new_lift = self.position['lift'] + i * lift_increment
            new_grab = self.position['grab'] + i * grab_increment
            
            self.setRotate(new_rotate)
            self.setLift(new_lift)
            self.setGrab(new_grab)
            
            time.sleep(self.move_timeperiod)
            i += 1
        
        self.setRotate(new_position['rotate'])
        self.setLift(new_position['lift'])
        self.setGrab(new_position['grab'])
        time.sleep(self.move_timeperiod)
                
    def initialiseOffsets(self):
        self.setRotate(0)
        self.setLift(0)
        self.setGrab(0)
    
    def setRotate(self, rotate):
        self.position['rotate'] = rotate
        self.servos[SERVO_BOARD][LEFT_ROTATE_PIN] = mapToLimits((self.position['rotate'] + LEFT_ROTATE_OFFSET)  * LEFT_ROTATE_DIRECTION)
        self.servos[SERVO_BOARD][RIGHT_ROTATE_PIN] = mapToLimits((self.position['rotate'] + RIGHT_ROTATE_OFFSET) * RIGHT_ROTATE_DIRECTION)
    
    def setLift(self, lift):
        self.position['lift'] = lift
        self.servos[SERVO_BOARD][LEFT_LIFT_PIN] = mapToLimits((self.position['lift'] + LEFT_LIFT_OFFSET)  * LEFT_LIFT_DIRECTION)
        self.servos[SERVO_BOARD][RIGHT_LIFT_PIN] = mapToLimits((self.position['lift'] + RIGHT_LIFT_OFFSET) * RIGHT_LIFT_DIRECTION)
        
    def setGrab(self, grab):
        self.position['grab'] = grab
        self.servos[SERVO_BOARD][LEFT_GRAB_PIN] = mapToLimits((self.position['grab'] + LEFT_GRAB_OFFSET)  * LEFT_GRAB_DIRECTION)
        self.servos[SERVO_BOARD][RIGHT_GRAB_PIN] = mapToLimits((self.position['grab'] + RIGHT_GRAB_OFFSET) * RIGHT_GRAB_DIRECTION)
    
    def run(self):
        print "Starting " + self.name
        
        while(True):
            self.processNewPosition()
            time.sleep(self.position_timeperiod)
            
        print "Exiting " + self.name

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