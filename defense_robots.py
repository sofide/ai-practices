"""
Ejercicio: Robots defensivos secretos.

Se poseen dos robots para custodiar un centro de investigación secreto. Los robots
permanecen almacenados en espera, y frente a alguna emergencia deben reaccionar
ubicándose en posiciones defensivas. El centro de investigación posee habitaciones en
forma de grilla, pero algunas de ellas no son accesibles para los robots, por riesgo de
contaminación. Los robots sólo pueden moverse entre habitaciones adyacentes.

Se debe resolver la “puesta en defensiva” como un problema de búsqueda, con el objetivo
de encontrar el camino más óptimo.
------+-----+-----+-----+-----+
|     |R1 R2|  X  |     |  O  |
------+-----+-----+-----+-----+
|     |     |     |  X  |     |
------+-----+-----+-----+-----+
|     |  X  |     |     |     |
------+-----+-----+-----+-----+
|     |     |  O  |     |     |
------+-----+-----+-----+-----+


R1: Robot1
R2: Robot2

X: Habitación no accesible por los Robots
O: Ubicación objetivo

"""
from itertools import product

from simpleai.search import SearchProblem, breadth_first, depth_first, uniform_cost
from simpleai.search.viewers import WebViewer, ConsoleViewer


INITIAL_STATE = (
    (0, 1),  # Position of first robot
    (0, 1),  # Position of second robot
)

RESTRICTED_AREAS = {
    (0, 2),
    (1, 3),
    (2, 1),
}

OBJECTIVE_AREAS = {
    (0, 4),
    (3, 2),
}

ROWS = 4
COLUMNS = 5


class DefenseRobots(SearchProblem):
    def is_goal(self, state):
        # in sets the elements doesn't have order so this works for any robot to be
        # in any objective.
        # return set(state) == OBJECTIVE_AREAS

        # This other solution is a bit larger and less efficient but it can be more
        # explicit
        for objective in OBJECTIVE_AREAS:
            if objective not in state:
                return False

        return True

    def _get_adjacent_positions(self, position):
        row, column = position
        all_adjacent_positions = [
            (row, column - 1),  # move to the left
            (row, column + 1),  # move to the right
            (row - 1, column),  # move up
            (row + 1, column),  # move down
        ]

        valid_adjacent_positions = [
            position for position in all_adjacent_positions
            if -1 not in position
            and position[0] < ROWS
            and position[1] < COLUMNS
        ]

        return valid_adjacent_positions


    def actions(self, state):
        actions_for_each_robot = []

        reached_obj = []

        for robot_position in state:
            if robot_position in OBJECTIVE_AREAS and robot_position not in reached_obj:
                # don't move the robot if it is the first to arrive to an objective area
                robot_actions = [robot_position]
                reached_obj.append(robot_position)
            else:
                robot_actions = [
                    position
                    for position in self._get_adjacent_positions(robot_position)
                    if position not in RESTRICTED_AREAS
                ]

            actions_for_each_robot.append(robot_actions)

        return product(*actions_for_each_robot)


    def result(self, state, action):
        return action

    def cost(self, state1, action, state2):
        movements = 0
        for robot, original_position in enumerate(state1):
            if state2[robot] != original_position:
                movements += 1

        return movements

    def cost2(self, state1, action, state2):
        movement_costs = [
            1
            for original_position, final_position
            in zip(state1, state2)
            if original_position != final_position
        ]
        return sum(movement_costs)

    def print_state_representation(self, state):
        robot = "R"
        restricted_area = "X"
        objective_area = "O"

        matrix = []

        position_size = 5

        for row in range(ROWS):
            row_elements = []
            for column in range(COLUMNS):
                position = (row, column)
                elements_in_position = []
                for robot_position in state:
                    if robot_position == position:
                        elements_in_position.append(robot)
                if position in RESTRICTED_AREAS:
                    elements_in_position.append(restricted_area)

                if position in OBJECTIVE_AREAS:
                    elements_in_position.append(objective_area)

                row_elements.append(elements_in_position)

            matrix.append(row_elements)

        row_separation = "\n" + ("+" + ("-" * position_size)) * COLUMNS + "+" + "\n"
        column_separation = "|"

        representation = row_separation

        for row in matrix:
            representation += column_separation
            for position in row:
                elements = "".join(position).center(position_size)
                representation += elements + column_separation

            representation += row_separation

        print(representation)
        # return representation
