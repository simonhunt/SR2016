#POSITIONS

# rotate +ve = roll the cube forwards like a front bike wheel rolling forwards
# lift +ve = arms up
# grab +ve = arms in
# time = time taken to move to the position


INITIALISATION = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 1}
ARMS_UP_OUT_THE_WAY = {'rotate': 0, 'lift': 100, 'grab': 0, 'time': 5}

ARMS_WIDE_90 = {'rotate': - 100, 'lift': - 40, 'grab': - 50, 'time': 5}
ARMS_ON_CUBE_90 = {'rotate': - 100, 'lift': - 40, 'grab': 30, 'time': 5}
LIFT_CUBE_90 = {'rotate': - 20, 'lift': 40, 'grab': 30, 'time': 5}
TURN_CUBE_90 = {'rotate': 80, 'lift': 40, 'grab': 30, 'time': 10}
DOWN_CUBE_90 = {'rotate': 40, 'lift': 0, 'grab': 30, 'time': 5}
RELEASE_CUBE_90 = {'rotate': 40, 'lift': 0, 'grab': 0, 'time': 5}

ARMS_WIDE_NEGATIVE_90 = {'rotate': 20, 'lift': - 40, 'grab': - 50, 'time': 5}
ARMS_ON_CUBE_NEGATIVE_90 = {'rotate': 20, 'lift': - 40, 'grab': 30, 'time': 5}
LIFT_CUBE_NEGATIVE_90 = {'rotate': 100, 'lift': 40, 'grab': 30, 'time': 5}
TURN_CUBE_NEGATIVE_90 = {'rotate': 0, 'lift': 40, 'grab': 30, 'time': 10}
DOWN_CUBE_NEGATIVE_90 = {'rotate': - 40, 'lift': 0, 'grab': 30, 'time': 5}
RELEASE_CUBE_NEGATIVE_90 = {'rotate': - 40, 'lift': 0, 'grab': 0, 'time': 5}

ARMS_WIDE_180 = {'rotate': 60, 'lift': - 40, 'grab': - 50, 'time': 5}
ARMS_ON_CUBE_180 = {'rotate': 60, 'lift': - 40, 'grab': 30, 'time': 5}
LIFT_CUBE_180 = {'rotate': 100, 'lift': 40, 'grab': 30, 'time': 5}
TURN_CUBE_180 = {'rotate': -60, 'lift': 40, 'grab': 30, 'time': 20}
DOWN_CUBE_180 = {'rotate': -100, 'lift': 0, 'grab': 30, 'time': 5}
RELEASE_CUBE_180 = {'rotate': -100, 'lift': 0, 'grab': 0, 'time': 5}

TEST_SEQUENCE_90 = [ARMS_WIDE_90, ARMS_ON_CUBE_90, LIFT_CUBE_90, TURN_CUBE_90, DOWN_CUBE_90, RELEASE_CUBE_90, ARMS_UP_OUT_THE_WAY]
TEST_SEQUENCE_NEGATIVE_90 = [ARMS_WIDE_NEGATIVE_90, ARMS_ON_CUBE_NEGATIVE_90, LIFT_CUBE_NEGATIVE_90, TURN_CUBE_NEGATIVE_90, DOWN_CUBE_NEGATIVE_90, RELEASE_CUBE_NEGATIVE_90, ARMS_UP_OUT_THE_WAY]
TEST_SEQUENCE_180 = [ARMS_WIDE_180, ARMS_ON_CUBE_180, LIFT_CUBE_180, TURN_CUBE_180, DOWN_CUBE_180, RELEASE_CUBE_180, ARMS_UP_OUT_THE_WAY]
