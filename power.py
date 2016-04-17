READY_NOTE = 'c'
READY_DURATION = 500 #milliseconds

GOOD_NOTE = 'g'
GOOD_DURATION = 1000 #milliseconds

BAD_NOTE = 'a'
BAD_DURATION = 1500 #milliseconds

ACTIVITY_NOTE = 'b'
ACTIVITY_DURATION = 200 #milliseconds

CAMERA_NOTE = 'd'
CAMERA_DURATION = 100 #milliseconds

def signalReady(Power):
    Power.beep(READY_DURATION, note = READY_NOTE)
    
def signalGood(Power):
    Power.beep(GOOD_DURATION, note = GOOD_NOTE)

def signalBad(Power):
    Power.beep(BAD_DURATION, note = BAD_NOTE)
    
def signalActivity(Power):
    Power.beep(ACTIVITY_DURATION, note = ACTIVITY_NOTE)
    
def signalCamera(Power):
    Power.beep(CAMERA_DURATION, note = CAMERA_NOTE)
    