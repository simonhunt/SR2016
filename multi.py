import threading
import time
from limits import angleMod

class MotionThread(threading.Thread):
    
    def __init__(self, MpuHandler, YawPid, MotorHandler, EncoderHandler, time_period = 0.01): #def __init__(self, MpuHandler, YawPid, MotorHandler, EncoderHandler, DisplacementPid, time_period = 0.01):
        threading.Thread.__init__(self)
        self.name = "MotionThread"
        self.steering = 0
        self.yaw = 0
        self.heading = 0
        self.heading_available = True
        self.forced_speed = 0
        self.forced_speed_available = True
        self.new_forced_speed = False
        #self.displacement = 0
        #self.desired_displacement = 0
        self.D = MpuHandler
        self.Y = YawPid
        self.M = MotorHandler
        self.E = EncoderHandler
        #self.S = DisplacementPid
        self.time_period = time_period
    
    def changeHeading(self, angle):
        updated = False
        
        if (self.heading_available == True):
            self.heading = self.heading + angle
            updated = True
        return updated
        
    def setForcedSpeed(self, speed):
        updated = False
        
        if (self.forced_speed_available == True):
            self.forced_speed = speed
            self.new_forced_speed = True
            updated = True
        return updated
    
    def run(self):
        print "Starting" + self.name
        
        while (True):
            
            new_steering = False
            
            if (self.D.updateAll() == True):
                self.yaw = self.D.yaw_without_drift
                
            else:
                print "D returned false in Motion Thread"
                
            if (self.E.update() == True):
                self.displacement = self.E.displacement
                
            else:
                print "E returned false in Motion Thread"
            
            self.heading_available = False
            heading = self.heading
            self.heading_available = True
            
            yaw_pid_input = angleMod(self.yaw - heading)
            
            if (self.Y.run(yaw_pid_input) == True):
                self.steering = self.Y.output
                new_steering = True
                
            else:
                print "Y returned false in Motion Thread"
            
            #self.desired_displacement_available = False
            #self.S.setpoint = self.desired_displacement
            #self.desired_displacement_available = True
            #
            #if (self.S.run(self.displacement) == True):
            #    self.speed = self.S.output
            #    self.new_speed = True
            #     
            #else:
            #    print "S returned false in Motion Thread"
            
            
            if (self.new_forced_speed == True):
                self.forced_speed_available = False
                speed = self.forced_speed
                self.forced_speed_available = True
                new_speed = True
                self.new_forced_speed = False
            
            if (new_steering == True or new_speed == True):
                self.M.setSpeedAndSteering(speed, self.steering)
            else:
                print "speed and steering not set in Motion Thread"
                
            
            
            time.sleep(self.time_period)
                
        print "Exiting " + self.name
