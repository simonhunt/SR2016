import copy

import polar
import limits

from robot_1 import APPROACH_LOCATION_INDENT, ENEMY_ROBOT_RADIUS, MAX_NUMBER_OF_ENEMY_IN_CUBE_RADIUS, MAX_NUMBER_OF_ENEMY_IN_APPROACH_RADIUS, MIN_ENEMY_DISTANCE_TO_CUBE, MIN_ENEMY_DISTANCE_TO_APPROACH, MOVING_SPEED, ANGULAR_SPEED, TURN_TIMES

CUBE_WIDTH = 0.25
#APPROACH_LOCATION_INDENT = 0.75

MAX_TIME_SINCE_ENEMY_SEEN = 5 #seconds
STARTING_SMALLEST_DISTANCE = 8 #seconds
#ENEMY_ROBOT_RADIUS = 2.5 #meters
MAX_CUBE_Z = 0.2 #meters
MAX_ROLL_FROM_LEVEL = 10 #degrees
MAX_PITCH_FROM_LEVEL = 10 #degrees
# MAX_NUMBER_OF_ENEMY_IN_CUBE_RADIUS = 2 #inclusive (2 is ok)
# MAX_NUMBER_OF_ENEMY_IN_APPROACH_RADIUS = 1 #inclusive (1 is ok)
# MIN_ENEMY_DISTANCE_TO_CUBE = 0.75 #meters
# MIN_ENEMY_DISTANCE_TO_APPROACH = 1 #meters

# MOVING_SPEED = 1 #meter/sec
# ANGULAR_SPEED = 90 #deg/sec

# TURN_ZERO_TIME = 0.5 #sec
# TURN_90_TIME = 1 #sec
# TURN_180_TIME = 5 #sec
# TURN_NEGATIVE_90_TIME = 1 #sec
# TURN_TIMES = {0: TURN_ZERO_TIME, 90: TURN_90_TIME, 180: TURN_180_TIME, - 90: TURN_NEGATIVE_90_TIME}

def decideCubeToApproach(a_cube_locations, b_cube_locations, c_cube_locations):
    
    selected_cube = copy.deepcopy(a_cube_locations[0])
    selected_approach_location = copy.deepcopy(selected_cube['approach'][1])
    selected_cube_net = 'A'
    
    cube_approach = {'x': selected_cube['x'], 'y': selected_cube['y'], 'z': selected_cube['z'], 'yaw': selected_cube['yaw'], 'pitch': selected_cube['pitch'], 'roll': selected_cube['roll']}
    cube_approach['approach_location'] = selected_approach_location
    cube_approach['net'] = selected_cube_net
    
    return cube_approach
    
