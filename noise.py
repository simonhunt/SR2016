READY_NOISE_DEBUG = True
GOOD_NOISE_DEBUG = True
BAD_NOISE_DEBUG = True
ACTION_NOISE_DEBUG = True
ACTIVITY_NOISE_DEBUG = True
CAMERA_NOISE_DEBUG = True
SERVO_NOISE_DEBUG = True
TARGET_NOISE_DEBUG = True

READY_NOTE = 'c'
READY_DURATION = 200 #milliseconds

GOOD_NOTE = 'g'
GOOD_DURATION = 300 #milliseconds

BAD_NOTE = 'a'
BAD_DURATION = 300 #milliseconds

ACTION_NOTE = 'b'
ACTION_DURATION = 200 #milliseconds

ACTIVITY_NOTE = 'g'
ACTIVITY_DURATION = 100 #milliseconds

CAMERA_NOTE = 'd'
CAMERA_DURATION = 100 #milliseconds

SERVO_NOTE = 'e'
SERVO_DURATION = 100 #milliseconds

TARGET_NOTE = 'f'
TARGET_DURATION = 100 #milliseconds

def signalReady(power):
    if (READY_NOISE_DEBUG == True):
        power.beep(READY_DURATION, note = READY_NOTE)
    
def signalGood(power):
    
    if (GOOD_NOISE_DEBUG == True):
        power.beep(GOOD_DURATION, note = GOOD_NOTE)

def signalBad(power):
    
    if (BAD_NOISE_DEBUG == True):
        power.beep(BAD_DURATION, note = BAD_NOTE)
    
def signalAction(power):
    
    if (ACTION_NOISE_DEBUG == True):
        power.beep(ACTION_DURATION, note = ACTION_NOTE)
    
def signalActivity(power):
    
    if (ACTIVITY_NOISE_DEBUG == True):
        power.beep(ACTIVITY_DURATION, note = ACTIVITY_NOTE)
    
def signalCamera(power):
    
    if (CAMERA_NOISE_DEBUG == True):
        power.beep(CAMERA_DURATION, note = CAMERA_NOTE)

def signalServo(power):
    
    if (SERVO_NOISE_DEBUG == True):
        power.beep(SERVO_DURATION, note = SERVO_NOTE)

def signalTarget(power):
    
    if (TARGET_NOISE_DEBUG == True):
        power.beep(TARGET_DURATION, note = TARGET_NOTE)
    