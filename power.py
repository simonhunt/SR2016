READY_NOTE = 'c'
READY_DURATION = 500 #milliseconds

GOOD_NOTE = 'g'
GOOD_DURATION = 1000 #milliseconds

BAD_NOTE = 'a'
BAD_DURATION = 500 #milliseconds

ACTION_NOTE = 'b'
ACTION_DURATION = 200 #milliseconds

ACTIVITY_NOTE = 'b'
ACTIVITY_DURATION = 500 #milliseconds

CAMERA_NOTE = 'd'
CAMERA_DURATION = 100 #milliseconds

SERVO_NOTE = 'e'
SERVO_DURATION = 100 #milliseconds

def signalReady(power):
    power.beep(READY_DURATION, note = READY_NOTE)
    
def signalGood(power):
    power.beep(GOOD_DURATION, note = GOOD_NOTE)

def signalBad(power):
    power.beep(BAD_DURATION, note = BAD_NOTE)
    
def signalAction(power):
    power.beep(ACTION_DURATION, note = ACTION_NOTE)
    
def signalActivity(power):
    power.beep(ACTIVITY_DURATION, note = ACTIVITY_NOTE)
    
def signalCamera(power):
    power.beep(CAMERA_DURATION, note = CAMERA_NOTE)

def signalServo(power):
    power.beep(SERVO_DURATION, note = SERVO_NOTE)
    