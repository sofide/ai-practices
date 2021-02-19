"""
TEORIA


1.a) Dinámico: el ambiente puede cambiar independientemente de las acciones que se
decidan efectuar. Por ejemplo: en el problema del auto que se maneja solo el ambiente
es dinamico porque hay cosas que suceden de las que no tenemos control, por ejemplo
peatones cruzando la calle, más autos, etc.

1.b) No observable: un ambiente es no observable cuando hay caracterísitcas del ambiente
que no podemos percibir. Por ejemplo, en el problema de la aspiradora en el caso de que
no se tengan sensores para observar si la habitación está sucia o no ni se sepa donde
está la aspiradora.

1.c) Determinístico: un ambiente es deterministico cuando los resultados de las acciones
se conocen con exactitud. Ej: el problema de la aspiradora siempre que estemos seguros
de que cuando ejecutamos la accion "mover izquierda" la aspiradora siempre va a terminar
en el casillero de la izquierda, y cuando se ejecuta la accion "aspirar" siempre vamos
a obtener como resultado la habitación limpia.


2) El programa agente, es el encargado de medir las percepciones por medio de los
sensores, consultar a la función agente y ejecutar la acción correspondiente.

La función agente es la que recibe los datos de las percepciones y decide que acción
ejecutar.


3) Un agente basado en modelos lleva un estado interno que depende de las percepciones
observadas en cada paso. En cambio, el agente basado en metas decide que acciones tomar
solamente observando el estado actual, comprobando si el mismo es un estado meta o no.

DISCLAIMER: Acá tengo que reconocer que miré un cuaderno donde tenía anotado esto, porque
al principio era más aplicada y tomaba nota, pero les RE RE RE JURO que solo en esta espié
jaja 😇


4) Los componentes principales de un nodo son: Estado, referencia al Nodo padre y costo
acumulado. También puede tener referencias a los nodos hijos y una identificación de si
su estado es un estado meta o no.

5) c -> La lista cerrada de un algoritmo de búsqueda en grafo contine los estados
visitados.

6) b -> El consumo de memoria del algoritmo de busqueda en profundidad es O(bm).

7) A* es optimamente eficiente porque garantiza encontrar la solución menos costosa (si
existe) en la menor cantidad de pasos posible.

Hay algoritmos que en algunos casos pueden encontrar la solución optima en menos pasos,
pero no pueden garantizar que SIEMPRE van a enconntrar la solución óptima en la menor
cantidad de pasos.

8) c -> Si hacemos "Búsqueda de haz local" con k=1 es lo mismo que ascenso de colina.

9) Las ventajas de plantear un problema como csp en lugar de plantearlo como problema
de búsqueda son:
- Ahorro en memoria: No mantiene en memoria el historial de "pasos" hasta llegar a la
solución.
- Existen heurísticas genéricas que es posible usar, sin tener que pensar una herurísica
específica para un problema en particular.

10) La propagación de restricciones es el paso siguiente a la asignación de un valor
a una determinada variable, y tiene que ver con eliminar del dominio de las demás
variables los valores que violen alguna restricción relacionada al valor elegido.

En backtracking search este paso es importante para garantizar que, si se encuentra
una solución, la misma no va a violar ninguna restricción.
"""


"""
PRACTICA


BUSQUEDA
Armado de cohetes
Se desea programar un robot capaz de transportar todas las piezas necesarias para ensamblar un cohete en el menor
tiempo posible, incluyendo los satélites que van a ser lanzados, transportando dichas partes desde un depósito cercano
hasta el edificio de ensamblado. Las diferentes partes son más o menos delicadas, y la velocidad de movimiento del
robot debe estar limitada de acuerdo a qué tan delicada es cada pieza. El robot permite cargar más de una pieza a la vez,
pero al hacerlo siempre la pieza más delicada es la que determina la velocidad de movimiento del robot. Y además solo
puede llevar hasta 2 piezas que no sumen más de 8 toneladas juntas, por su capacidad de carga limitada. Las piezas a
transportar son:

● La estructura de la primera fase, que por su gran
tamaño no debería ser movida a más de 10km/h, y pesa 7
toneladas.
● La estructura de la segunda fase, que como es un poco
más chica puede ser llevada a hasta 15km/h, y pesa 3
toneladas.

● La estructura de la tercera fase, que puede llevarse hasta la velocidad máxima (20km/h) del robot y pesa 1
tonelada.
● 2 satélites, que por su extrema delicadeza solo pueden moverse a 5km/h. Uno de ellos pesa 0.5 toneladas y el
otro 1.5 toneladas.

+-----------------------+    60 km    +----------+
| Edificio de ensambado | <---------> | Depósito |
+-----------------------+             +----------+

Es importante recordar que el robot debe volver al depósito luego de cada ida al edificio de ensamblado, y en dichos
viajes puede moverse a su máxima velocidad (20km/h).
a. Defina formalmente el problema para ser resuelto mediante búsqueda. Escriba código Python y donde
considere necesario agregue comentarios que esclarezcan el funcionamiento del código.
b. Plantee y programe una heurística admisible para ser utilizada en este problema (no importa la calidad de la
misma).
c. Resuelva 5 iteraciones mediante búsqueda A* considerando la heurística planteada en b. Indique en cada
iteración la frontera al iniciar la iteración, y el nodo elegido. Para cada nodo es necesario indicar qué estado
contiene, el costo acumulado y el valor de la heurística.
"""
from itertools import combinations

