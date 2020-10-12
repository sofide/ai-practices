"""
En el juego Munchkin, cada jugador tiene un personaje al que puede mejorar aplicando
diferentes cartas. Estas cartas incluyen cosas como armas, armaduras, pociones,
maldiciones, y otros modificadores que incrementan el nivel del personaje, haciéndolo
más capaz de ganar el juego. Pero existen algunas restricciones respecto a qué cartas
pueden utilizarse en un mismo personaje, de forma de evitar jugadores “superpoderosos”
que degradan la jugabilidad.

Un jugador tiene que elegir 3 cartas para intentar armar su personaje, y las opciones
disponibles son:
- Armadura de madera +1 (800 oro)
- Armadura de hierro +3 (1000 oro)
- Armadura de acero +5 (1300 oro)
- Espada de madera +1 (500 oro)
- Espada de hierro +2 (700 oro)
- Espada de acero +4 (1000 oro)
- Garrote gigante de madera +6 (1300 oro)
- Poción de fuego +5 (1500 oro)
- Poción de hielo +2 (800 oro)
- Poción de ácido +3 (1200 oro)

Y a la vez, deben cumplirse las siguientes restricciones:
- Solo se puede tener 1 armadura
- Solo se puede tener 1 arma de mano (espada o garrote)
- Solo se dispone de 3000 de oro para gastar (es decir, el valor de las cartas sumadas
no puede superar ese monto)
- No se pueden mezclar cartas de objetos de fuego con cartas de objetos de madera
- Se tiene que lograr un bonificador total (sumando las cartas) mayor a +8

"""
from itertools import combinations

from simpleai.search import (
    CspProblem,
    backtrack,
    min_conflicts,
    MOST_CONSTRAINED_VARIABLE,
    HIGHEST_DEGREE_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
)
from simpleai.search.csp import convert_to_binary

from utils import print_grid

VARIABLES = ["slot1", "slot2", "slot3"]

# tipo, material, bonif, costo
ITEMS = [
    ("armadura", "madera", 1, 800),
    ("armadura", "hierro", 3, 1000),
    ("armadura", "acero", 5, 1300),
    ("espada", "madera", 1, 500),
    ("espada", "hierro", 2, 700),
    ("espada", "acero", 4, 1000),
    ("garrote", "madera", 6, 1300),
    ("pocion", "fuego", 5, 1500),
    ("pocion", "hielo", 2, 800),
    ("pocion", "acido", 3, 1200),
]

DOMAINS = {
    variable: ITEMS
    for variable in VARIABLES
}

CONSTRAINTS = []

def differents(variables, values):
    item_a, item_b = values

    return item_a != item_b


def una_armadura_max(variables, values):
    item_a, item_b = values

    return (item_a[0], item_b[0] != ("armadura", "armadura"))


def arma_de_mano(variables, values):
    item_a, item_b = values

    items_type = {item_a[0], item_b[0]}

    return items_type not in [{"espada", "espada"}, {"espada", "garrote"}]


def fuego_y_madera(variables, values):
    item_a, item_b = values

    items_material = {item_a[1], item_b[1]}

    return items_material != {"fuego", "madera"}


for variables_pair in combinations(VARIABLES, 2):
    CONSTRAINTS.extend([
        (variables_pair, differents),
        (variables_pair, una_armadura_max),
        (variables_pair, arma_de_mano),
        (variables_pair, fuego_y_madera),
    ])

def valid_cost(variables, values):
    cost = sum(item[-1] for item in values)

    return cost <= 3000


def bonificador_total(variables, values):
    bonif = sum(item[-2] for item in values)

    return bonif >= 8


CONSTRAINTS.append((VARIABLES, valid_cost))
CONSTRAINTS.append((VARIABLES, bonificador_total))


def print_result(result):
    for item in result.values():
        print(item)

    print("COST:", sum(x[-1] for x in result.values()))
    print("BONIF:", sum(x[-2] for x in result.values()))

if __name__ == "__main__":
    problem = CspProblem(VARIABLES, DOMAINS, CONSTRAINTS)

    print("MIN CONFLICTS")
    result = min_conflicts(problem, iterations_limit=100)

    print_result(result)

    print("-"* 50)
    print("BACKTRACKING")
    result = backtrack(problem)
    print_result(result)

