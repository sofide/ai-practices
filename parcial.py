"""
TEORIA
1.a) Un ambiente estocastico es aquel en el cual los resultados de las acciones
se conocen con certeza.
Por ejemplo en el problema de las 8 reinas, dada la accion mover la reina_x a
la prosición_y sabemos exactamente que el resultado de esa acción va a tener a la
reina_x en la prosición_y

1.b) Un ambiente es completamente observable cuando tenemos conocimiento del estado completo
Por ejemplo, en el problema de la aspiradora podemos decir que es completamente observable solo si
conocemos en todo momento cuales son los lugares sucios y donde se encuentra la aspiradora

1.c) Un ambiente o problem es secuencial cuando se resuelve en diferentes pasos pasando
por diferentes estados relacionados entre sí.  Por ejemplo: una partida de ajedrez teniendo
en cuenta cada jugada como posible paso o secuencia.

2) Un agente reflejo simple tiene mapeadas las acciones a tomar para cada posible observacion.
mientras que un agente basado en modelos decide que acciones tomar en base a distintas
condiciones, llevando en memoria una representación del estado general (no solo de lo
observado en cada iteración).

Una situación resoluble por el segundo es por ejemplo un auto que se maneja solo, y tiene
que observar adelante y atrás antes de decidir si puede girar/avanzar/frenar/etc.

3) La racionalidad depende de que la resolución de un problema sea completa y no viole
ninguna restriccion (??????)

4) La solución de un problema de búsqueda  es una suceción de acciones que partiendo
de un estado inicial pueden llegar a un estado meta. Para que una solución sea optima
debe llegar a un estado meta con el menor costo posible.

5) Medidas para comparar performance:
    - (d) la distancia máxima entre dos nodos
    - (b) el factor de bifurcación
    - (m) la altura mínima donde se puede encontrar un estado meta
    - ...
    Con estas medidas se pueden calcular:
    - Complejidad espacial: mide cuánto ocupa como máximo el problema en memoria
    - Complejidad temporal: mide cuantas iteraciones como máximo puede demorar en
    encontrar una solución

6) Respuesta correcta: O(b**m) el factor de  bifurcación elevado a la altura minima de la meta

7) Para ser admisible una heuristica debe cumplir dos condiciones:
- No sobreestimar
- No perder información (heuristica de nodo <= costo_de_ir_a_nodo_hijo + heuristica_de_nodo_hijo)

Si no se utiliza una heuristica admisible en A*, esta estrategia puede no encontrar
la solución más óptima.


8) La mayor diferencia es que la búsqueda por haz local se puede quedar "trabada" en un
mínimo local.

9) Para resolver un problema de CSP es necesario definir las variables, sus posibles
dominios (o valores) y las restricciones.

Se considera solución a la asignación de valores a las variables.

Una solución es completa cuando todas las variables tienen asignado un valor y es
consistente cuando esa asignación no viola ninguna restricción.


10) Dos heuristicas genericas usadas en csp (voy a inventar porque no me acuerdo)
- cantidad de variables no asignadas (puede ser utilizada en estrategias como backtracking)
- cantidad de restricciones violadas (puede ser utilizada en estrategias como min_conflicts)






PRACTICA
"""
DORMITORIO = "dormitorio"
LIVING = "living"
ENTRADA = "entrada"
BAÑO = "baño"
COMEDOR = "comedor"

MOVER = "mover"
APAGAR = "apagar"


ROOM_CONNECTIONS = {
    DORMITORIO: [LIVING],
    LIVING: [DORMITORIO, COMEDOR, ENTRADA],
    ENTRADA: [LIVING],
    BAÑO: [COMEDOR],
    COMEDOR: [BAÑO, LIVING],
}


INITIAL_STATE = (
    # el primer elemento es donde está el bombero
    ENTRADA,
    # el segundo elemento es una tupla de habitaciones
    (
        # cada habitación tiene el nombre y los segundos que le lleva apagar el fuego que tenga
        (DORMITORIO, 10),
        (LIVING, 10),
        (ENTRADA, 0),
        (BAÑO, 30),
        (COMEDOR, 600),
    )
)

