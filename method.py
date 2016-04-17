import copy

import polar
import limits

CUBE_WIDTH = 0.25
APPROACH_LOCATION_INDENT = 0.75

MAX_TIME_SINCE_ENEMY_SEEN = 5 #seconds
STARTING_SMALLEST_DISTANCE = 8 #seconds
ENEMY_ROBOT_RADIUS = 2.5 #meters
MAX_CUBE_Z = 0.3 #meters
MAX_ROLL_FROM_LEVEL = 10 #degrees
MAX_PITCH_FROM_LEVEL = 10 #degrees
MAX_NUMBER_OF_ENEMY_IN_CUBE_RADIUS = 2 #inclusive (2 is ok)
MAX_NUMBER_OF_ENEMY_IN_APPROACH_RADIUS = 1 #inclusive (2 is ok)
MIN_ENEMY_DISTANCE_TO_CUBE = 0.75 #meters
MIN_ENEMY_DISTANCE_TO_APPROACH = 0.75 #meters

MOVING_SPEED = 1 #meter/sec
ANGULAR_SPEED = 90 #deg/sec
TURN_ZERO_TIME = 0.5 #sec
TURN_90_TIME = 1 #sec
TURN_180_TIME = 5 #sec
TURN_NEGATIVE_90_TIME = 1 #sec
TURN_TIMES = {0: TURN_ZERO_TIME, 90: TURN_90_TIME, 180: TURN_180_TIME, - 90: TURN_NEGATIVE_90_TIME}

def decideCubeToApproach(a_cube_locations, b_cube_locations, c_cube_locations, return_location = 0, robot_location = 0, robots = 0, current_time = 0):
    
    selected_cube = copy.deepcopy(a_cube_locations[0])
    selected_approach_location = copy.deepcopy(selected_cube['approach'][1])
    selected_cube_net = 'A'
    
    cube_approach = {'x': selected_cube['x'], 'y': selected_cube['y'], 'z': selected_cube['z'], 'yaw': selected_cube['yaw'], 'pitch': selected_cube['pitch'], 'roll': selected_cube['roll']}
    cube_approach['approach_location'] = selected_approach_location
    cube_approach['net'] = selected_cube_net
    
    return cube_approach
    
def decideCubeToApproach2(a_cube_locations, b_cube_locations, c_cube_locations, return_location = 0, robot_location = 0, robots = 0, current_time = 0):
    
    cube_approach_paths = []
    
    cube_net = 'A'
    
    for cube_location in a_cube_locations:
        
        if (isCubeLocationOk(cube_location, robots, current_time) == True):
            
            for cube_approach_location in cube_location['approach']:
                
                if (isApproachLocationOk(cube_approach_location, robots, current_time) == True):
                    cube_approach_path = {}
                    cube_approach_path['cube_location'] = cube_location
                    cube_approach_path['approach_location'] = cube_approach_location
                    cube_approach_path['net'] = cube_net
                    cube_approach_paths.append(cube_approach_path)
    
    cube_net = 'B'
    
    for cube_location in b_cube_locations:
        
        if (isCubeLocationOk(cube_location, robots, current_time) == True):
            
            for cube_approach_location in cube_location['approach']:
                
                if (isApproachLocationOk(cube_approach_location, robots, current_time) == True):
                    cube_approach_path = {}
                    cube_approach_path['cube_location'] = cube_location
                    cube_approach_path['approach_location'] = cube_approach_location
                    cube_approach_path['net'] = cube_net
                    cube_approach_paths.append(cube_approach_path)
    
    cube_net = 'C'
    
    for cube_location in c_cube_locations:
        
        if (isCubeLocationOk(cube_location, robots, current_time) == True):
            
            for cube_approach_location in cube_location['approach']:
                
                if (isApproachLocationOk(cube_approach_location, robots, current_time) == True):
                    cube_approach_path = {}
                    cube_approach_path['cube_location'] = cube_location
                    cube_approach_path['approach_location'] = cube_approach_location
                    cube_approach_path['net'] = cube_net
                    cube_approach_paths.append(cube_approach_path)
    
    for cube_approach_path in cube_approach_paths:
        pass

def isCubeLocationOk(cube_location, robots, current_time):
    ok = True
    
    z = cube_location['x']
    roll_from_level = abs(limits.rightAngleMod(cube_location['roll']))
    pitch_from_level = abs(cube_location['pitch'])
    
    if (z > MAX_CUBE_Z):
        ok = False
    
    elif (roll_from_level > MAX_ROLL_FROM_LEVEL):
        ok = False
    
    elif (pitch_from_level > MAX_PITCH_FROM_LEVEL): #this should eliminate any facing up cubes NEEEEEEEDSS A LOT OF TESTING THIS IS A BIG VULNERABILITY
        ok = False
    
    elif (isLocationWithinArena(cube_location) == False):
        ok = False
        
    elif (getNearestEnemyRobotDistanceToLocation(cube_location, robots, current_time) < MIN_ENEMY_DISTANCE_TO_CUBE):
        ok = False
        
    elif (getNumberOfEnemyRobotsWithinRadiusFromLocation(cube_location, robots, current_time) > MAX_NUMBER_OF_ENEMY_IN_CUBE_RADIUS):
        ok = False
    
    return ok

