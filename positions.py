#POSITIONS

# rotate +ve = roll the cube forwards like a front bike wheel rolling forwards
# lift +ve = arms up
# grab +ve = arms in
# time = time taken to move to the position


INITIALISATION = {'rotate': 0, 'lift': 0, 'grab': 0, 'time': 1}
ARMS_UP_OUT_THE_WAY = {'rotate': 0, 'lift': 100, 'grab': - 75, 'time': 1}

ARMS_WIDE_ZERO = {'rotate': 0, 'lift': - 100, 'grab': - 70, 'time': 1}
ARMS_ON_CUBE_ZERO = {'rotate': 0, 'lift': - 100, 'grab': 30, 'time': 2}
LIFT_CUBE_ZERO = {'rotate': 80, 'lift': 0, 'grab': 30, 'time': 1}
RELEASE_CUBE_ZERO = {'rotate': 80, 'lift': 0, 'grab': -20, 'time': 0.5}

ARMS_WIDE_90 = {'rotate': - 100, 'lift': - 80, 'grab': - 70, 'time': 1}
ARMS_ON_CUBE_90 = {'rotate': - 100, 'lift': - 80, 'grab': 30, 'time': 2}
LIFT_CUBE_90 = {'rotate': - 100, 'lift': 80, 'grab': 30, 'time': 2}
TURN_CUBE_90 = {'rotate': 100, 'lift': 80, 'grab': 30, 'time': 2}
DOWN_CUBE_90 = {'rotate': 100, 'lift': -20, 'grab': 30, 'time': 1}
RELEASE_CUBE_90 = {'rotate': 100, 'lift': -20, 'grab': -20, 'time': 0.5}

ARMS_WIDE_NEGATIVE= {'rotate': 100, 'lift': - 50, 'grab': - 70, 'time': 1}
ARMS_ON_CUBE_NEGATIVE_90 = {'rotate': 100, 'lift': - 50, 'grab': 30, 'time': 2}
LIFT_CUBE_NEGATIVE_90 = {'rotate': 100, 'lift': 60, 'grab': 30, 'time': 2}
TURN_CUBE_NEGATIVE_90 = {'rotate': 10, 'lift': 60, 'grab': 30, 'time': 2}
DOWN_CUBE_NEGATIVE_90 = {'rotate': -80, 'lift': -10, 'grab': 30, 'time': 1}
RELEASE_CUBE_NEGATIVE_90 = {'rotate': -80, 'lift': -10, 'grab': -20, 'time': 0.5}

ARMS_ON_CUBE_180 = {'rotate': 100, 'lift': - 70, 'grab': 30, 'time': 2}
LIFT_CUBE_180 = {'rotate': 100, 'lift': 40, 'grab': 30, 'time': 2}
TURN_CUBE_180 = {'rotate': - 100, 'lift': 40, 'grab': 30, 'time': 2}
DOWN_CUBE_180 = {'rotate': - 100, 'lift': -35, 'grab': 30, 'time': 1}
RELEASE_CUBE_180 = {'rotate': - 100, 'lift': 0, 'grab': -20, 'time': 0.5}
PREPARE_SECOND_ROTATE_180 = {'rotate': 100, 'lift': - 40, 'grab': -20, 'time': 0.5}
ARMS_ON_CUBE_180_FAST = {'rotate': 100, 'lift': - 50, 'grab': 30, 'time': 0.5}

TEST_SEQUENCE_ZERO = [ARMS_WIDE_ZERO, ARMS_ON_CUBE_ZERO, LIFT_CUBE_ZERO, RELEASE_CUBE_ZERO]
TEST_SEQUENCE_90 = [ARMS_WIDE_90, ARMS_ON_CUBE_90, LIFT_CUBE_90, TURN_CUBE_90, DOWN_CUBE_90, RELEASE_CUBE_90, ARMS_UP_OUT_THE_WAY]
TEST_SEQUENCE_180 = [ARMS_WIDE_NEGATIVE, ARMS_ON_CUBE_180, LIFT_CUBE_180, TURN_CUBE_180, DOWN_CUBE_180, RELEASE_CUBE_180, PREPARE_SECOND_ROTATE_180, ARMS_ON_CUBE_180_FAST, LIFT_CUBE_180, TURN_CUBE_NEGATIVE_90, DOWN_CUBE_NEGATIVE_90, RELEASE_CUBE_NEGATIVE_90, ARMS_UP_OUT_THE_WAY]
TEST_SEQUENCE_NEGATIVE_90 = [ARMS_WIDE_NEGATIVE, ARMS_ON_CUBE_NEGATIVE_90, LIFT_CUBE_NEGATIVE_90, TURN_CUBE_NEGATIVE_90, DOWN_CUBE_NEGATIVE_90, RELEASE_CUBE_NEGATIVE_90, ARMS_UP_OUT_THE_WAY]

PHASE_0_ZERO = [ARMS_WIDE_ZERO]
PHASE_1_ZERO = [ARMS_ON_CUBE_ZERO, LIFT_CUBE_ZERO]
PHASE_2_ZERO = []
PHASE_3_ZERO = [RELEASE_CUBE_ZERO, ARMS_UP_OUT_THE_WAY]
PHASES_ZERO = [PHASE_0_ZERO, PHASE_1_ZERO, PHASE_2_ZERO, PHASE_3_ZERO]

PHASE_0_90 = [ARMS_WIDE_90]
PHASE_1_90 = [ARMS_ON_CUBE_90, LIFT_CUBE_90]
PHASE_2_90 = [TURN_CUBE_90]
PHASE_3_90 = [DOWN_CUBE_90, RELEASE_CUBE_90, ARMS_UP_OUT_THE_WAY]
PHASES_90 = [PHASE_0_90, PHASE_1_90, PHASE_2_90, PHASE_3_90]

PHASE_0_180 = [ARMS_WIDE_NEGATIVE]
PHASE_1_180 = [ARMS_ON_CUBE_180, LIFT_CUBE_180]
PHASE_2_180 = [TURN_CUBE_180]
PHASE_3_180 = [DOWN_CUBE_180, RELEASE_CUBE_180, PREPARE_SECOND_ROTATE_180, ARMS_ON_CUBE_180_FAST, LIFT_CUBE_180, TURN_CUBE_NEGATIVE_90, DOWN_CUBE_NEGATIVE_90, RELEASE_CUBE_NEGATIVE_90, ARMS_UP_OUT_THE_WAY]
PHASES_180 = [PHASE_0_180, PHASE_1_180, PHASE_2_180, PHASE_3_180]

PHASE_0_NEGATIVE_90 = [ARMS_WIDE_NEGATIVE]
PHASE_1_NEGATIVE_90 = [ARMS_ON_CUBE_NEGATIVE_90, LIFT_CUBE_NEGATIVE_90]
PHASE_2_NEGATIVE_90 = [TURN_CUBE_NEGATIVE_90]
PHASE_3_NEGATIVE_90 = [DOWN_CUBE_NEGATIVE_90, RELEASE_CUBE_NEGATIVE_90, ARMS_UP_OUT_THE_WAY]
PHASES_NEGATIVE_90 = [PHASE_0_NEGATIVE_90, PHASE_1_NEGATIVE_90, PHASE_2_NEGATIVE_90, PHASE_3_NEGATIVE_90]

PHASES = {0: PHASES_ZERO, 90: PHASES_90, 180: PHASES_180, - 90: PHASES_NEGATIVE_90}

