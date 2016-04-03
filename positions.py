#POSITIONS

# rotate +ve = roll the cube forwards like a front bike wheel rolling forwards
# lift +ve = arms up
# grab +ve = arms in
# time = time taken to move to the position


INITIALISATION = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 1}
ARMS_UP_OUT_THE_WAY = {'rotate': 0, 'lift': 100, 'grab': 0, 'time': 1}

ARMS_WIDE_POSITIVE_TURN = {'rotate': - 100, 'lift': - 40, 'grab': - 50, 'time': 1}
ARMS_ON_CUBE_POSITIVE_TURN = {'rotate': - 100, 'lift': - 40, 'grab': 30, 'time': 1}
LIFT_CUBE_POSITIVE_TURN = {'rotate': - 20, 'lift': 40, 'grab': 30, 'time': 1}
TURN_CUBE_90 = {'rotate': 80, 'lift': 40, 'grab': 30, 'time': 1}
DOWN_CUBE_90 = {'rotate': 40, 'lift': 0, 'grab': 30, 'time': 1}
RELEASE_CUBE_90 = {'rotate': 40, 'lift': 0, 'grab': 0, 'time': 1}

ARMS_WIDE_NEGATIVE_TURN = {'rotate': 20, 'lift': - 40, 'grab': - 50, 'time': 1}
ARMS_ON_CUBE_NEGATIVE_TURN = {'rotate': 20, 'lift': - 40, 'grab': 30, 'time': 1}
LIFT_CUBE_NEGATIVE_TURN = {'rotate': 100, 'lift': 40, 'grab': 30, 'time': 1}
TURN_CUBE_MINUS_90 = {'rotate': 0, 'lift': 40, 'grab': 30, 'time': 1}
DOWN_CUBE_MINUS_90 = {'rotate': - 40, 'lift': 0, 'grab': 30, 'time': 1}
RELEASE_CUBE_MINUS_90 = {'rotate': - 40, 'lift': 0, 'grab': 0, 'time': 1}

ARMS_WIDE_NEGATIVE_TURN = {'rotate': 60, 'lift': - 40, 'grab': - 50, 'time': 1}
ARMS_ON_CUBE_NEGATIVE_TURN = {'rotate': 60, 'lift': - 40, 'grab': 30, 'time': 1}
LIFT_CUBE_NEGATIVE_TURN = {'rotate': 100, 'lift': 40, 'grab': 30, 'time': 1}
TURN_CUBE_MINUS_180 = {'rotate': -60, 'lift': 40, 'grab': 30, 'time': 1}
DOWN_CUBE_MINUS_180 = {'rotate': -100, 'lift': 0, 'grab': 30, 'time': 1}
RELEASE_CUBE_MINUS_180 = {'rotate': -100, 'lift': 0, 'grab': 0, 'time': 1}