MAX_WEIGHT = 8

FIRST_STAGE = "first_stage"
SECOND_STAGE = "second_stage"
THIRD_STAGE = "third_stage"
SATELLITE_ONE = "satellite_one"
SATELLITE_TWO = "satellite_two"

DISTANCE_BETWEEN_BUILDINGS = 60  # Km
MAX_ROBOT_VELOCITY = 20  # Km / h
TIME_IN_MAX_VELOCITY = DISTANCE_BETWEEN_BUILDINGS / MAX_ROBOT_VELOCITY

PIECES_WEIGHT = {
    FIRST_STAGE: 7,
    SECOND_STAGE: 3,
    THIRD_STAGE: 1,
    SATELLITE_ONE: 0.5,
    SATELLITE_TWO: 1.5,
}

PIECES_MAX_VELOCITY = {
    FIRST_STAGE: 10,
    SECOND_STAGE: 15,
    THIRD_STAGE: 20,
    SATELLITE_ONE: 5,
    SATELLITE_TWO: 5,
}


PIECES_TIME_TO_MOVE = {
    piece: DISTANCE_BETWEEN_BUILDINGS / PIECES_MAX_VELOCITY[piece]
    for piece in PIECES_MAX_VELOCITY
}

# ((pieces in ensamble building), (pieces in storage))
INITIAL_STATE = ((), (FIRST_STAGE, SECOND_STAGE, THIRD_STAGE, SATELLITE_ONE, SATELLITE_TWO))


class RocketProblem(SearchProblem):
    def is_goal(state):
        _, pieces_pending_to_move = state

        return pieces_pending_to_move ==  ()

    def actions(state):
        _, pieces_pending_to_move = state

        # movements of one piece
        posible_actions = [(piece,) for piece in pieces_pending_to_move]

        # movements of two pieces
        posible_actions.extend(
            piece_a, piece_b
            for piece_a, piece_b in combinations(pieces_pending_to_move, 2)
            if PIECES_WEIGHT[piece_a] + PIECES_WEIGHT[piece_b] <= MAX_WEIGHT
        )

        return posible_actions

    def result(state, action):
        pieces_in_ensamble, pieces_in_storage = state

        pieces_in_ensamble = list(pieces_in_ensamble)
        pieces_in_ensamble.extend(action)

        pieces_in_storage = [piece for piece in pieces_in_storage if piece not in action]

        return tuple(pieces_in_ensamble), tuple(pieces_in_storage)

    def cost(state, action, state2):
        movement_time = max(PIECES_TIME_TO_MOVE[piece] for piece in action)

        if not is_goal(state2):
            movement_time += TIME_IN_MAX_VELOCITY

        return movement_time


    def heuristic(state):
        _, pieces_pending_to_move = state

        if not pieces_pending_to_move:
            return 0

        # max movement time of the pieces pending to move
        estimated_time = max(PIECES_TIME_TO_MOVE[piece] for piece in pieces_pending_to_move)

        if len(pieces_pending_to_move) > 2:
            estimated_time += TIME_IN_MAX_VELOCITY

        return estimated_time



