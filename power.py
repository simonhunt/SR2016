READY_NOTE = 'c'
READY_DURATION = 500 #milliseconds

GOOD_NOTE = 'g'
GOOD_DURATION = 1000 #milliseconds

BAD_NOTE = 'a'
BAD_DURATION = 1500 #milliseconds

def signalReady(Power):
    Power.beep(READY_DURATION, note = READY_NOTE)
    
def signalGood(Power):
    Power.beep(GOOD_DURATION, note = GOOD_NOTE)

def signalBad(Power):
    Power.beep(BAD_DURATION, note = BAD_NOTE
    