import threading
import time

DEBUG_DEBUG = False
DEBUG_MOTION = False
DEBUG_Y = False
DEBUG_S = False
DEBUG_M = False
DEBUG_MAP = False
DEBUG_TARGET = False
DEBUG_SERVO = True


class DebugThread(threading.Thread):
    
    def __init__(self, Threads, time_period = 1): #default 1hz
        threading.Thread.__init__(self)
        
        self.name = "DebugThread"
        
        self.time_period = time_period
        self.debug_counter = 0
        self.Threads = (self,) + Threads
        
    def run(self):
        print "Starting " + self.name
        
        while(True):
            for Thread in self.Threads:
                Thread.debug()
            time.sleep(self.time_period)
        
        print "Exiting " + self.name
    
    def debug(self):
        
        if (DEBUG_DEBUG == True):
            self.debug_counter += 1
            print self.name + ", debug_counter = " + str(self.debug_counter) + ", time = " + str(time.time())