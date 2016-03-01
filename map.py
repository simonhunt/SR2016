import math
import cmath
import turn
from sr.robot import *

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

def getInitialCameraLocation(zone, currentTime): ##this method is not finished
    
    
    if (zone == 0):
        initialCameraLocation = ZONE_0_INITIAL_CAMERA_LOCATION
    
    elif (zone == 1):
        initialCameraLocation = ZONE_1_INITIAL_CAMERA_LOCATION
    
    elif (zone == 2):
        initialCameraLocation = ZONE_2_INITIAL_CAMERA_LOCATION
    
    else: #zone == 3
        initialCameraLoctaion = ZONE_0_INITIAL_CAMERA_LOCATION
    
    initialCameraLocation['time'] = currentTime
        
    return initialCameraLocation
            
def getStartingCubeLocations(currentTime):
    
    startingCubeLocations = [STARTING_CUBE_0, STARTING_CUBE_1, STARTING_CUBE_2, STARTING_CUBE_3, STARTING_CUBE_4 , STARTING_CUBE_5 , STARTING_CUBE_6 , STARTING_CUBE_7 , STARTING_CUBE_8]
    return startingCubeLocations
    
def getStartingRobotLocations(current_time):
    
    robot_0 = STARTING__ROBOT_0
    robot_0['time'] = current_time
    robot_1 = STARTING__ROBOT_1
    robot_1['time'] = current_time
    robot_2 = STARTING__ROBOT_2
    robot_2['time'] = current_time
    robot_3 = STARTING__ROBOT_3
    robot_3['time'] = current_time
    
    startingRobotLocations = [robot_0, robot_1, robot_2, robot_3]
    return startingRobotLocations
    
class markerHandler():
    
    def __init__(self, currentTime):
        self.currentTime = currentTime
        self.markerSeen = False
        self.markers = []
    
    def addMarker(self, marker):
        self.markerSeen = True
        self.markers.append(marker)
    

class arenaMarkerHandler(markerHandler):
            
    def processMarkers(self):
        cameraLocations = []
        
        for marker in self.markers:
            cameraLocation = cameraLocationFromArenaMarker(marker, self.currentTime)
            cameraLocations.append(cameraLocation)
            
        cameraLocation = getAverageLocation(cameraLocations)
        
        return cameraLocation
        
class robotMarkerHandler(markerHandler):
            
    def processMarkers(self, cameraLocation):
        robotLocations = []
        
        for marker in self.markers:
            robotLocation = objectLocationFromObjectMarker(marker, cameraLocation, self.currentTime, ROBOT_WIDTH)
            robotLocations.append(robotLocation)
            
        robotLocation = getAverageLocation(robotLocations)
        
        return robotLocation
        
class tokenMarkerHandler(markerHandler):
            
    def processMarkers(self, cameraLocation, zone):
        tokenLocations = []
        
        for marker in self.markers:
            tokenLocation = objectLocationFromObjectMarker(marker, cameraLocation, self.currentTime, TOKEN_WIDTH, zone)
            tokenLocations.append(tokenLocation)
        
        return tokenLocations
        
## CAMERA LOCATION CODE ########################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


def getAverageLocation(locations):
    ## Returns the average of the cameraLocation from the arenaMarker
    
    totalLocationX = 0
    totalLocationY = 0
    totalLocationZ = 0
    totalYawUnitVector = (0 + 0j)
    totalPitchUnitVector = (0 + 0j)
    totalRollUnitVector = (0 + 0j)
    
    numberOfLocations = len(locations)
    
    for location in locations:
        
        totalLocationX += location['x']
        totalLocationY += location['y']
        totalLocationZ += location['z']
        totalYawUnitVector += cmath.exp(1j * math.radians(location['yaw']))
        totalPitchUnitVector += cmath.exp(1j * math.radians(location['pitch']))
        totalRollUnitVector += cmath.exp(1j * math.radians(location['roll']))
        
    averageLocationX = totalLocationX / numberOfLocations
    averageLocationY = totalLocationY / numberOfLocations
    averageLocationZ = totalLocationZ / numberOfLocations
    averageLocationYaw = math.degrees(cmath.phase(totalYawUnitVector))
    averageLocationPitch = math.degrees(cmath.phase(totalPitchUnitVector))
    averageLocationRoll = math.degrees(cmath.phase(totalRollUnitVector))
    time = locations[0]['time']
    
    averageLocation = {'x': averageLocationX, 'y': averageLocationY, 'z': averageLocationZ, 'yaw': averageLocationYaw, 'pitch': averageLocationPitch, 'roll': averageLocationRoll, 'time': time}
    return averageLocation

