import threading
import time
import copy

from sr.robot import MARKER_ARENA, MARKER_ROBOT, NET_A, NET_B, NET_C

import map 
import noise

from limits import mapToLimits
from debug import DEBUG_MAP

MAX_CUBE_AGE = 5 #seconds 
MAX_BLIND_TIME = 1000 #seconds
MAX_ARENA_MARKER_DISTANCE = 2 #meters


class MapThread(threading.Thread):
    
    def __init__(self, SteadycamThread, power):        
        threading.Thread.__init__(self)
        self.name = "MapThread"
        self.SteadycamThread = SteadycamThread
        self.power = power
        self.a_cube_locations = []
        self.b_cube_locations = []
        self.c_cube_locations = []
        self.ignore_arena_markers = False
        
    def prepareForStart(self, see, zone, MotionThread):
        self.zone = zone
        self.see = see
        self.MotionThread = MotionThread
        
        current_time = time.time()
        
        self.camera_location = map.getInitialCameraLocation(zone, current_time)
        self.setMotionThreadRobotLocation(self.SteadycamThread.camera_angle)
        self.starting_cube_locations = map.getStartingCubeLocations(current_time)
        self.robot_locations = map.getStartingRobotLocations(current_time)
        
    def setMotionThreadRobotLocation(self, camera_angle):
        robot_location = map.robotLocationFromCameraLocation(self.camera_location, camera_angle) # self.camera_location
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
            
            self.SteadycamThread.steady_targets = [1]
            
            with self.SteadycamThread.camera_moving_lock:
                #self.SteadycamThread.nextPan()
                camera_angle_at_latest_markers = copy.deepcopy(self.SteadycamThread.camera_angle)
                robot_location_at_latest_markers = copy.deepcopy(self.MotionThread.robot_location)
                markers = self.see(res = (1280,960))
            
            self.camera_location = map.cameraLocationFromRobotLocation(robot_location_at_latest_markers, camera_angle_at_latest_markers) #self.MotionThread.robot_location
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
                    self.setMotionThreadRobotLocation(camera_angle_at_latest_markers)
            
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
        