"""
El JPL (laboratorio de la NASA) desea rediseñar el algoritmo de control del robot que
hoy llega a Marte, el Perseverance. Para ello desean comenzar con una parte reducida del
problema: dado un mapa de sus alrededores, su posición y un conjunto de tareas a
realizar, determinar el orden adecuado de acciones a ejecutar para lograr todas las
tareas en el menor tiempo posible.

Lista de tareas a completar en esta simulación es la siguiente:

- Tomar 2 muestras de terreno de zonas interesantes geológicamente y separadas
(diferentes coordenadas en la grilla).
- Desplegar el helicóptero Ingenuity (una sola vez).

En el siguiente diagrama se puede ver la posición actual de Perseverance (P) y las
características del terreno en el que trabajará, donde el fondo con lineas (--) indica
que se trata de una región geológicamente “interesante”, y el simbolo "O" indica que es
una región con obstáculos que no permitiría desplegar el helicóptero.

------+-----+-----+-----+
|--O--|  O  |     |-----|
------+-----+-----+-----+
|     |     |  O  |     |
------+-----+-----+-----+
|-----|--O--|--O--|  P  |
------+-----+-----+-----+
|     |     |--O--|     |
------+-----+-----+-----+

Para completar sus tareas, en cada momento Perseverance puede ejecutar una de las
siguientes tareas:
- Moverse a una región adyacente (5 mins).
- Tomar una muestra de suelo, si se encuentra sobre suelo interesante geológicamente (10
mins).
- Desplegar el helicóptero Ingenuity, si se encuentra en una región lo suficientemente
despejada (3 mins).

Es importante aclarar que los picos no son obstáculo para el robot, puede moverse por
esas regiones sin problemas (posee la capacidad de evadirlos de forma autónoma).

a. Plantee formalmente como problema de búsqueda tradicional, con código y comentarios
explicativos.
b. Plantee una heurística para el mismo. No hace falta que sea muy precisa, pero debe
ser admisible.
c. Realice al menos 5 iteraciones de búsqueda A*. Por cada iteración especifique los
odos de la frontera, con sus estados, el valor de f asociado a cada nodo, y el nodo
elegido.
"""
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    astar,
    greedy,
    iterative_limited_depth_first,
)

from utils import print_grid, try_search_method


# State = (robot position, positions of samples taken, helicopter lauched)
INITIAL_STATE = ((2, 3), (), 0)

OBSTACLES = [(0, 0), (0, 1), (1, 2), (2, 1), (2, 2), (3, 2)]
INTERESTING_ZONES = [(0, 0), (0, 3), (2, 0), (2, 1), (2, 2), (3, 2)]

MOVE = "move"
TAKE_SAMPLE = "take_sample"
LAUNCH_HELICOPTER = "launch_helicopter"

TIMES = {MOVE: 5, TAKE_SAMPLE: 10, LAUNCH_HELICOPTER: 3}


class PerseveranceProblem(SearchProblem):
    def is_goal(self, state):
        _, samples, helicopter_launched = state
        return (len(samples), helicopter_launched) == (2, 1)

    def actions(self, state):
        (row, column), samples, helicopter_launched = state
        # an action can be a coordinate (if the robot decide to move), or a string if
        # it decide to take a sample or launch the helicopter.
        posible_actions = []
        if row != 0:
            posible_actions.append((row-1, column))  # move up
        if row != 3:
            posible_actions.append((row+1, column))  # move down
        if column != 0:
            posible_actions.append((row, column-1))  # move left
        if column != 3:
            posible_actions.append((row, column+1))  # move right

        if len(samples) < 2 and (row, column) in INTERESTING_ZONES and (row, column) not in samples:
            posible_actions.append(TAKE_SAMPLE)

        if not helicopter_launched and (row, column) not in OBSTACLES:
            posible_actions.append(LAUNCH_HELICOPTER)

        return posible_actions

    def result(self, state, action):
        position, samples, helicopter_launched = state

        if action == TAKE_SAMPLE:
            samples = list(samples)
            samples.append(position)
            samples = tuple(samples)
            return position, samples, helicopter_launched

        if action == LAUNCH_HELICOPTER:
            return position, samples, 1

        return action, samples, helicopter_launched

    def cost(self, state, action, state_2):
        if isinstance(action, tuple):
            action = MOVE

        return TIMES[action]

    def heuristic(self, state):
        position, samples, launched = state

        pending_samples = len(samples) - 2
        estimated_cost = pending_samples * TIMES[TAKE_SAMPLE]

        if pending_samples and (position in samples or position not in INTERESTING_ZONES):
            # at least one extra movement before next sample taken
            estimated_cost += TIMES[MOVE]

        if pending_samples == 2:
            # if both samples are pending, is needed a movement between them
            estimated_cost += TIMES[MOVE]

        if not launched:
            estimated_cost += TIMES[LAUNCH_HELICOPTER]

        return estimated_cost

    def print_state_representation(self, state):
        position, samples, helicopter_launched = state
        if helicopter_launched:
            robot_symbol = "R"
        else:
            robot_symbol = "RH"

        elements = {
            "X": INTERESTING_ZONES,
            "O": OBSTACLES,
            "S": samples,
            robot_symbol: [position],
        }

        print_grid(4, 4, elements)


methods = (
    # breadth_first,
    # depth_first,
    # iterative_limited_depth_first,
    # uniform_cost,
    # greedy,
    astar,
)

for search_method in methods:
    try_search_method(search_method, PerseveranceProblem, INITIAL_STATE)

