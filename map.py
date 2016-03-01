import math
import cmath
import turn
from sr.robot import *
from limits import mapToLimits, angleMod

ROBOT_WIDTH = 0.5
TOKEN_WIDTH = 0.25

ZONE_0_INITIAL_CAMERA_LOCATION = {'x': 0, 'y': 0, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
ZONE_1_INITIAL_CAMERA_LOCATION = {'x': 0, 'y': 0, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
ZONE_2_INITIAL_CAMERA_LOCATION = {'x': 0, 'y': 0, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
ZONE_3_INITIAL_CAMERA_LOCATION = {'x': 0, 'y': 0, 'z': 0, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}

STARTING_CUBE_0 = {'x': 2.5, 'y': 2.5, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
STARTING_CUBE_1 = {'x': 4, 'y': 2.5, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
STARTING_CUBE_2 = {'x': 5.5, 'y': 2.5, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
STARTING_CUBE_3 = {'x': 2.5, 'y': 4, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
STARTING_CUBE_4 = {'x': 4, 'y': 4, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
STARTING_CUBE_5 = {'x': 5.5, 'y': 4, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
STARTING_CUBE_6 = {'x': 2.5, 'y': 5.5, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
STARTING_CUBE_7 = {'x': 4, 'y': 5.5, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}
STARTING_CUBE_8 = {'x': 5.5, 'y': 5.5, 'z': 0.125, 'yaw': 0, 'pitch': 0, 'roll': 0, 'time': None}

STARTING__ROBOT_0 = {'x': 1, 'y': 7, 'z': 0.25, 'yaw': -45, 'pitch': 0, 'roll': 0, 'time': None}
STARTING__ROBOT_1 = {'x': 7, 'y': 7, 'z': 0.25, 'yaw': -135, 'pitch': 0, 'roll': 0, 'time': None}
STARTING__ROBOT_2 = {'x': 7, 'y': 1, 'z': 0.25, 'yaw': 135, 'pitch': 0, 'roll': 0, 'time': None}
STARTING__ROBOT_3 = {'x': 1, 'y': 1, 'z': 0.25, 'yaw': 45, 'pitch': 0, 'roll': 0, 'time': None}

###########

## INITIAL LOCATION CODE #######################################################################################
################################################################################################################
################################################################################################################
################################################################################################################

def getInitialCameraLocation(zone, current_time): ##this method is not finished
    
    
    if (zone == 0):
        initial_camera_location = ZONE_0_INITIAL_CAMERA_LOCATION
    
    elif (zone == 1):
        initial_camera_location = ZONE_1_INITIAL_CAMERA_LOCATION
    
    elif (zone == 2):
        initial_camera_location = ZONE_2_INITIAL_CAMERA_LOCATION
    
    else: #zone == 3
        initial_camera_location = ZONE_0_INITIAL_CAMERA_LOCATION
    
    initial_camera_location['time'] = current_time
        
    return initial_camera_location
            
def getStartingCubeLocations(current_time):
    
    starting_cube_locations = [STARTING_CUBE_0, STARTING_CUBE_1, STARTING_CUBE_2, STARTING_CUBE_3, STARTING_CUBE_4 , STARTING_CUBE_5 , STARTING_CUBE_6 , STARTING_CUBE_7 , STARTING_CUBE_8]
    return starting_cube_locations
    
def getStartingRobotLocations(current_time):
    
    robot_0 = STARTING__ROBOT_0
    robot_0['time'] = current_time
    robot_1 = STARTING__ROBOT_1
    robot_1['time'] = current_time
    robot_2 = STARTING__ROBOT_2
    robot_2['time'] = current_time
    robot_3 = STARTING__ROBOT_3
    robot_3['time'] = current_time
    
    starting_robot_locations = [robot_0, robot_1, robot_2, robot_3]
    return starting_robot_locations
    
class MarkerHandler():
    
    def __init__(self, current_time):
        self.current_time = current_time
        self.marker_seen = False
        self.markers = []
    
    def addMarker(self, marker):
        self.marker_seen = True
        self.markers.append(marker)
    

class ArenaMarkerHandler(MarkerHandler):
            
    def processMarkers(self):
        camera_locations = []
        
        for marker in self.markers:
            camera_location = cameraLocationFromArenaMarker(marker, self.current_time)
            camera_locations.append(camera_location)
            
        camera_location = getAverageLocation(camera_locations)
        
        return camera_location
        
class RobotMarkerHandler(MarkerHandler):
            
    def processMarkers(self, camera_location):
        robot_locations = []
        
        for marker in self.markers:
            robot_location = objectLocationFromObjectMarker(marker, camera_location, self.current_time, ROBOT_WIDTH)
            robot_locations.append(robot_location)
            
        robot_location = getAverageLocation(robot_locations)
        
        return robot_location
        
class TokenMarkerHandler(MarkerHandler):
            
    def processMarkers(self, camera_location, zone):
        token_locations = []
        
        for marker in self.markers:
            token_location = objectLocationFromObjectMarker(marker, camera_location, self.current_time, TOKEN_WIDTH, zone)
            token_locations.append(token_location)
        
        return token_locations
        
## CAMERA LOCATION CODE ########################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


def getAverageLocation(locations):
    ## Returns the average of the camera_location from the arenaMarker
    
    total_location_X = 0
    total_location_Y = 0
    total_location_Z = 0
    total_yaw_unit_vector = (0 + 0j)
    total_pitch_unit_vector = (0 + 0j)
    total_roll_unit_vector = (0 + 0j)
    
    number_of_locations = len(locations)
    
    for location in locations:
        
        total_location_X += location['x']
        total_location_Y += location['y']
        total_location_Z += location['z']
        total_yaw_unit_vector += cmath.exp(1j * math.radians(location['yaw']))
        total_pitch_unit_vector += cmath.exp(1j * math.radians(location['pitch']))
        total_roll_unit_vector += cmath.exp(1j * math.radians(location['roll']))
        
    average_location_X = total_location_X / number_of_locations
    average_location_Y = total_location_Y / number_of_locations
    average_location_Z = total_location_Z / number_of_locations
    average_location_Yaw = math.degrees(cmath.phase(total_yaw_unit_vector))
    average_location_Pitch = math.degrees(cmath.phase(total_pitch_unit_vector))
    average_location_Roll = math.degrees(cmath.phase(total_roll_unit_vector))
    time = locations[0]['time']
    
    average_location = {'x': average_location_X, 'y': average_location_Y, 'z': average_location_Z, 'yaw': average_location_Yaw, 'pitch': average_location_Pitch, 'roll': average_location_Roll, 'time': time}
    return average_location

## OBJECT MARKER CODE ###########################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
    
    
def objectLocationFromObjectMarker(object_marker, camera_location, current_time, object_width, zone = None, approach_distance = 1):
    
    # SPHERICAL VECTOR REFERENCE: http://mathworld.wolfram.com/SphericalCoordinates.html
    
    #  first translate the p.x and p.y angles by the roll of the robot to line with the z axis of the area
    # I have done this with a werid vector method, which I HOPE works
    
    p_vector = (math.cos(math.radians(90 - object_marker.centre.polar.rot_y)) * math.sin(math.radians(90 - object_marker.centre.polar.rot_x)) + math.cos(math.radians(90 - object_marker.centre.polar.rot_x))*1j)
    translated_vector = p_vector * cmath.exp(1j * math.radians(camera_location['roll']))

    translated_PRX = 90 - math.degrees(math.acos(translated_vector.imag)) 
    translated_PRY = 90 - math.degrees(math.acos(translated_vector.real / math.sin(math.acos(translated_vector.imag))))
    
    # next I add the yaw and pitch to the translated values (THIS ONLY WORKES FOR SMALL PITCH, YAW, PRY OR PRX!! IT IS AN APPROXIMATION, i got stuck here) :(
    #build a spherical vector
    
    radial = object_marker.centre.polar.length
    azimuthal = camera_location['yaw'] - translated_PRY
    polar = 90 - translated_PRX - camera_location['pitch']  
    
    # cartesian vector
    
    dX = radial * math.cos(math.radians(azimuthal)) * math.sin(math.radians(polar))
    dY = radial * math.sin(math.radians(azimuthal)) * math.sin(math.radians(polar))
    dZ = radial * math.cos(math.radians(polar))
    
    # position of face
    
    x = camera_location['x'] + dX
    y = camera_location['y'] + dY
    z = camera_location['z'] + dZ
    yaw = camera_location['yaw'] + 180 - object_marker.orientation.rot_y
    pitch = object_marker.orientation.rot_x - camera_location['pitch']
    roll = - object_marker.orientation.rot_z - camera_location['roll']
    
    # vector from face to center
    
    radial = - object_width / 2
    
    azimuthal = yaw
    polar = 90 - pitch
    
    dX = radial * math.cos(math.radians(azimuthal)) * math.sin(math.radians(polar))
    dY = radial * math.sin(math.radians(azimuthal)) * math.sin(math.radians(polar))
    dZ = radial * math.cos(math.radians(polar))
    
    # position of center 
    
    x += dX
    y += dY
    z += dZ
    
    time = current_time
    
    object_location = {'x': x, 'y': y, 'z': z, 'yaw': yaw, 'pitch': pitch, 'roll': roll, 'time': time}
    
    if (object_marker.info.marker_type == MARKER_TOKEN_TOP or object_marker.info.marker_type == MARKER_TOKEN_BOTTOM or object_marker.info.marker_type == MARKER_TOKEN_SIDE):
        #vector from center to approach spot
        net = object_marker.info.token_net
        code = object_marker.info.code
        turns = turn.getTurns(net, roll, code, zone)
        approach_locations = []
        
        i = 0
        for turn in turns:
            if (turn[0] == True):
                adX = approach_distance * math.cos(math.radians(azimuthal)) * math.sin(math.radians(polar))
                adY = approach_distance * math.sin(math.radians(azimuthal)) * math.sin(math.radians(polar))
                adZ = approach_distance * math.cos(math.radians(polar))
                
                if (i == 0):
                    ax = x + adX
                    ay = y + adY
                    
                elif (i == 1):
                    ax = x - adY
                    ay = y + adX
                    
                elif (i == 2):
                    ax = x - adX
                    ay = y - adY
                    
                else: # i == 3
                    ax = x + adY
                    ay = y - adX
                
                az = z + adZ
                
                a_yaw = mapToLimits(yaw - 180 + 90 * i)
                a_pitch = - pitch
                a_roll = - roll
                
                degrees = angleMod(turn[1] * 90)
                
                approach_location = {'x': ax, 'y': ay, 'z': az, 'yaw': a_yaw, 'pitch': a_pitch, 'roll': a_roll, 'time': time, 'degrees': degrees}
                
                approach_locations.append(approach_location) 
        
        print "approach locations: ", approach_locations
        
    return object_location 
 

## ARENA MARKER CODE ###########################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


def cameraLocationFromArenaMarker(arenaMarker, current_time):
    ## Returns the co-ordinates of the camera according to an arena marker by adding the arean marker vector to the arena marker location, in a direction depending on which wall it is on.
    
    arena_marker_location = getArenaMarkerLocation(arenaMarker)
    arena_marker_vector = getArenaMarkerVector(arenaMarker)
    arena_marker_angles = getArenaMarkerAngles(arenaMarker)
    
    if (arena_marker_location['wall'] == "Top"):
        x = arena_marker_location['x'] + arena_marker_vector['alpha']
        y = arena_marker_location['y'] - arena_marker_vector['beta']
        yaw = arena_marker_angles['yaw'] + 90
        
    elif (arena_marker_location['wall'] == "Right"):
        x = arena_marker_location['x'] - arena_marker_vector['beta']
        y = arena_marker_location['y'] - arena_marker_vector['alpha']
        yaw = arena_marker_angles['yaw']
        
    elif (arena_marker_location['wall'] == "Bottom"):
        x = arena_marker_location['x'] - arena_marker_vector['alpha']
        y = arena_marker_location['y'] + arena_marker_vector['beta']
        yaw = arena_marker_angles['yaw'] - 90
        
    else: #arena_marker_location['wall'] == "Left"
        x = arena_marker_location['x'] + arena_marker_vector['beta']
        y = arena_marker_location['y'] + arena_marker_vector['alpha']
        yaw = arena_marker_angles['yaw'] - 180

    z = arena_marker_location['z'] + arena_marker_vector['gamma']
    
    pitch = arena_marker_angles['pitch']
    roll = -arena_marker_angles['roll']
    time = current_time
    
    camera_location = {'x': x, 'y': y, 'z': z, 'yaw': yaw, 'pitch': pitch, 'roll': roll, 'time': time}
    
   # print "camera_location acording to", arenaMarker.info.code, ": ", camera_location, " | with vector: ", arena_marker_vector
    print "camera_location acording to", arenaMarker.info.code, ": ", camera_location
    
    return camera_location
    
def getArenaMarkerVector(arenaMarker):
    ## Returns the vector from the arena marker to the camera in the direction of the normal from the face of the arena marker.
    ## Alpha is the distance from the arena marker to the camera in the direction left to right facing the arena marker.
    ## Beta is the distance from the arena marker to the camera in the direction coming out of the face of the arena marker.
    ## Gamma is the distance from the arena marker to the camera in the direction bottom to top facing the arena marker. 

    side_angle = - arenaMarker.centre.polar.rot_x - arenaMarker.orientation.rot_x
    top_angle = arenaMarker.orientation.rot_y - arenaMarker.centre.polar.rot_y
    
    top_length = arenaMarker.centre.polar.length * math.cos(math.radians(side_angle))
    
    alpha_before_z_rotation = top_length * math.sin(math.radians(top_angle))
    gamma_before_z_rotation = arenaMarker.centre.polar.length * math.sin(math.radians(side_angle))
    
    alpha = gamma_before_z_rotation * math.sin(math.radians(arenaMarker.orientation.rot_z)) + alpha_before_z_rotation * math.cos(math.radians(arenaMarker.orientation.rot_z))
    beta = top_length * math.cos(math.radians(top_angle))
    gamma = gamma_before_z_rotation * math.cos(math.radians(arenaMarker.orientation.rot_z)) - alpha_before_z_rotation * math.sin(math.radians(arenaMarker.orientation.rot_z))
    
    #alpha = math.cos(math.radians(m.orientation.rot_z))*(m.centre.polar.length)*math.cos(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x))*math.sin(math.radians(m.orientation.rot_y -m.centre.polar.rot_y)) + math.sin(math.radians(m.orientation.rot_z))*(m.centre.polar.length)*math.sin(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x))
    #beta = (m.centre.polar.length)*math.cos(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x))*math.cos(math.radians(m.orientation.rot_y -m.centre.polar.rot_y))
    #gamma = math.cos(math.radians(m.orientation.rot_z))*(m.centre.polar.length)*math.sin(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x)) - math.sin(math.radians(m.orientation.rot_z))*(m.centre.polar.length)*math.cos(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x))*math.sin(math.radians(m.orientation.rot_y -m.centre.polar.rot_y))
    
    arena_marker_vector = {'alpha': alpha, 'beta': beta, 'gamma': gamma}
    return arena_marker_vector
        
def getArenaMarkerAngles(arenaMarker):

    yaw = arenaMarker.orientation.rot_y
    pitch = arenaMarker.orientation.rot_x
    roll = arenaMarker.orientation.rot_z
    
    arena_marker_angles = {'yaw': yaw, 'pitch': pitch, 'roll': roll}
    return arena_marker_angles
     
def getArenaMarkerLocation(arenaMarker): 
    ## Returns the co-ordinates of a arena marker and which wall it is on.
    
    arena_marker_offset = arenaMarker.info.offset
    arena_marker_wall = getArenaMarkerWall(arena_marker_offset)
    
    z = 0.175
    
    if (arena_marker_wall == "Top"):
        x = arena_marker_offset +1
        y = 8
        
    elif (arena_marker_wall == "Right"):
        x = 8
        y = 14 - arena_marker_offset
        
    elif (arena_marker_wall == "Bottom"):
        x = 21 - arena_marker_offset
        y = 0
        
    elif (arena_marker_wall == "Left"):
        x = 0
        y = arena_marker_offset - 20
    
    arena_marker_location = {'x': x, 'y': y, 'z': z, 'wall': arena_marker_wall}
    return arena_marker_location

def getArenaMarkerWall(arena_marker_offset):
    ## Returns which wall of the arena a arena marker is on.
    
    if (arena_marker_offset < 7): 
        arena_marker_wall = "Top"
        
    elif (arena_marker_offset < 14):
        arena_marker_wall = "Right" 
        
    elif (arena_marker_offset < 21):
        arena_marker_wall = "Bottom" 
        
    elif (arena_marker_offset < 28):
        arena_marker_wall = "Left"
        
    return arena_marker_wall    
    
## CODE ########################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################

class MapHandler():
    
    def __init__(self, zone, current_time):
        self.camera_location = getInitialCameraLocation(zone, current_time)
        self.starting_cube_locations = getStartingCubeLocations(current_time)
        self.a_cube_locations = []
        self.b_cube_locations = []
        self.c_cube_locations = []
        self.robot_locations = getStartingRobotLocations(current_time)
        
    def filterCubes(self, current_time, maxAge = 1):
         
        for A in self.a_cube_locations:
             if ((current_time - A['time']) > maxAge):
                 self.a_cube_locations.remove(A)
        
        for B in self.b_cube_locations:
             if ((current_time - B['time']) > maxAge):
                 self.b_cube_locations.remove(B)
                 
        for C in self.c_cube_locations:
             if ((current_time - C['time']) > maxAge):
                 self.c_cube_locations.remove(C)
                 
        
    def update(self, markers, current_time, zone):
        A = ArenaMarkerHandler(current_time)
        
        R0 = RobotMarkerHandler(current_time)
        R1 = RobotMarkerHandler(current_time)
        R2 = RobotMarkerHandler(current_time)
        R3 = RobotMarkerHandler(current_time)
        
        TA = TokenMarkerHandler(current_time)
        TB = TokenMarkerHandler(current_time)
        TC = TokenMarkerHandler(current_time)
        
        RList = [R0, R1, R2, R3]
        
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
            
        if (current_time - self.camera_location['time'] <= 1):
            
            i = 0
            for R in RList:
                
                if (R.marker_seen == True):
                    self.robot_locations[i] = R.processMarkers(self.camera_location)
                i += 1
            
            if (TA.marker_seen == True):
                self.a_cube_locations.extend(TA.processMarkers(self.camera_location, zone))
            
            if (TB.marker_seen == True):
                self.b_cube_locations.extend(TB.processMarkers(self.camera_location, zone))
                
            if (TC.marker_seen == True):
                self.c_cube_locations.extend(TC.processMarkers(self.camera_location, zone))
                
                  
        #print "camerLocation according to all markers: ", camera_location
