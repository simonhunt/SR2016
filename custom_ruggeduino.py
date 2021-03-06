from sr.robot import *
import time
import math
from limits import angleMod

from robot_1 import WHEEL_RADIUS, ENCODER_RESOLUTION, DEFAULT_TRIG_PIN, DEFAULT_ECHO_PIN

MAX_SONAR = 5000

# WHEEL_RADIUS = 0.04875 #0.04826 #0.05134
# ENCODER_RESOLUTION = 96

class MpuSonarEncoderRuggeduino(Ruggeduino):
    
    def mpuGetYaw(self):
        
        with self.lock:
            yaw = - float(self.command('x'))
        return yaw
    
    def mpuGetPitch(self):
        
        with self.lock:
            pitch = float(self.command('y'))
        return pitch
        
    def mpuGetRoll(self):
        
        with self.lock:
            roll = float(self.command('z'))
        return roll
    
    def mpuGetError(self):
        
        with self.lock:
            error = int(self.command('w')) #error = float(self.command('w'))
        return error
        
    def mpuInit(self):
        
        with self.lock:
            self.command('m')
            
    def sonar(self, trig_pin = DEFAULT_TRIG_PIN, echo_pin = DEFAULT_ECHO_PIN):   #pin = trig, pin+1=echo
    
        with self.lock:
            trig_pin_char = chr(trig_pin + 97) 
            echo_pin_char = chr(echo_pin + 97)
            duration = int(self.command('s' + trig_pin_char + echo_pin_char))  # s for sonar
        
        if (duration == 0):
            duration = MAX_SONAR
        distance = duration * 0.00028
        return distance
        
    
    def encoderGetSteps(self):
        
        with self.lock:
            steps = int(self.command('e'))
        return steps
        
    def setCameraServoAngle(self, desired_angle):
        
        units = int(desired_angle % 10)
        tens = int((desired_angle % 100 - units) / 10)
        hundreds = int((desired_angle - tens - units) / 100)
        
        hundreds_char = chr(hundreds + 97)
        tens_char = chr(tens + 97)
        units_char = chr(units + 97)
        
        # print "units = " + str(units) + str(units_char)
        # print "tens = " + str(tens) + str(tens_char)
        # print "hundreds = " + str(hundreds) + str(hundreds_char)
        
        with self.lock:
            #new_angle = int(self.command('t' + hundreds_char + tens_char + units_char))
            self.command('t' + hundreds_char + tens_char + units_char)
        #return new_angle

class EncoderHandler():
    
    def __init__(self, EncoderRuggeduino, time_period = 0.005): # default 200Hz
        current_time = time.time()
        self.EncoderRuggeduino = EncoderRuggeduino
        self.time_period = time_period
        self.distance = 0
        self.last_time = current_time - time_period
    
    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        updated = False
        
        if (dt >= self.time_period):
            self.distance = (float(self.EncoderRuggeduino.encoderGetSteps()) / ENCODER_RESOLUTION) * 2 * math.pi * WHEEL_RADIUS
            self.last_time = current_time
            updated = True
        
        return updated
        

class MpuHandler():
    
    def __init__(self, MpuRuggeduino, yaw_drift, time_period = 0.005, mpu_start_timeout = 2): # default 200Hz
        current_time = time.time()
        self.innit_time = current_time
        self.time_period = time_period
        self.MpuRuggeduino = MpuRuggeduino
        self.MpuRuggeduino.mpuInit()
        self.yaw = 0
        self.yaw_without_drift = 0
        self.yaw_drift = yaw_drift
        self.pitch = 0
        self.roll = 0
        self.error = 0
        self.last_yaw_time = current_time + mpu_start_timeout - time_period
        self.last_pitch_time = current_time + mpu_start_timeout - time_period
        self.last_roll_time = current_time + mpu_start_timeout - time_period
        self.last_error_time = current_time + mpu_start_timeout - time_period
        time.sleep(mpu_start_timeout)
        
    def setTimePeriod(self, time_period):
        self.time_period = time_period
        
    def updateAll(self):
        current_time = time.time()
        dyt = current_time - self.last_yaw_time
        dpt = current_time - self.last_pitch_time
        drt = current_time - self.last_roll_time
        det = current_time - self.last_error_time
        updated = False
        
        if ((dyt >= self.time_period) and (dpt >= self.time_period) and (drt >= self.time_period) and (det >= self.time_period)):
            self.yaw = self.MpuRuggeduino.mpuGetYaw()
            self.pitch = self.MpuRuggeduino.mpuGetPitch()
            self.roll = self.MpuRuggeduino.mpuGetRoll()
            self.error = self.MpuRuggeduino.mpuGetError()
            self.last_yaw_time = current_time
            self.last_pitch_time = current_time
            self.last_roll_time = current_time
            self.last_error_time = current_time
            updated = True 
        self.updateYawWithoutDrift()
        return updated
        
    def updateYawWithoutDrift(self):
        elapsed_time = self.last_yaw_time - self.innit_time
        drift = self.yaw_drift * elapsed_time
        self.yaw_without_drift = angleMod(self.yaw - drift)
                
    def updateYaw(self):
        current_time = time.time()
        dyt = current_time - self.last_yaw_time
        updated = False
        
        if (dyt >= self.time_period):
            self.yaw = self.MpuRuggeduino.mpuGetYaw()
            self.last_yaw_time = current_time
            updated = True
        return updated
        
    def updatePitch(self):
        current_time = time.time()
        dpt = current_time - self.last_pitch_time
        updated = False
        
        if (dpt >= self.time_period):
            self.pitch = self.MpuRuggeduino.mpuGetPitch()
            self.last_pitch_time = current_time
            updated = True
        return updated
        
    def updateRoll(self):
        current_time = time.time()
        drt = current_time - self.last_roll_time
        updated = False
        
        if (drt >= self.time_period):
            self.roll = self.MpuRuggeduino.mpuGetRoll()
            self.last_roll_time = current_time            
            updated = True
        return updated
        
    def updateError(self):
        current_time = time.time()
        det = current_time - self.last_error_time
        updated = False
        
        if (det >= self.time_period):
            self.error = self.MpuRuggeduino.mpuGetError()
            self.last_error_time = current_time
            updated = True
        return updated