class SearchProblem:
    pass

class ControlDeIncendios(SearchProblem):
    def is_goal(self, state):
        _, habitaciones = state
        fuegos_apagados = sum(habitacion[-1] for habitacion in habitaciones) == 0

        return fuegos_apagados

    def actions(self, state):
        # un action se define como una tupla de dos elementos:
        #   - el primero puede ser "mover" o "apagar" segun la accion del bombero
        #   - el segundo es la habitación a la que se mueve o donde apaga el fuego

        bombero_position, habitaciones = state
        habitaciones = dict(habitaciones)
        # acciones de mover
        actions = [
            (habitacion_conectada, MOVER)
            for habitacion_conectada
            in ROOM_CONNECTIONS[bombero_position]
        ]

        # accion de apagar incendio, si corresponde
        if habitaciones[bombero_position] > 0:
            actions.append((APAGAR, bombero_position))

        return actions

    def result(self, state, action):
        bombero_position, habitaciones = state
        habitaciones = dict(habitaciones)
        action, place = action
        if action == MOVER:
            bombero_position = place

        else:
            habitaciones[bombero_position] = 0

        habitaciones = tuple(
            (habitacion, fuego) for habitacion, fuego in habitaciones.items()
        )
        return bombero_position,


    def cost(self, state, action, state2):
        action, place = action

        if action == MOVER:
            return 5

        bombero_position, habitaciones = state
        habitaciones = dict(habitaciones)

        return habitaciones[bombero_position]


    def heuristic(self, state):
        bombero_position, habitaciones = state

        # costo de apagar los fuegos que quedan prendidos:
        cost = sum(hab[1] for hab in habitaciones)

        habitaciones_con_fuego = [hab for hab in habitaciones if hab[1] > 0]

        # costo de moverse
        cost += len(habitaciones_con_fuego) * 5

        # si el bombero ya está en una habitación con fuego le restamos el costo de un movimiento
        if bombero_position in habitaciones_con_fuego:
            cost -= 5

        return cost


"""
Resolucion con astar

NODOS
=====
e = entrada
d = dormitorio
l = living
b = baño
c = comedor

m = moverse
a = apagar
Nombre | Pad| Action | Estado                                          | Costo Acum | Heuristica        | Coso Ac + Heuristica
       |    |que     |                                                 |            |                   |
       |    |lleva al|                                                 |            |                   |
       |    |nodo    |                                                 |            |                   |
-------|-------------------------------------------------------------------------------------
 N1    |    |        | (e, ((e, 0), (d, 10), (l, 10), (b, 30), (c, 600)|     0      | 650 + 4*5 (670)   |  670
 N2    | N1 | m, l   | (l, ((e, 0), (d, 10), (l, 10), (b, 30), (c, 600)|     5      | 650 + 3*5 (665)   |  670
 N3    | N2 | m, e   | estado igual a N1 con mayor costo acum, se descarta                                    |
 N4    | N2 | m, c   | (c, ((e, 0), (d, 10), (l, 10), (b, 30), (c, 600)| 5+5   10   | 650 + 3*5 (665)   |  675
 N5    | N2 | m, d   | (d, ((e, 0), (d, 10), (l, 10), (b, 30), (c, 600)| 5+5   10   | 650 + 3*5 (665)   |  675
 N6    | N2 | a, l   | (l, ((e, 0), (d, 10), (l, 0), (b, 30), (c, 600) | 5+10  15   | 640 + 3*5 (655)   |  670
 N7    | N6 | m, d   | (d, ((e, 0), (d, 10), (l, 0), (b, 30), (c, 600) | 15+5  20   | 640 + 2*5 (650)   |  670
 N8    | N6 | m, c   | (c, ((e, 0), (d, 10), (l, 0), (b, 30), (c, 600) | 15+5  20   | 640 + 2*5 (650)   |  670
 N9    | N6 | m, e   | (e, ((e, 0), (d, 10), (l, 0), (b, 30), (c, 600) | 15+5  20   | 640 + 2*5 (650)   |  670
 N10   | N7 | m, l   | estado igual a N6 con mayor costo acumulado, se descarta
 N11   | N7 | a, d   | (d, ((e, 0), (d, 0), (l, 0), (b, 30), (c, 600)  | 20+10  30  | 630 + 2*5 (640)   |  670
 N12   | N11| m, l   | (l, ((e, 0), (d, 0), (l, 0), (b, 30), (c, 600)  | 30+5   35  | 630 + 2*5 (640)   |  675
       |    |        |                                                 |            |                   |
       |    |        |                                                 |            |                   |


ITERACIONES
===========

FRONTERA                              | NODO ELEGIDO    | ES META      | HIJOS
------------------------------------------------------------------------------
                                      |    N1           |     No       | N2
                                      |    N2           |     No       | N3, N4, N5, N6
N4, N5                                |    N6           |     No       | N7, N8, N9
N8, N9, N4, N5                        |    N7           |     No       | N10, N11
N8, N9, N4, N5                        |    N11          |     No       | N12
N9, N12, N4, N5                       |    N8           |              |
                                      |                 |              |

"""