def decideCubeApproachPath(a_cube_locations, b_cube_locations, c_cube_locations, return_location, robot_location, zone, robot_locations, current_time):
    
    cube_approach_paths = []
    
    cube_net = 'A'
    
    for cube_location in a_cube_locations:
        
        if (isCubeLocationOk(cube_location, robot_locations, zone, current_time) == True):
            
            for cube_approach_location in cube_location['approach']:
                
                if (isApproachLocationOk(cube_approach_location, robot_locations, current_time) == True):
                    cube_approach_path = {}
                    cube_approach_path['cube_location'] = cube_location
                    cube_approach_path['approach_location'] = cube_approach_location
                    cube_approach_path['net'] = cube_net
                    cube_approach_paths.append(cube_approach_path)
    
    cube_net = 'B'
    
    for cube_location in b_cube_locations:
        
        if (isCubeLocationOk(cube_location, robot_locations, zone, current_time) == True):
            
            for cube_approach_location in cube_location['approach']:
                
                if (isApproachLocationOk(cube_approach_location, robot_locations, current_time) == True):
                    cube_approach_path = {}
                    cube_approach_path['cube_location'] = cube_location
                    cube_approach_path['approach_location'] = cube_approach_location
                    cube_approach_path['net'] = cube_net
                    cube_approach_paths.append(cube_approach_path)
    
    cube_net = 'C'
    
    for cube_location in c_cube_locations:
        
        if (isCubeLocationOk(cube_location, robot_locations, zone, current_time) == True):
            
            for cube_approach_location in cube_location['approach']:
                
                if (isApproachLocationOk(cube_approach_location, robot_locations, current_time) == True):
                    cube_approach_path = {}
                    cube_approach_path['cube_location'] = cube_location
                    cube_approach_path['approach_location'] = cube_approach_location
                    cube_approach_path['net'] = cube_net
                    cube_approach_paths.append(cube_approach_path)
    
    print "cube_location and approach_locations screened, len(cube_approach_paths) = " + str(len(cube_approach_paths))
    
    best_info = {'score': 0}
    best_cube_approach_path = None
    
    for cube_approach_path in cube_approach_paths:
        cube_approach_path_info = getCubeApproachPathInfo(cube_approach_path, return_location, robot_location, zone, robot_locations, current_time)
        
        if (cube_approach_path_info['score'] > best_info['score']):
            
            best_info = cube_approach_path_info
            best_cube_approach_path = cube_approach_path
            
            print "New best_cube_approach_path with info = " + str(best_info) + ", best_cube_approach_path = " + str(best_cube_approach_path)
        
        else:
            print "cube_approach_path rejected with info = " + str(cube_approach_path_info) + ", cube_approach_path = " + str(cube_approach_path)
    
    best_cube_approach_path['info'] = best_info
    
    print "best_cube_approach_path selected = " + str(best_cube_approach_path)
    
    return best_cube_approach_path
        
def isCubeLocationOk(cube_location, robot_locations, zone, current_time):
    ok = True
    
    z = cube_location['z']
    
    roll_from_level = abs(limits.rightAngleMod(cube_location['roll']))
    pitch_from_level = abs(cube_location['pitch'])
    cube_location_within_arena = isLocationWithinArena(cube_location)
    points_increase = getPointsIncrease(cube_location, zone)
    nearest_enemy_distance = getNearestEnemyRobotDistanceToLocation(cube_location, robot_locations, current_time)
    number_of_enemy_within_radius = getNumberOfEnemyRobotsWithinRadiusFromLocation(cube_location, robot_locations, current_time)
    
    if (z > MAX_CUBE_Z):
        ok = False
        print "rejecting cube_location due to z = " + str(z) + ", cube_location = " + str(cube_location)            
    
    elif (roll_from_level > MAX_ROLL_FROM_LEVEL):
        ok = False
        print "rejecting cube_location due to roll_from_level = " + str(roll_from_level) + ", cube_location = " + str(cube_location)        
    
    elif (pitch_from_level > MAX_PITCH_FROM_LEVEL): #this should eliminate any facing up cubes NEEEEEEEDSS A LOT OF TESTING THIS IS A BIG VULNERABILITY
        ok = False
        print "rejecting cube_location due to pitch_from_level = " + str(pitch_from_level) + ", cube_location = " + str(cube_location)
    
    elif (cube_location_within_arena == False):
        ok = False
        print "rejecting cube_location due to cube_location_within_arena = " + str(cube_location_within_arena) + ", cube_location = " + str(cube_location)
        
    elif (points_increase == 0):
        ok = False
        print "rejecting cube_location due to points_increase = " + str(points_increase) + ", cube_location = " + str(cube_location)
        
    elif (nearest_enemy_distance < MIN_ENEMY_DISTANCE_TO_CUBE):
        ok = False
        print "rejecting cube_location due to nearest_enemy_distance = " + str(nearest_enemy_distance) + ", cube_location = " + str(cube_location)
        
    elif (number_of_enemy_within_radius > MAX_NUMBER_OF_ENEMY_IN_CUBE_RADIUS):
        ok = False
        print "rejecting cube_location due to number_of_enemy_within_radius = " + str(number_of_enemy_within_radius) + ", cube_location = " + str(cube_location)
    
    return ok

