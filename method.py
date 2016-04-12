def decideCubeToApproach(a_cube_locations, b_cube_locations, c_cube_locations):
    
    selected_cube = a_cube_locations[0].deepcopy()
    selected_approach_location = selected_cube['approach'][0].deepcopy()
    selected_cube_net = 'A'
    
    cube_approach = {'x': selected_cube['x'], 'y': selected_cube['y'], 'z': selected_cube['z'], 'yaw': selected_cube['yaw'], 'pitch': selected_cube['pitch'], 'roll': selected_cube['roll']}
    cube_approach['approach_location'] = selected_approach_location
    cube_approach['net'] = selected_cube_net
    
    return cube_approach