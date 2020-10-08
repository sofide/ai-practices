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


variables = ["slot_a", "slot_b", "slot_c"]

COSTOS = {
    "assault_cuirass": 5000,
    "battlefury": 4000,
    "cloak": 500,
    "hyperstone": 2000,
    "quelling_blase": 200,
    "shadow_blade": 3000,
    "veil_of_discord": 2000,
}


# name, price
dominios = {}

for variable in ["slot_b", "slot_c"]:
    dominios[variable] = [
        "assault_cuirass",
        "battlefury",
        "cloak",
        "hyperstone",
        "quelling_blase",
        "shadow_blade",
        "veil_of_discord",
    ]

dominios["slot_a"] = ["battlefury", "veil_of_discord"]

restricciones = []

def sumar_items(variables, values):
    costo_total = sum(COSTOS[item] for item in values)

    return costo_total <= 6000


restricciones.append(
    (('slot_a', 'slot_b', 'slot_c'), sumar_items),
)


def hyperstone_no_con_shadow_blade(variables, values):
    mala_combinacion = {"hyperstone", "shadow_blade"}
    return set(values) != mala_combinacion


def quelling_no_con_shadow(variables, values):
    mala_combinacion = {"quelling_blase", "shadow_blade"}
    return set(values) != mala_combinacion


def cloack_no_con_veil(variables, values):
    mala_combinacion = {"cloak", "veil_of_discord"}
    return set(values) != mala_combinacion

def diferentes(variables, values):
    item_a, item_b = values
    return item_a != item_b

for variable1, variable2 in combinations(variables, 2):
    restricciones.extend([
        ((variable1, variable2), hyperstone_no_con_shadow_blade),
        ((variable1, variable2), quelling_no_con_shadow),
        ((variable1, variable2), cloack_no_con_veil),
        ((variable1, variable2), diferentes),
    ])

problem = CspProblem(variables, dominios, restricciones)
result = min_conflicts(problem, iterations_limit=100)

print(result)
