from sr.robot import *
import time
import customRuggeduino
import PID
import motorHandler
  
print "Classes imported"

R = Robot.setup()
print "Robot.setup ran"

# Register the custom class with the Robot object
R.ruggeduino_set_handler_by_fwver("SRcustom", customRuggeduino.mpuSonarRuggeduino)
print "Ruggeduino handler ran"

R.init()
print "R.init ran"

M = customRuggeduino.mpuHandler(R.ruggeduinos[0])
print "mpuHandler initialised"

R.wait_start()
print "wait_start ran"

targetYaw = 0
speed = 30

P = PID.pidController("steeringPID", 1.5, 2, 1, targetYaw) #p, i, d, setpoint
print "PID setup"

S = motorHandler.motorHandler(R.motors[0].m0, R.motors[0].m1) #left motor, right motor
print "motorHandler setup"

while True:
    
    if (M.updateAll() == True):
        
        if (P.run(M.yaw) == True):
            steering = P.output
            
            if (S.setSpeedAndSteering(speed, steering) == True):
                print "yaw: ", M.yaw, " pitch:", M.pitch, " roll: ", M.roll, " error: ", M.error, " speed: ", S.speed, " steering: ", S.steering
        
    
    
        
        
        
        
        
        
        
        
        
    