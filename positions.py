#POSITIONS

# rotate +ve = roll the cube forwards like a front bike wheel rolling forwards
# lift +ve = arms up
# grab +ve = arms in
# time = time taken to move to the position


INITIALISATION = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 1}
ARMS_UP_OUT_THE_WAY = {'rotate': 0, 'lift': 100, 'grab': 0, 'time': 1}

ARMS_WIDE_ZERO = {'rotate': 0, 'lift': - 40, 'grab': - 50, 'time': 1}
ARMS_ON_CUBE_ZERO = {'rotate': 0, 'lift': - 40, 'grab': 35, 'time': 2}
LIFT_CUBE_ZERO = {'rotate': 0, 'lift': 0, 'grab': 35, 'time': 1}
RELEASE_CUBE_ZERO = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 0.5}

ARMS_WIDE_90= {'rotate': - 100, 'lift': - 100, 'grab': - 70, 'time': 1}
ARMS_ON_CUBE_90 = {'rotate': - 100, 'lift': - 100, 'grab': 20, 'time': 2}
LIFT_CUBE_90 = {'rotate': - 100, 'lift': 60, 'grab': 20, 'time': 2}
TURN_CUBE_90 = {'rotate': 100, 'lift': 60, 'grab': 20, 'time': 2}
DOWN_CUBE_90 = {'rotate': 100, 'lift': -70, 'grab': 20, 'time': 1}
RELEASE_CUBE_90 = {'rotate': 100, 'lift': -70, 'grab': -20, 'time': 0.5}

ARMS_WIDE_NEGATIVE= {'rotate': 100, 'lift': - 100, 'grab': - 70, 'time': 1}
ARMS_ON_CUBE_NEGATIVE_90 = {'rotate': 100, 'lift': - 100, 'grab': 20, 'time': 2}
LIFT_CUBE_NEGATIVE_90 = {'rotate': 100, 'lift': 40, 'grab': 20, 'time': 2}
TURN_CUBE_NEGATIVE_90 = {'rotate': -30, 'lift': 40, 'grab': 20, 'time': 2}
DOWN_CUBE_NEGATIVE_90 = {'rotate': -80, 'lift': -50, 'grab': 20, 'time': 1}
RELEASE_CUBE_NEGATIVE_90 = {'rotate': -80, 'lift': -50, 'grab': -20, 'time': 0.5}

ARMS_ON_CUBE_180 = {'rotate': 100, 'lift': - 40, 'grab': 35, 'time': 2}
LIFT_CUBE_180 = {'rotate': 100, 'lift': 40, 'grab': 35, 'time': 2}
TURN_CUBE_180 = {'rotate': - 100, 'lift': 40, 'grab': 35, 'time': 2}
DOWN_CUBE_180 = {'rotate': - 100, 'lift': -35, 'grab': 35, 'time': 1}
RELEASE_CUBE_180 = {'rotate': - 100, 'lift': 0, 'grab': 0, 'time': 0.5}
PREPARE_SECOND_ROTATE_180 = {'rotate': 100, 'lift': - 40, 'grab': 0, 'time': 0.5}
ARMS_ON_CUBE_180_FAST = {'rotate': 100, 'lift': - 40, 'grab': 35, 'time': 0.5}

TEST_SEQUENCE_ZERO = [ARMS_WIDE_ZERO, ARMS_ON_CUBE_ZERO, LIFT_CUBE_ZERO, RELEASE_CUBE_ZERO]
TEST_SEQUENCE_90 = [ARMS_WIDE_90, ARMS_ON_CUBE_90, LIFT_CUBE_90, TURN_CUBE_90, DOWN_CUBE_90, RELEASE_CUBE_90, ARMS_UP_OUT_THE_WAY]
TEST_SEQUENCE_NEGATIVE_90 = [ARMS_WIDE_NEGATIVE, ARMS_ON_CUBE_NEGATIVE_90, LIFT_CUBE_NEGATIVE_90, TURN_CUBE_NEGATIVE_90, DOWN_CUBE_NEGATIVE_90, RELEASE_CUBE_NEGATIVE_90, ARMS_UP_OUT_THE_WAY]
TEST_SEQUENCE_180 = [ARMS_WIDE_NEGATIVE, ARMS_ON_CUBE_180, LIFT_CUBE_180, TURN_CUBE_180, DOWN_CUBE_180, RELEASE_CUBE_180, PREPARE_SECOND_ROTATE_180, ARMS_ON_CUBE_180_FAST, LIFT_CUBE_180, TURN_CUBE_NEGATIVE_90, DOWN_CUBE_NEGATIVE_90, RELEASE_CUBE_NEGATIVE_90, ARMS_UP_OUT_THE_WAY]