# Control de incendios 2 - CSP


VARIABLES = ["central", "aux_a", "aux_b"]
VARIABLES = ["central", "aux_a", "aux_b"]

JULIO_42 = "42_julio"
ESTANDAR_1 = "barrio_estandar_1"
ESTANDAR_2 = "barrio_estandar_2"
ESTANDAR_3 = "barrio_estandar_3"
PARQUE_INDUSTRIAL = "parque_industrial"
CICLOVIALANDIA = "ciclovialandia"
CENTRO = "centro"
QUINTAS = "quintas"
AEROCLUB = "aeroclub"
COSTANERA = "costanera"

BARRIOS_ADYACENTES = {
    JULIO_42: [CICLOVIALANDIA, CENTRO, ESTANDAR_2],
    ESTANDAR_2: [JULIO_42, CENTRO, ESTANDAR_1],
    PARQUE_INDUSTRIAL: [ESTANDAR_1, ESTANDAR_3],
    CICLOVIALANDIA: [JULIO_42, CENTRO, QUINTAS],
    CENTRO: [CICLOVIALANDIA, JULIO_42, ESTANDAR_1, ESTANDAR_2, COSTANERA, AEROCLUB],
    ESTANDAR_1: [ESTANDAR_2, CENTRO, COSTANERA, PARQUE_INDUSTRIAL, ESTANDAR_3],
    ESTANDAR_3: [ESTANDAR_1, PARQUE_INDUSTRIAL, COSTANERA],
    QUINTAS: [CICLOVIALANDIA],
    AEROCLUB: [CENTRO, COSTANERA],
    COSTANERA: [CENTRO, AEROCLUB, ESTANDAR_1, ESTANDAR_3],
}

DOMINIOS = {}

DOMINIOS["central"] = [
    barrio for barrio, adyacentes in BARRIOS_ADYACENTES.items()
    if barrio != CENTRO
    and len(adyacentes) >= 3
]

DOMINIOS["aux_b"] = [
    barrio for barrio, adyacentes in BARRIOS_ADYACENTES.items()
    if barrio not in [CENTRO, PARQUE_INDUSTRIAL, QUINTAS, AEROCLUB]
]

DOMINIOS["aux_a"] = [
    barrio for barrio, adyacentes in BARRIOS_ADYACENTES.items()
    if CENTRO in adyacentes
    and barrio not in [CENTRO, CICLOVIALANDIA]
]


CONSTRAINTS = []


def diferentes(variables, values):
    barrio1, barrio2 = values

    return barrio1 != barrio2


def no_adyacentes(variables, values):
    barrio1, barrio2 = values

    return barrio1 not in BARRIOS_ADYACENTES[barrio2]


for par_de_barrios in itertools.combinations(VARIABLES):
    CONSTRAINTS.extend([
        (par_de_barrios, diferentes),
        (par_de_barrios, no_adyacentes),
    ])