def isApproachLocationOk(approach_location, robots, current_time):
    ok = True
    
    if (isLocationWithinArena(approach_location, APPROACH_LOCATION_INDENT) == False):
        ok = False
        
    elif (getNearestEnemyRobotDistanceToLocation(approach_location, robots, current_time) < MIN_ENEMY_DISTANCE_TO_APPROACH):
        ok = False
        
    elif (getNumberOfEnemyRobotsWithinRadiusFromLocation(approach_location, robots, current_time) > MAX_NUMBER_OF_ENEMY_IN_APPROACH_RADIUS):
        ok = False
    
    return ok

def getCubeApproachPathScore(cube_approach_path, return_location, robot_location, robots, current_time):
    cube_location = cube_approach_path['cube_location']
    approach_location = cube_approach_path['approach_location']
    round_trip_time = estimateRoundTripTime(cube_location, approach_location, robot_location, return_location)
    risk = estimateRisk(cube_approach_path, robot_location, robots, current_time)
    score = 
    
def estimateRoundTripTime(cube_location, approach_location, robot_location, return_location):
    distance_to_approach_location = getDistanceFromLocationToLocation(robot_location, approach_location)    
    distance_to_cube_location = getDistanceFromLocationToLocation(approach_location, cube_location)
    distance_to_return_location = getDistanceFromLocationToLocation(cube_location, return_location)
    
    distance_time = (distance_to_approach_location + distance_to_cube_location + distance_to_return_location) / MOVING_SPEED
    
    turn_time = TURN_TIMES[approach_location['degrees']]
    
    robot_t = robot_location['yaw']
    polar_t_to_approach_location = getPolarTFromLocationToLocation(robot_location, approach_location)    
    polar_t_to_cube_location = getPolarTFromLocationToLocation(approach_location, cube_location)
    polar_t_to_return_location = getPolarTFromLocationToLocation(cube_location, return_location)
    
    degrees_to_approach_location = abs(polar_t_to_approach_location - robot_t)
    degrees_to_cube_location = abs(polar_t_to_cube_location - polar_t_to_approach_location)
    degrees_to_return_location = abs(polar_t_to_return_location - polar_t_to_cube_location)
    
    degrees_time = (degrees_to_approach_location + degrees_to_cube_location + degrees_to_return_location) / ANGULAR_SPEED
    
    total_time = distance_time + turn_time + degrees_time
    return total_time

def estimateRisk(cube_approach_path, robot_location, robots, current_time):
    return 1
    
def isLocationWithinArena(location, indent = (CUBE_WIDTH / 2)):
    
    within_arena = True
    
    x = location['x']
    y = location['y']
    
    if ((x > (8 - indent)) or (y > (8 - indent)) or (x < indent) or (y < indent)):
        within_arena = False
    return within_arena
    
    
def getNearestEnemyRobotDistanceToLocation(location, robots, current_time):
    smallest_distance = STARTING_SMALLEST_DISTANCE
    
    for enemy_robot in robots:
        distance = polar.getPolarR(location, enemy_robot)
        time_since_seen = current_time - enemy_robot['time']
        
        if ((distance < smallest_distance) and (time_since_seen < MAX_TIME_SINCE_ENEMY_SEEN)):
            smallest_distance = distance
    return smallest_distance
            
def getNumberOfEnemyRobotsWithinRadiusFromLocation(location, robots, current_time, radius = ENEMY_ROBOT_RADIUS):
    number = 0
    
    for enemy_robot in robots:
        distance = polar.getPolarR(location, enemy_robot)
        time_since_seen = current_time - enemy_robot['time']
        
        if ((distance < radius) and (time_since_seen < MAX_TIME_SINCE_ENEMY_SEEN)):
            number += 1
    return number
    
def getDistanceFromLocationToLocation(from_location, to_location):
    distance = polar.getPolarR(from_location, to_location)
    return distance

def getPolarTFromLocationToLocation(from_location, to_location):
    theta = polar.getPolarT(from_location, to_location)
    return theta
    
    
def getDistanceToEdge(location):
    
    smallest_distance = 4
    
    x = location['x']
    y = location['y']
    
    distances = [(8 - x), (8 - y), x, y]
    
    for distance in distances:
        
        if (distance < smallest_distance):
            smallest_distance = distance
    return smallest_distance
    
        

'''
min dist to enemy robot*done
distance to zone*done
distance to bot*done
distance to bot + distance to zone?*done
number of enemy robots in x radius*done
in arena *
too near edges *
not right way up*
top face*
not on the floor*
best rotation
something to do with turns
'''