import threading
import time
from sr.robot import MARKER_ARENA, MARKER_ROBOT, NET_A, NET_B, NET_C
import map 

MAX_BLIND_TIME = 60 #seconds

class MapThread(threading.Thread):
    
    def __init__(self):        
        threading.Thread.__init__(self)
        self.name = "MapThread"
        
    def prepareForStart(self, see, zone, MotionThread):
        self.zone = zone
        self.see = see
        self.MotionThread = MotionThread # not sure if you can do this
        
        current_time = time.time()
        
        self.camera_location = map.getInitialCameraLocation(zone, current_time)
        self.setMotionThreadRobotLocation()
        
        self.starting_cube_locations = map.getStartingCubeLocations(current_time)
        self.a_cube_locations = []
        self.b_cube_locations = []
        self.c_cube_locations = []
        self.robot_locations = map.getStartingRobotLocations(current_time)        
        
    def setMotionThreadRobotLocation(self):
        robot_location = self.camera_location # map.robotLocationFromCameraLocation(self.camera_location)
        self.MotionThread.setRobotLocation(robot_location)
    
    def run(self):
        self.camera_location = self.MotionThread.robot_location #map.cameraLocationFromRobotLocation(self.MotionThread.robot_location)
        current_time = time.time()
        
        A = map.ArenaMarkerHandler(current_time)
        
        R0 = map.RobotMarkerHandler(current_time)
        R1 = map.RobotMarkerHandler(current_time)
        R2 = map.RobotMarkerHandler(current_time)
        R3 = map.RobotMarkerHandler(current_time)
        
        TA = map.TokenMarkerHandler(current_time)
        TB = map.TokenMarkerHandler(current_time)
        TC = map.TokenMarkerHandler(current_time)
        
        RList = [R0, R1, R2, R3]
        
        markers = self.see()
        
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
        
        if (A.marker_seen == True):
            self.camera_location = A.processMarkers()
            self.setMotionThreadRobotLocation
        
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
        