## OBJECT MARKER CODE ###########################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
    
    
def objectLocationFromObjectMarker(objectMarker, cameraLocation, currentTime, objectWidth, zone = None, approachDistance = 1):
    
    # SPHERICAL VECTOR REFERENCE: http://mathworld.wolfram.com/SphericalCoordinates.html
    
    #  first translate the p.x and p.y angles by the roll of the robot to line with the z axis of the area
    # I have done this with a werid vector method, which I HOPE works
    
    pVector = (math.cos(math.radians(90 - objectMarker.centre.polar.rot_y)) * math.sin(math.radians(90 - objectMarker.centre.polar.rot_x)) + math.cos(math.radians(90 - objectMarker.centre.polar.rot_x))*1j)
    translatedVector = pVector * cmath.exp(1j * math.radians(cameraLocation['roll']))

    translatedPRX = 90 - math.degrees(math.acos(translatedVector.imag)) 
    translatedPRY = 90 - math.degrees(math.acos(translatedVector.real / math.sin(math.acos(translatedVector.imag))))
    
    # next I add the yaw and pitch to the translated values (THIS ONLY WORKES FOR SMALL PITCH, YAW, PRY OR PRX!! IT IS AN APPROXIMATION, i got stuck here) :(
    #build a spherical vector
    
    radial = objectMarker.centre.polar.length
    azimuthal = cameraLocation['yaw'] - translatedPRY
    polar = 90 - translatedPRX - cameraLocation['pitch']  
    
    # cartesian vector
    
    dX = radial * math.cos(math.radians(azimuthal)) * math.sin(math.radians(polar))
    dY = radial * math.sin(math.radians(azimuthal)) * math.sin(math.radians(polar))
    dZ = radial * math.cos(math.radians(polar))
    
    # position of face
    
    x = cameraLocation['x'] + dX
    y = cameraLocation['y'] + dY
    z = cameraLocation['z'] + dZ
    yaw = cameraLocation['yaw'] + 180 - objectMarker.orientation.rot_y
    pitch = objectMarker.orientation.rot_x - cameraLocation['pitch']
    roll = - objectMarker.orientation.rot_z - cameraLocation['roll']
    
    # vector from face to center
    
    radial = - objectWidth / 2
    
    azimuthal = yaw
    polar = 90 - pitch
    
    dX = radial * math.cos(math.radians(azimuthal)) * math.sin(math.radians(polar))
    dY = radial * math.sin(math.radians(azimuthal)) * math.sin(math.radians(polar))
    dZ = radial * math.cos(math.radians(polar))
    
    # position of center 
    
    x += dX
    y += dY
    z += dZ
    
    time = currentTime
    
    objectLocation = {'x': x, 'y': y, 'z': z, 'yaw': yaw, 'pitch': pitch, 'roll': roll, 'time': time}
    
    if (objectMarker.info.marker_type == MARKER_TOKEN_TOP or objectMarker.info.marker_type == MARKER_TOKEN_BOTTOM or objectMarker.info.marker_type == MARKER_TOKEN_SIDE):
        #vector from center to approach spot
        net = objectMarker.info.token_net
        code = objectMarker.info.code
        turn = turn.getTurn(net, roll, code, zone)
        
        if (turn[0] == False):
        
            adX = approachDistance * math.cos(math.radians(azimuthal)) * math.sin(math.radians(polar))
            adY = approachDistance * math.sin(math.radians(azimuthal)) * math.sin(math.radians(polar))
            adZ = approachDistance * math.cos(math.radians(polar))
        
            #position of approach spot
            ax = x + adX
            ay = y + adY
            az = z + adZ
        
            #add positions to objectLocation array
            objectLocation['ax'] = ax
            objectLocation['ay'] = ay
            objectLocation['az'] = az
            
            objectLocation['turns'] = turn[1]
        
        print "turn: ", turn
        
    return objectLocation 
 

## ARENA MARKER CODE ###########################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