def isApproachLocationOk(approach_location, robot_locations, current_time):
    ok = True
    
    approach_location_within_arena = isLocationWithinArena(approach_location, APPROACH_LOCATION_INDENT)
    nearest_enemy_distance = getNearestEnemyRobotDistanceToLocation(approach_location, robot_locations, current_time)
    number_of_enemy_within_radius = getNumberOfEnemyRobotsWithinRadiusFromLocation(approach_location, robot_locations, current_time)
    
    if (approach_location_within_arena == False):
        ok = False
        print "rejecting approach_location due to approach_location_within_arena = " + str(approach_location_within_arena) + ", approach_location = " + str(approach_location)
        
    elif (nearest_enemy_distance < MIN_ENEMY_DISTANCE_TO_APPROACH):
        ok = False
        print "rejecting approach_location due to nearest_enemy_distance = " + str(nearest_enemy_distance) + ", approach_location = " + str(approach_location)   
     
    elif (number_of_enemy_within_radius > MAX_NUMBER_OF_ENEMY_IN_APPROACH_RADIUS):
        ok = False
        print "rejecting approach_location due to number_of_enemy_within_radius = " + str(number_of_enemy_within_radius) + ", approach_location = " + str(approach_location)
    
    return ok

def getCubeApproachPathInfo(cube_approach_path, return_location, robot_location, zone, robot_locations, current_time):
    cube_location = cube_approach_path['cube_location']
    approach_location = cube_approach_path['approach_location']
    
    round_trip_time = estimateRoundTripTime(cube_location, approach_location, robot_location, return_location)
    risk = estimateRisk(cube_approach_path, robot_location, robot_locations, current_time)
    points_increase = getPointsIncrease(cube_location, zone)
    
    points_per_second = points_increase / round_trip_time
    
    score = points_per_second / risk
    
    info =  {'score': score, 'points_increase': points_increase, 'round_trip_time': round_trip_time}
    
    return info
    
def getPointsIncrease(cube_location, zone):
    start_points = 0
    finish_points = 2
    current_team_scoring = cube_location['team_scoring']
    current_corner = getCorner(cube_location)
    
    if (current_team_scoring == zone):
        
        if (current_corner == zone):
            start_points = 2
        
        else: 
            start_points = 1
    
    elif (current_team_scoring != None):
        
        if (current_corner == current_team_scoring):
            start_points = (- 2 / 3)
            
        else:
            start_points = (- 1 / 3)
    
    points_increase = finish_points - start_points
    
    return points_increase    

def getCorner(cube_location): #https://www.studentrobotics.org/resources/2016/rulebook.pdf
    x = cube_location['x']
    y = cube_location['y']
    
    corner = None
    
    if (y > (5.875 + x)):
        corner = 0
    
    elif (y > (13.875 - x)):
        corner = 1
    
    elif (y < (-5.875 + x)):
        corner = 2
        
    elif (y < (2.125 - x)):
        corner = 3
        
    return corner 
    
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

def estimateRisk(cube_approach_path, robot_location, robot_locations, current_time):
    return 1
    
def isLocationWithinArena(location, indent = (CUBE_WIDTH / 2)):
    
    within_arena = True
    
    x = location['x']
    y = location['y']
    
    if ((x > (8 - indent)) or (y > (8 - indent)) or (x < indent) or (y < indent)):
        within_arena = False
    return within_arena
    
def getNearestEnemyRobotDistanceToLocation(location, robot_locations, current_time):
    smallest_distance = STARTING_SMALLEST_DISTANCE
    
    for enemy_robot_location in robot_locations:
        distance = polar.getPolarR(location, enemy_robot_location)
        time_since_seen = current_time - enemy_robot_location['time']
        
        if ((distance < smallest_distance) and (time_since_seen < MAX_TIME_SINCE_ENEMY_SEEN)):
            smallest_distance = distance
    return smallest_distance
    
def getNumberOfEnemyRobotsWithinRadiusFromLocation(location, robot_locations, current_time, radius = ENEMY_ROBOT_RADIUS):
    number = 0
    
    for enemy_robot_location in robot_locations:
        distance = polar.getPolarR(location, enemy_robot_location)
        time_since_seen = current_time - enemy_robot_location['time']
        
        if ((time_since_seen < MAX_TIME_SINCE_ENEMY_SEEN) and (distance < radius)):
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