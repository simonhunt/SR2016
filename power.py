NOTE = 'a'
DURATION = 500 #milliseconds

def signalReady(Power):
    Power.beep(DURATION, note = NOTE)
    