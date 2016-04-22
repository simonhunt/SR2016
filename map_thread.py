import threading
import time

from sr.robot import MARKER_ARENA, MARKER_ROBOT, NET_A, NET_B, NET_C

import map 
import noise

from limits import mapToLimits
from debug import DEBUG_MAP

from robot_1 import CAMERA_SERVO_BOARD, CAMERA_SERVO_PIN

MAX_CUBE_AGE = 5 #seconds 
MAX_BLIND_TIME = 1000 #seconds
MAX_ARENA_MARKER_DISTANCE = 2.5 #meters

#temp consts
MAX_CAMERA_OUTPUT = 100
MIN_CAMERA_OUTPUT = 100
MAX_CAMERA_ANGLE = 45 #deg
MIN_CAMERA_ANGLE = -45 #deg
CAMERA_TURN_RATE = 200 #/sec

class MapThread(threading.Thread):
    
    def __init__(self, servos, power):        
        threading.Thread.__init__(self)
        self.name = "MapThread"
        self.servos = servos
        self.camera_angle = 0
        self.power = power
        self.a_cube_locations = []
        self.b_cube_locations = []
        self.c_cube_locations = []
        self.ignore_arena_markers = False
        
        
        self.servos[CAMERA_SERVO_BOARD][CAMERA_SERVO_PIN] = 100
        print "camera_servo"
        
        
    def prepareForStart(self, see, zone, MotionThread):
        self.zone = zone
        self.see = see
        self.MotionThread = MotionThread
        
        current_time = time.time()
        
        self.camera_location = map.getInitialCameraLocation(zone, current_time)
        self.setMotionThreadRobotLocation()
        self.starting_cube_locations = map.getStartingCubeLocations(current_time)
        self.robot_locations = map.getStartingRobotLocations(current_time)
        
    def changeCameraAngle(self):
        
        if (self.camera_angle == 0):
            self.moveCameraServo(MAX_CAMERA_ANGLE)
        
        elif (self.camera_angle == MAX_CAMERA_ANGLE):
            self.moveCameraServo(- MIN_CAMERA_ANGLE)
        
        elif (self.camera_angle == - MIN_CAMERA_ANGLE):
            self.moveCameraServo(0)
            
        
    def moveCameraServo(self, new_camera_angle):
        start_output = self.servos[CAMERA_SERVO_BOARD][CAMERA_SERVO_PIN]
        new_camera_angle = mapToLimits(new_camera_angle, MAX_CAMERA_ANGLE, MIN_CAMERA_ANGLE)
        finish_output = int(mapToLimits((new_camera_angle - MIN_CAMERA_ANGLE) * (MAX_CAMERA_OUTPUT - MIN_CAMERA_OUTPUT) / (MAX_CAMERA_ANGLE - MIN_CAMERA_ANGLE)))
        self.servos[CAMERA_SERVO_BOARD][CAMERA_SERVO_PIN] = finish_output
        time_to_sleep = (abs(finish_output - start_output) / CAMERA_TURN_RATE)
        time.sleep(time_to_sleep)
        self.camera_angle = new_camera_angle
        
    def setMotionThreadRobotLocation(self):
        robot_location = map.robotLocationFromCameraLocation(self.camera_location, self.camera_angle) # self.camera_location
        self.MotionThread.setRobotLocation(robot_location)
        
    def filterCubesByAge(self, current_time):
         
        for A in self.a_cube_locations:
             if ((current_time - A['time']) > MAX_CUBE_AGE):
                 self.a_cube_locations.remove(A)
        
        for B in self.b_cube_locations:
             if ((current_time - B['time']) > MAX_CUBE_AGE):
                 self.b_cube_locations.remove(B)
                 
        for C in self.c_cube_locations:
             if ((current_time - C['time']) > MAX_CUBE_AGE):
                 self.c_cube_locations.remove(C)
    
    def run(self):
        print "Starting " + self.name
        
        while (True):
            
            self.changeCameraAngle()
            
            self.camera_location = map.cameraLocationFromRobotLocation(self.MotionThread.robot_location, self.camera_angle) #self.MotionThread.robot_location
            current_time = time.time()
            self.filterCubesByAge(current_time)
            
            A = map.ArenaMarkerHandler(current_time)
            
            R0 = map.RobotMarkerHandler(current_time)
            R1 = map.RobotMarkerHandler(current_time)
            R2 = map.RobotMarkerHandler(current_time)
            R3 = map.RobotMarkerHandler(current_time)
            
            TA = map.TokenMarkerHandler(current_time)
            TB = map.TokenMarkerHandler(current_time)
            TC = map.TokenMarkerHandler(current_time)
            
            RList = [R0, R1, R2, R3]
            
            noise.signalCamera(self.power)
            markers = self.see( res=(1280,960) )
            
            for marker in markers:
                
                if (marker.info.marker_type == MARKER_ARENA): # & (m.info.code < 28)
                    A.addMarker(marker)
                    
                elif (marker.info.marker_type == MARKER_ROBOT): # & (m.info.code > 27 & m.info.code < 32) 
                    #RList[marker.info.offset].addMarker(marker)
                    
                    if (marker.info.offset == 0):
                        R0.addMarker(marker)
                        
                    elif(marker.info.offset == 1):
                        R1.addMarker(marker)
                        
                    elif(marker.info.offset == 2):
                        R2.addMarker(marker)
                        
                    elif (marker.info.offset == 3):
                        R3.addMarker(marker)
                    
                    else:
                        print "error: robot marker with offset != {0,1,2,3}"
                    
                else: # MARKER_TOKEN
                    
                    if (marker.info.token_net == NET_A):
                        TA.addMarker(marker)
                    
                    elif (marker.info.token_net == NET_B):
                        TB.addMarker(marker)
                        
                    elif (marker.info.token_net == NET_C):
                        TC.addMarker(marker)
                        
                    else:
                        print "error: marker with undefined NET handled as token"
            
            if ((A.marker_seen == True) and (self.ignore_arena_markers == False)):
                A.filterMarkersByDistance(MAX_ARENA_MARKER_DISTANCE)
                
                if (A.marker_in_range_seen == True):
                    self.camera_location = A.processMarkers()
                    self.setMotionThreadRobotLocation()
            
            if (current_time - self.camera_location['time'] < MAX_BLIND_TIME):
                
                i = 0
                for R in RList:
                    
                    if (R.marker_seen == True):
                        self.robot_locations[i] = R.processMarkers(self.camera_location)
                    i += 1
                
                if (TA.marker_seen == True):
                    self.a_cube_locations.extend(TA.processMarkers(self.camera_location, self.zone))
                
                if (TB.marker_seen == True):
                    self.b_cube_locations.extend(TB.processMarkers(self.camera_location, self.zone))
                    
                if (TC.marker_seen == True):
                    self.c_cube_locations.extend(TC.processMarkers(self.camera_location, self.zone))
        
        print "Exiting " + self.name
        
    def debug(self):
        
        if (DEBUG_MAP == True):
            
            print self.name
            
            print "length of a_cube_locations = " + str(len(self.a_cube_locations))
            print "length of b_cube_locations = " + str(len(self.b_cube_locations))
            print "length of c_cube_locations = " + str(len(self.c_cube_locations))        
        