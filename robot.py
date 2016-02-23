from sr.robot import *
import time
import customRuggeduino
import PID
import motorHandler
import mapHandler
  
print "Classes imported"

R = Robot.setup()
print "Robot.setup ran"

# Register the custom class with the Robot object
R.ruggeduino_set_handler_by_fwver("SRcustom", customRuggeduino.mpuSonarRuggeduino)
print "Ruggeduino handler ran"

R.init()
print "R.init ran"

D = customRuggeduino.mpuHandler(R.ruggeduinos[0])
print "mpuHandler initialised"

R.wait_start()
print "wait_start ran"

targetYaw = 0
speed = 30

currentTime = time.time()
zone = R.zone
M = mapHandler.mapHandler(zone, currentTime)

P = PID.pidController("steeringPID", 3, 2, 3, targetYaw, 100) #p, i, d, setpoint
print "PID setup"

S = motorHandler.motorHandler(R.motors[0].m0, R.motors[0].m1) #left motor, right motor
print "motorHandler setup"

while True:
   
   if (S.steering < 5 & S.steering > -5):    
        currentTime = time.time()
        markers = R.see( res=(1280,960) )         ## Takes a picture and analyses it at a resolution. For information on which resolutions can vbe used: https://www.studentrobotics.org/docs/programming/sr/vision/#ChoosingResolution
        
        print "I can see", len(markers), "markers:"       ## Prints out how many markers by taking the length of the markers array
        print " "       ##line clear
        
        M.update(markers, currentTime)
        
        print "Cameralocation: ", M.cameraLocation
        print "aCubeLocations: ", M.aCubeLocations
        print "bCubeLocations: ", M.bCubeLocations
        print "cCubeLocations: ", M.cCubeLocations
        print "robotLocations: ", M.robotLocations
    
    if (D.updateAll() == True):
        
        if (P.run(D.yaw) == True):
            steering = P.output
            
            if (S.setSpeedAndSteering(speed, steering) == True):
                print "yaw: ", D.yaw, " pitch:", D.pitch, " roll: ", D.roll, " error: ", D.error, " speed: ", S.speed, " steering: ", S.steering
        
    
    
        
        
        
        
        
        
        
        
        
    