"""
Resolucioón con A*

f1 = estructura de la primera fase
f2 = estructura de la segund fase
f3 = estructura de la tercera fase
s1 = satelite 1
s2 = satelite 2


VELOCITIES:
    FIRST_STAGE: 10,
    SECOND_STAGE: 15,
    THIRD_STAGE: 20,
    SATELLITE_ONE: 5,
    SATELLITE_TWO: 5,


TIME TO MOVE:
    FIRST_STAGE: 6,
    SECOND_STAGE: 4,
    THIRD_STAGE: 3,
    SATELLITE_ONE: 12,
    SATELLITE_TWO: 12,


TIME IN MAX VELOCITY: 3


Nombre | Padre | Estado                     | Costo Acum | Heuristica        | Coso Ac + Heuristica
-------+-------+----------------------------+------------+-------------------+---------------------
N1     |       | (), (f1, f2, f3, s1, s2)   |            |  15               | 15
N2     |  N1   | (f1,), (f2, f3, s1, s2)    | 3+6  =  9  |  15               | 24
N3     |  N1   | (f2,), (f1, f3, s1, s2)    | 3+4  =  7  |  15               | 22
N4     |  N1   | (f3,), (f1, f2, s1, s2)    | 3+3  =  6  |  15               | 21
N5     |  N1   | (s1,), (f1, f2, f3, s2)    | 3+12 =  15 |  15               | 30
N6     |  N1   | (s2,), (f1, f2, f3, s1)    | 3+12 =  15 |  15               | 30
N7     |  N1   | (f1, f2), (f3, s1, s2)     | 3+6  =  9  |  15               | 24
N8     |  N1   | (f1, f3), (f2, s1, s2)     | 3+6  =  9  |  15               | 24
N9     |  N1   | (f1, s1), (f2, f3, s2)     | 3+12 =  15 |  15               | 30
N10    |  N1   | (f1, s2), (f2, f3, s1)     | 3+12 =  15 |  15               | 30
N12    |  N1   | (f2, f3), (f1, s1, s2)     | 3+4  =  7  |  15               | 22
N13    |  N1   | (f2, s1), (f1, f3, s2)     | 3+12 =  15 |  15               | 30
N14    |  N1   | (f2, s2), (f1, f3, s1)     | 3+12 =  15 |  15               | 30
N15    |  N1   | (f3, s1), (f1, f2, s2)     | 3+12 =  15 |  15               | 30
N16    |  N1   | (f3, s2), (f1, f2, s1)     | 3+12 =  15 |  15               | 30
N17    |  N1   | (s1, s2), (f1, f2, f3)     | 3+12 =  15 |  9                | 24

N18    |  N4   | (f3, f1), (f2, s1, s2)     | 6+6  =  12 |  15               | 27
N19    |  N4   | (f3, f2), (f1, s1, s2)     | 6+4  =  10 |  15               | 25
N20    |  N4   | (f3, s1), (f1, f2, s2)     | 6+12 =  18 |  15               | 33
N21    |  N4   | (f3, s2), (f1, f2, s1)     | 6+12 =  18 |  15               | 33
N22    |  N4   | (f3, f1, f2), (s1, s2)     | 6+6  =  12 |  15               | 27
N23    |  N4   | (f3, f1, s1), (f2, s2)     | 6+12 =  18 |  15               | 33
N24    |  N4   | (f3, f1, s2), (f2, s1)     | 6+12 =  18 |  15               | 33
N25    |  N4   | (f3, f2, s1), (f1, s2)     | 6+12 =  18 |  15               | 33
N26    |  N4   | (f3, f2, s2), (f1, s1)     | 6+12 =  18 |  15               | 33
N27    |  N4   | (f3, s1, s2), (f1, f2)     | 6+12 =  18 |  9                | 27

N28    |  N3   | (f2, f1), (f3, s1, s2)    | 7+6  =  13 |  15               | 28
N29    |  N3   | (f2, f3), (f1, s1, s2)    | 7+3  =  10 |  15               | 25
N30    |  N3   | (f2, s1), (f1, f2, s2)    | 7+12 =  19 |  15               | 34
N31    |  N3   | (f2, s2), (f1, f2, s1)    | 7+12 =  19 |  15               | 34
N32    |  N3   | (f2, f1, f3), (s1, s2)    | 7+6  =  13 |  15               | 28
N33    |  N3   | (f2, f1, s1), (f3, s2)    | 7+12 =  19 |  15               | 34
N34    |  N3   | (f2, f1, s2), (f3, s1)    | 7+12 =  19 |  15               | 34
N35    |  N3   | (f2, f3, s1), (f1, s2)    | 7+12 =  19 |  15               | 34
N36    |  N3   | (f2, f3, s2), (f1, s1)    | 7+12 =  19 |  15               | 34
N37    |  N3   | (f2, s1, s2), (f1, f3)    | 7+12 =  19 |  9                | 28

N38    |  N12  | (f2, f3, f1), (s1, s2)    | 7+6  =  13 |  15               | 28
N39    |  N12  | (f2, f3, s1), (f1, s2)    | 7+12 =  19 |  15               | 34
N40    |  N12  | (f2, f3, s2), (f1, s1)    | 7+12 =  19 |  15               | 34
N41    |  N12  | (f2, f3, f1, s1), (s2)    | 7+12 =  19 |  15               | 34
N42    |  N12  | (f2, f3, f1, s2), (s1)    | 7+12 =  19 |  15               | 34
N43    |  N12  | (f2, f3, s1, s2), (f1)    | 7+12 =  19 |  9                | 28


FRONTERA                                 | Nodo elegido | Es meta? | Hijos
-----------------------------------------+--------------+----------+-------
N1                                       |   N1         |   no     | N2, N3, N4, N5, N6, N7, N8, N9
                                         |              |          | N10, N11, N12, N13, N14, N15, N16, N17
                                         |              |          | (menos los que superan la restriccion de peso :P)
-----------------------------------------+--------------+----------+-------
N4, N3, N12, N17, N2, N7, N8, N5, N6, N9 |   N4         |   no     | N18, N19, N20, N21, N22, N23, N24
N10, N13, N14, N15, N16                  |              |          | N25, N26, N27
(menos los que superan el peso max)      |              |          | (menos los que superan la restriccion de peso :P)
-----------------------------------------+--------------+----------+-------
[22 N3, N12], [24 N17, N2, N7, N8], [25  |   N3         |   no     | N28 .... N37
N19], [27 N18, N22, N27], [30 N5, N6, N9,|              |          |
N10, N13, N14, N15, N16], [33 N20, N21,  |              |          |
N23, N24, N25, N26]                      |              |          |
(menos los que superan el peso max)      |              |          | (menos los que superan la restriccion de peso :P)
-----------------------------------------+--------------+----------+-------
[22     N12], [24 N17, N2, N7, N8], [25  |   N12        |   no     | N38 .... N43
N19], [27 N18, N22, N27], [30 N5, N6, N9,|              |          |
N10, N13, N14, N15, N16], [33 N20, N21,  |              |          |
N23, N24, N25, N26]  + [N28 .... N37 ]   |              |          |
sorted                                   |              |          |
(menos los que superan el peso max)      |              |          | (menos los que superan la restriccion de peso :P)
-----------------------------------------+--------------+----------+-------
              [24 N17, N2, N7, N8], [25  |   N17        |   no     | ....
N19], [27 N18, N22, N27], [30 N5, N6, N9,|              |          |
N10, N13, N14, N15, N16], [33 N20, N21,  |              |          |
N23, N24, N25, N26]  + [N28 .... N37 ]   |              |          |
+ [N38 .... N43 ] sorted
(menos los que superan el peso max)      |              |          | (menos los que superan la restriccion de peso :P)
-----------------------------------------+--------------+----------+-------




CSP
"""
S1 = "S1"
S2 = "S."
S3 = "S3"
MS1 = "MS1"
MS2 = "MS2"