def cameraLocationFromArenaMarker(arenaMarker, currentTime):
    ## Returns the co-ordinates of the camera according to an arena marker by adding the arean marker vector to the arena marker location, in a direction depending on which wall it is on.
    
    arenaMarkerLocation = getArenaMarkerLocation(arenaMarker)
    arenaMarkerVector = getArenaMarkerVector(arenaMarker)
    arenaMarkerAngles = getArenaMarkerAngles(arenaMarker)
    
    if (arenaMarkerLocation['wall'] == "Top"):
        x = arenaMarkerLocation['x'] + arenaMarkerVector['alpha']
        y = arenaMarkerLocation['y'] - arenaMarkerVector['beta']
        yaw = arenaMarkerAngles['yaw'] + 90
    elif (arenaMarkerLocation['wall'] == "Right"):
        x = arenaMarkerLocation['x'] - arenaMarkerVector['beta']
        y = arenaMarkerLocation['y'] - arenaMarkerVector['alpha']
        yaw = arenaMarkerAngles['yaw']
    elif (arenaMarkerLocation['wall'] == "Bottom"):
        x = arenaMarkerLocation['x'] - arenaMarkerVector['alpha']
        y = arenaMarkerLocation['y'] + arenaMarkerVector['beta']
        yaw = arenaMarkerAngles['yaw'] - 90
    else: #arenaMarkerLocation['wall'] == "Left"
        x = arenaMarkerLocation['x'] + arenaMarkerVector['beta']
        y = arenaMarkerLocation['y'] + arenaMarkerVector['alpha']
        yaw = arenaMarkerAngles['yaw'] - 180

    z = arenaMarkerLocation['z'] + arenaMarkerVector['gamma']
    
    pitch = arenaMarkerAngles['pitch']
    roll = -arenaMarkerAngles['roll']
    time = currentTime
    
    cameraLocation = {'x': x, 'y': y, 'z': z, 'yaw': yaw, 'pitch': pitch, 'roll': roll, 'time': time}
    
   # print "cameraLocation acording to", arenaMarker.info.code, ": ", cameraLocation, " | with vector: ", arenaMarkerVector
    print "cameraLocation acording to", arenaMarker.info.code, ": ", cameraLocation
    
    return cameraLocation
    
def getArenaMarkerVector(arenaMarker):
    ## Returns the vector from the arena marker to the camera in the direction of the normal from the face of the arena marker.
    ## Alpha is the distance from the arena marker to the camera in the direction left to right facing the arena marker.
    ## Beta is the distance from the arena marker to the camera in the direction coming out of the face of the arena marker.
    ## Gamma is the distance from the arena marker to the camera in the direction bottom to top facing the arena marker. 

    sideAngle = - arenaMarker.centre.polar.rot_x - arenaMarker.orientation.rot_x
    topAngle = arenaMarker.orientation.rot_y - arenaMarker.centre.polar.rot_y
    
    topLength = arenaMarker.centre.polar.length * math.cos(math.radians(sideAngle))
    
    alphaBeforeZRotation = topLength * math.sin(math.radians(topAngle))
    gammaBeforeZRotation = arenaMarker.centre.polar.length * math.sin(math.radians(sideAngle))
    
    alpha = gammaBeforeZRotation * math.sin(math.radians(arenaMarker.orientation.rot_z)) + alphaBeforeZRotation * math.cos(math.radians(arenaMarker.orientation.rot_z))
    beta = topLength * math.cos(math.radians(topAngle))
    gamma = gammaBeforeZRotation * math.cos(math.radians(arenaMarker.orientation.rot_z)) - alphaBeforeZRotation * math.sin(math.radians(arenaMarker.orientation.rot_z))
    
    #alpha = math.cos(math.radians(m.orientation.rot_z))*(m.centre.polar.length)*math.cos(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x))*math.sin(math.radians(m.orientation.rot_y -m.centre.polar.rot_y)) + math.sin(math.radians(m.orientation.rot_z))*(m.centre.polar.length)*math.sin(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x))
    #beta = (m.centre.polar.length)*math.cos(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x))*math.cos(math.radians(m.orientation.rot_y -m.centre.polar.rot_y))
    #gamma = math.cos(math.radians(m.orientation.rot_z))*(m.centre.polar.length)*math.sin(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x)) - math.sin(math.radians(m.orientation.rot_z))*(m.centre.polar.length)*math.cos(math.radians(-m.centre.polar.rot_x -m.orientation.rot_x))*math.sin(math.radians(m.orientation.rot_y -m.centre.polar.rot_y))
    
    arenaMarkerVector = {'alpha': alpha, 'beta': beta, 'gamma': gamma}
    return arenaMarkerVector
        
