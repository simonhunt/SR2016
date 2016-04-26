import threading
import time
import copy

from sr.robot import MARKER_ARENA, MARKER_ROBOT, NET_A, NET_B, NET_C

import map 
import noise

from limits import mapToLimits, rightAngleMod
from debug import DEBUG_MAP

MAX_CUBE_AGE = 5 #seconds 
MAX_BLIND_TIME = 1000 #seconds
MAX_ARENA_MARKER_DISTANCE = 2 #meters

MAX_D_X = 0.125 #meters
MAX_D_Y = 0.125 #meters
MAX_D_Z = 0.25 #meters
MAX_D_PITCH = 45 #degrees
MAX_D_YAW = 20 #degrees
MAX_D_ROLL = 20 #degrees

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
        self.targeted_cube = None
        
    def setTargetedCube(self, targeted_cube):
        self.ignore_arena_markers = True
        self.targeted_cube = targeted_cube
    
    def removeTargetedCube(self):
        self.ignore_arena_markers = False
        self.targeted_cube = None
        
    def prepareForStart(self, see, zone, MotionThread):
        self.zone = zone
        self.see = see
        self.MotionThread = MotionThread
        
        current_time = time.time()
        
        camera_location = map.getInitialCameraLocation(zone, current_time)
        self.setMotionThreadRobotLocation(self.SteadycamThread.camera_angle, camera_location)
        self.starting_cube_locations = map.getStartingCubeLocations(current_time)
        self.robot_locations = map.getStartingRobotLocations(current_time)
        
    def setMotionThreadRobotLocation(self, camera_angle, camera_location):
        robot_location = map.robotLocationFromCameraLocation(camera_location, camera_angle) # self.camera_location
        self.MotionThread.setRobotLocation(robot_location)
        
    def updateMotionThreadRobotLocation(self, camera_angle, old_camera_location, new_camera_location):
        
        d_x = new_camera_location['x'] - old_camera_location['x']
        d_y = new_camera_location['y'] - old_camera_location['y']
        d_z = new_camera_location['z'] - old_camera_location['z']
        d_yaw = new_camera_location['yaw'] - old_camera_location['yaw']
        d_pitch = new_camera_location['pitch'] - old_camera_location['pitch']
        d_roll = new_camera_location['roll'] - old_camera_location['roll']
        
        robot_location = copy.deepcopy(self.MotionThread.robot_location)
        
        robot_location['x'] += d_x
        robot_location['y'] += d_y
        robot_location['z'] += d_z
        robot_location['yaw'] += d_yaw
        robot_location['pitch'] += d_pitch
        robot_location['roll'] += d_roll
        
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
                 
    def updateTargetedCube(self, new_a_cube_locations, new_b_cube_locations, new_c_cube_locations):
        
        if (self.targeted_cube['net'] == 'A'):
            self.checkForNewTargetedCubeLocation(new_a_cube_locations)
            
        elif (self.targeted_cube['net'] == 'B'):
            self.checkForNewTargetedCubeLocation(new_b_cube_locations)
            
        elif (self.targeted_cube['net'] == 'C'):
            self.checkForNewTargetedCubeLocation(new_c_cube_locations)
            
        elif (self.targeted_cube['net'] == '*'):
            all_new_cube_locations = []
            all_new_cube_locations.extend(new_a_cube_locations)
            all_new_cube_locations.extend(new_b_cube_locations)
            all_new_cube_locations.extend(new_c_cube_locations)
            self.checkForNewTargetedCubeLocation(all_new_cube_locations)
            
    def checkForNewTargetedCubeLocation(self, new_cube_locations):
        
        new_targeted_cube_locations = []
        
        for new_cube_location in new_cube_locations:
            
            if (self.isNewCubeTargettedCube(new_cube_location) == True):
                new_targeted_cube_locations.append(new_cube_location)
                
        if (len(new_targeted_cube_locations) != 0):
            print "NEW TARGETED_CUBE SPOTTED: list = " +  str(new_targeted_cube_locations)
            self.setTargetedCube(new_targeted_cube_locations)
                
            
    def isNewCubeTargettedCube(self, new_cube_location):
        same = False
        d_x = abs(new_cube_location['x'] - self.targeted_cube['cube_location']['x'])
        d_y = abs(new_cube_location['y'] - self.targeted_cube['cube_location']['y'])
        d_z = abs(new_cube_location['z'] - self.targeted_cube['cube_location']['z'])
        d_yaw = abs(rightAngleMod(new_cube_location['yaw'] - self.targeted_cube['cube_location']['yaw']))
        d_pitch = abs(new_cube_location['pitch'] - self.targeted_cube['cube_location']['pitch'])
        d_roll =  abs(rightAngleMod(new_cube_location['roll'] - self.targeted_cube['cube_location']['roll']))
        team_scoring_same = (new_cube_location['team_scoring'] == self.targeted_cube['cube_location']['team_scoring'])
        
        if ((d_x < MAX_D_X) and (d_y < MAX_D_Y) and (d_z < MAX_D_Z) and (d_yaw < MAX_D_YAW) and (d_pitch < MAX_D_PITCH) and (d_roll < MAX_D_ROLL) and (team_scoring_same == True)):
            same = True
        
        else:
            print "rejecting targetted_cube with (d_x, d_y, d_z, d_yaw, d_pitch, d_roll) = " + str((d_x, d_y, d_z, d_yaw, d_pitch, d_roll))
            
        return same
        
    def setNewTargetedCube(self, new_cube_locations):
        average_new_cube_location = map.getAverageLocation(new_cube_locations)
        self.targeted_cube['cube_location'] = average_new_cube_location
    
    def run(self):
        print "Starting " + self.name
        
        while (True):
            
            with self.SteadycamThread.camera_moving_lock:
                
                if (self.targeted_cube == None):
                    self.SteadycamThread.nextPan()
                    
                else: #self.targeted_cube != None
                    print "self.targeted_cube['cube_location']" + str(self.targeted_cube['cube_location'])
                    self.SteadycamThread.steady_target = self.targeted_cube['cube_location']
                    
                camera_angle_at_latest_markers = copy.deepcopy(self.SteadycamThread.camera_angle)
                robot_location_at_latest_markers = copy.deepcopy(self.MotionThread.robot_location)
                markers = self.see(res = (1280,960))
            
            camera_location_at_latest_markers = map.cameraLocationFromRobotLocation(robot_location_at_latest_markers, camera_angle_at_latest_markers) #self.MotionThread.robot_location
            camera_location_from_latest_markers = copy.deepcopy(camera_location_at_latest_markers)
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
                    camera_location_from_latest_markers = A.processMarkers(camera_location_at_latest_markers)
                    self.updateMotionThreadRobotLocation(camera_angle_at_latest_markers, camera_location_at_latest_markers, camera_location_from_latest_markers)
            
            i = 0
            for R in RList:
                
                if (R.marker_seen == True):
                    self.robot_locations[i] = R.processMarkers(camera_location_from_latest_markers)
                i += 1
            
            if (TA.marker_seen == True):
                new_a_cube_locations = TA.processMarkers(camera_location_from_latest_markers, self.zone)
                self.a_cube_locations.extend(new_a_cube_locations)
            
            else: 
                new_a_cube_locations = []
            
            if (TB.marker_seen == True):
                new_b_cube_locations = TB.processMarkers(camera_location_from_latest_markers, self.zone)
                self.b_cube_locations.extend(new_b_cube_locations)
                
            else: 
                new_b_cube_locations = []
                
                
            if (TC.marker_seen == True):
                new_c_cube_locations = TC.processMarkers(camera_location_from_latest_markers, self.zone)
                self.c_cube_locations.extend(new_c_cube_locations)
                
            else: 
                new_c_cube_locations = []
                
            if (self.targeted_cube != None):
                self.updateTargetedCube(new_a_cube_locations, new_b_cube_locations, new_c_cube_locations)
                
            
        
        print "Exiting " + self.name
      
    def debug(self):
        
        if (DEBUG_MAP == True):
            
            print self.name
            
            print "length of a_cube_locations = " + str(len(self.a_cube_locations))
            print "length of b_cube_locations = " + str(len(self.b_cube_locations))
            print "length of c_cube_locations = " + str(len(self.c_cube_locations))        
        