ARABSAT3 = "arabsat-3"
BIOSAT8 = "biosat8"
COMSAT10 = "comsat10"
MICROCOMSAT20 = "microcomsat2"
NUSAT6 = "nusat6"
RADARSAT1 = "radarsat1"
SUPERSAT1 = "supersat1"
TESTSAT1 = "testsat1"
XSAT42 = "xsat42"

SATES_WEIGHT = {
    ARABSAT3: 300,
    BIOSAT8: 60,
    COMSAT10: 700,
    MICROCOMSAT20: 80,
    NUSAT6: 40,
    RADARSAT1: 400,
    SUPERSAT1: 500,
    TESTSAT1: 30,
    XSAT42: 600,
}
MAX_WEIGHT = 1500  # kg

MICRO_SATES = [BIOSAT8, MICROCOMSAT20, NUSAT6, TESTSAT1]
SLOTS_WITH_MICRO_SATE_ONLY = [MS1, MS2]

SATES_ONLY_IN_S3 = [RADARSAT1, SUPERSAT1]


VARIABLES = [S1, S2, S3, MS1, MS2]

DOMAINS = {
    slot: MICRO_SATES
    for slot in SLOTS_WITH_MICRO_SATE_ONLY
}

DOMAINS[S3] = list(SATES_WEIGHT.keys())

SATES_THAT_CAN_BE_ANYWHERE = [sate for sate in SATES_WEIGHT if sate not in SATES_ONLY_IN_S3]

DOMAINS.update([
    (slot, SATES_THAT_CAN_BE_ANYWHERE)
    for slot in VARIABLES
    if slot != S3
    and slot not in SLOTS_WITH_MICRO_SATE_ONLY
])

CONSTRAINTS = []

def max_weight(variables, values):
    weight = sum(SATES_WEIGHT[sate] for sate in values)

    weight <= MAX_WEIGHT

CONSTRAINTS.append((VARIABLES, max_weight))


CEIL_SLOT = {
    S1: MS1,  # the ceil of S1 is MS1
    S2: MS2,
    MS1: S3,
    MS2: S3,
}


def testsat1_not_above_normal(variables, values):
    bottom_sate, top_sate = values

    if top_sate == TESTSAT1 and bottom_sate not in MICRO_SATES:
        return False

    return True


def microsat20_not_above_xsat42(variables, values):
    bottom_sate, top_sate = values

    if top_sate == MICROCOMSAT20 and bottom_sate == XSAT42:
        return False

    return True


for bottom_sate, top_sate in CEIL_SLOT.items():
    CONSTRAINTS.extend(
        ((bottom_sate, top_sate), testsat1_not_above_normal),
        ((bottom_sate, top_sate), microsat20_not_above_xsat42),
    )