def getArenaMarkerAngles(arenaMarker):

    yaw = arenaMarker.orientation.rot_y
    pitch = arenaMarker.orientation.rot_x
    roll = arenaMarker.orientation.rot_z
    
    arenaMarkerAngles = {'yaw': yaw, 'pitch': pitch, 'roll': roll}
    return arenaMarkerAngles
     
def getArenaMarkerLocation(arenaMarker): 
    ## Returns the co-ordinates of a arena marker and which wall it is on.
    
    arenaMarkerOffset = arenaMarker.info.offset
    arenaMarkerWall = getArenaMarkerWall(arenaMarkerOffset)
    
    z = 0.175
    
    if (arenaMarkerWall == "Top"):
        x = arenaMarkerOffset +1
        y = 8
    elif (arenaMarkerWall == "Right"):
        x = 8
        y = 14 - arenaMarkerOffset
    elif (arenaMarkerWall == "Bottom"):
        x = 21 - arenaMarkerOffset
        y = 0
    elif (arenaMarkerWall == "Left"):
        x = 0
        y = arenaMarkerOffset - 20
    
    arenaMarkerLocation = {'x': x, 'y': y, 'z': z, 'wall': arenaMarkerWall}
    return arenaMarkerLocation

def getArenaMarkerWall(arenaMarkerOffset):
    ## Returns which wall of the arena a arena marker is on.
    
    if (arenaMarkerOffset < 7): 
        arenaMarkerWall = "Top"
    elif (arenaMarkerOffset < 14):
        arenaMarkerWall = "Right" 
    elif (arenaMarkerOffset < 21):
        arenaMarkerWall = "Bottom" 
    elif (arenaMarkerOffset < 28):
        arenaMarkerWall = "Left"
        
    return arenaMarkerWall    
    
## CODE ########################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################

class mapHandler():
    
    def __init__(self, zone, currentTime):
        self.cameraLocation = getInitialCameraLocation(zone, currentTime)
        self.startingCubeLocations = getStartingCubeLocations(currentTime)
        self.aCubeLocations = []
        self.bCubeLocations = []
        self.cCubeLocations = []
        self.robotLocations = getStartingRobotLocations(currentTime)
        
    def filterCubes(self, currentTime, maxAge = 1):
         
        for A in self.aCubeLocations:
             if ((currentTime - A['time']) > maxAge):
                 self.aCubeLocations.remove(A)
        
        for B in self.bCubeLocations:
             if ((currentTime - B['time']) > maxAge):
                 self.bCubeLocations.remove(B)
                 
        for C in self.cCubeLocations:
             if ((currentTime - C['time']) > maxAge):
                 self.cCubeLocations.remove(C)
                 
        
    def update(self, markers, currentTime, zone):
        A = arenaMarkerHandler(currentTime)
        
        R0 = robotMarkerHandler(currentTime)
        R1 = robotMarkerHandler(currentTime)
        R2 = robotMarkerHandler(currentTime)
        R3 = robotMarkerHandler(currentTime)
        
        TA = tokenMarkerHandler(currentTime)
        TB = tokenMarkerHandler(currentTime)
        TC = tokenMarkerHandler(currentTime)
        
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
        
        if (A.markerSeen == True):
            self.cameraLocation = A.processMarkers()
            
        if (currentTime - self.cameraLocation['time'] <= 1):
            
            i = 0
            for R in RList:
                
                if (R.markerSeen == True):
                    self.robotLocations[i] = R.processMarkers(self.cameraLocation)
                i += 1
            
            if (TA.markerSeen == True):
                self.aCubeLocations.extend(TA.processMarkers(self.cameraLocation, zone))
            
            if (TB.markerSeen == True):
                self.bCubeLocations.extend(TB.processMarkers(self.cameraLocation, zone))
                
            if (TC.markerSeen == True):
                self.cCubeLocations.extend(TC.processMarkers(self.cameraLocation, zone))
                
                  
        #print "camerLocation according to all markers: ", cameraLocation
