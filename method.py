import copy

import polar

MAX_TIME_SINCE_ENEMY_SEEN = 5 #seconds
STARTING_SMALLEST_DISTANCE = 8 #seconds
ENEMY_ROBOT_RADIUS = 2.5 #meters

def decideCubeToApproach(a_cube_locations, b_cube_locations, c_cube_locations, robot_location = 0, robots = 0, current_time = 0):
    
    selected_cube = copy.deepcopy(a_cube_locations[0])
    selected_approach_location = copy.deepcopy(selected_cube['approach'][1])
    selected_cube_net = 'A'
    
    cube_approach = {'x': selected_cube['x'], 'y': selected_cube['y'], 'z': selected_cube['z'], 'yaw': selected_cube['yaw'], 'pitch': selected_cube['pitch'], 'roll': selected_cube['roll']}
    cube_approach['approach_location'] = selected_approach_location
    cube_approach['net'] = selected_cube_net
    
    return cube_approach
    
    
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
    
def isLocationWithinArena(location, indent = 0):
    
    within_arena = True
    
    x = location['x']
    y = location['y']
    
    if ((x > (8 - indent)) or (y > (8 - indent)) or (x < indent) or (y < indent):
        within_arena = False
    return within_arena
        
    
        

'''
min dist to enemy robot
distance to zone
distance to bot
distance to bot + distance to zone?
number of enemy robots in x radius
too near edges
not right way up
top face
not on the floor
'''