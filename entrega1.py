from collections import defaultdict
from itertools import combinations

from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, ConsoleViewer, WebViewer

RAFAELA = "rafaela"
SUNCHALES = "sunchales"
LEHMANN = "lehmann"
SUSANA = "susana"
SC_DE_SAGUIER = "sc_de_saguier"
ESPERANZA = "esperanza"
RECREO = "recreo"
SANTA_FE = "santa_fe"
SAN_VICENTE = "san_vicente"
SANTO_TOME = "santo_tome"
ANGELICA = "angelica"
SAUCE_VIEJO = "sauce_viejo"


CONNECTIONS = [
    (SUNCHALES, LEHMANN, 32),
    (LEHMANN, RAFAELA, 8),
    (RAFAELA, SUSANA, 10),
    (SUSANA, ANGELICA, 25),
    (ANGELICA, SAN_VICENTE, 18),
    (SC_DE_SAGUIER, ANGELICA, 60),
    (ANGELICA, SANTO_TOME, 85),
    (RAFAELA, ESPERANZA, 70),
    (ESPERANZA, RECREO, 20),
    (RECREO, SANTA_FE, 10),
    (SANTO_TOME, SANTA_FE, 5),
    (SANTO_TOME, SAUCE_VIEJO, 15),
]


CONNECTIONS_DICT = defaultdict(dict)
for connection in CONNECTIONS:
    city_a, city_b, liters = connection
    CONNECTIONS_DICT[city_a][city_b] = liters
    CONNECTIONS_DICT[city_b][city_a] = liters

KM_FOR_OIL_LITER = 100


SEDES = [RAFAELA, SANTA_FE]

TRUCKS_EXAMPLE = [
    # id, ciudad de origen, y capacidad de combustible máxima (litros)
    ("c1", RAFAELA, 1.5),
    ("c2", RAFAELA, 2),
    ("c3", SANTA_FE, 2),
]

PACKAGES_EXAMPLE = [
    # id, ciudad de origen, y ciudad de destino
    ('p1', RAFAELA, ANGELICA),
    ('p2', RAFAELA, SANTA_FE),
    ('p3', ESPERANZA, SUSANA),
    ('p4', RECREO, SAN_VICENTE),
]


class MercadoArtificalProblem(SearchProblem):
    def __init__(self, trucks_liters, packages_goal=PACKAGES_EXAMPLE, *args, **kwargs):
        self.packages_goal = packages_goal
        self.trucks_liters = trucks_liters
        super().__init__(*args, **kwargs)

    def is_goal(self, state):
        # print("-"*50)
        # print("IN IS GOAL")
        # print("state:", state)
        # print("-"*50)
        trucks_info, packages_info = state

        if packages_info != self.packages_goal:
            # los paquetes tienen que estar en la ciudad de destino
            return False
        for truck in trucks_info:
            # los camiones deben estar en alguna de las sedes
            if truck[1] not in SEDES:
                return False
        # print("IS GOAL TRUE")
        return True

    def actions(self, state):
        """
        each action is defined by a tuple of four elements, for example:
        ('c1', 'esperanza', 0.7, ('p1', 'p2')),
        - c1: truck_id
        - 'esperanza': city where the truck will travel
        - 0.7: liters of oil spended in the trip
        - ('p1', 'p2'): packages to transport in the trip
        """
        # print("-"*50)
        # print("IN ACTIONS")
        # print("state:", state)
        trucks_info, packages_info = state
        posible_actions = []
        for truck in trucks_info:
            truck_id, truck_city, oil_in_truck = truck
            posible_trips = []

            for connected_city, km in CONNECTIONS_DICT[truck_city].items():
                oil_for_trip = km / KM_FOR_OIL_LITER
                if oil_for_trip < oil_in_truck:
                    posible_trips.append((connected_city, oil_for_trip))

            posible_packages_to_take = [
                package_id
                for package_id, package_city in packages_info
                if package_city == truck_city
            ]

            packages_combinations = []

            # any combination of packages, from 0 to all.
            for comb_qty in range(len(posible_packages_to_take) + 1):
                qty_combinations = combinations(posible_packages_to_take, comb_qty)
                packages_combinations.extend(qty_combinations)

            posible_actions.extend(
                (truck_id, city_to_go, oil_for_trip, packages)
                for city_to_go, oil_for_trip in posible_trips
                for packages in packages_combinations
            )

        # print("RETURNES ACTIONS:", posible_actions)
        # print("-"*50)
        return posible_actions

    def result(self, state, action):
        # print("-"*50)
        # print("IN RESULT")
        # print("state:", state)
        # print("action:", action)
        trucks_info, packages_info = state
        trucks_dict = {
            truck_id: (city, oil)
            for truck_id, city, oil in trucks_info
        }
        truck_id, city_to_go, oil_for_trip, packages_to_move = action

        # Update the state of the moved truck
        if city_to_go in SEDES:
            oil_in_moved_truck = self.trucks_liters[truck_id]
        else:
            oil_in_moved_truck = trucks_dict[truck_id][1] - oil_for_trip

        moved_truck_new_state = (truck_id, city_to_go, oil_in_moved_truck)

        trucks_new_state = [
            truck_state for truck_state in trucks_info
            if truck_state[0] != truck_id
        ]
        trucks_new_state.append(moved_truck_new_state)

        # Update the state for the moved packages
        packages_new_state = []
        for package_id, package_city in packages_info:
            if package_id in packages_to_move:
                package_city = city_to_go

            packages_new_state.append((package_id, package_city))

        result_to_return =  tuple(trucks_new_state), tuple(packages_new_state)
        # print("RETURNED RESULT:", result_to_return)
        # print("-"*50)
        return result_to_return

    def cost(self, state, action, state2):
        """
        The cost of an action is equal to the oil spended in the trip.
        """
        # print("-"*50)
        # print("IN COST")
        # print("state:", state)
        # print("action:", action)
        # print("RETURNED COST:", action[2])
        # print("-"*50)
        return action[2]

    def heuristic(self, state):
        print("-"*50)
        print("IN HEURISTIC")
        print("state:", state)
        trucks_info, packages_info = state
        trucks_locations = [truck[1] for truck in trucks_info]

        packages_goal_dict = {
            package_id: city
            for package_id, city in self.packages_goal
        }
        packages_not_in_destination = [
            # package_id, current_city, destination_city
            (package_id, current_city, packages_goal_dict[package_id])
            for package_id, current_city in packages_info
            if current_city != packages_goal_dict[package_id]
        ]

        cities_with_pkg_to_move = [x[1] for x in packages_not_in_destination]

        estimated_km = 0
        for package_id, current_city, destination in packages_not_in_destination:
            pkg_city_shortest_conn = min(CONNECTIONS_DICT[current_city].values())
            pkg_estimated_cost = 0

            if destination in CONNECTIONS_DICT[current_city]:
                pkg_estimated_cost += CONNECTIONS_DICT[current_city][destination]
            else:
                destination_shortest_conn = min(CONNECTIONS_DICT[destination].values())
                print(f"parcial heuristic for  [MOVE PKG] {package_id}: {pkg_city_shortest_conn} + {destination_shortest_conn}")
                pkg_estimated_cost += pkg_city_shortest_conn + destination_shortest_conn

            print("current_city:", current_city)
            print("trucks_locations:", trucks_locations)
            if not current_city in trucks_locations:
                nearest_pkg_cities = [
                    adjacent_city
                    for adjacent_city, distance in CONNECTIONS_DICT[current_city].items()
                    if distance == pkg_city_shortest_conn
                ]

                for near_city in nearest_pkg_cities:
                    if near_city in trucks_locations:
                        print(f"parcial heuristic for [TRUCK ARRIVING] {package_id}: {pkg_city_shortest_conn}")
                        pkg_estimated_cost += pkg_city_shortest_conn
                        break

                else:
                    trucks_shortest_conn = min(
                        min(CONNECTIONS_DICT[truck_city].values())
                        for truck_city in trucks_locations
                    )
                    print(f"parcial heuristic for [TRUCK ARRIVING] {package_id}: {pkg_city_shortest_conn} + {trucks_shortest_conn}")
                    pkg_estimated_cost += pkg_city_shortest_conn + trucks_shortest_conn

            pkgs_to_move_in_current_city = cities_with_pkg_to_move.count(current_city)

            print(f"heuristic for {package_id}: {pkg_estimated_cost} / {pkgs_to_move_in_current_city}")
            print(f"heuristic for {package_id}: {pkg_estimated_cost / pkgs_to_move_in_current_city}")
            estimated_km += pkg_estimated_cost / pkgs_to_move_in_current_city

        trucks_not_in_sede = [
            location for location in trucks_locations
            if location not in SEDES
        ]

        cities_set = set(cities_with_pkg_to_move)
        extra_trucks_to_move = len(trucks_not_in_sede) - len(cities_set)
        if extra_trucks_to_move > 0:
            shortest_sede_connection = min(
                min(conn for conn in CONNECTIONS_DICT[sede_city].values())
                for sede_city in SEDES
            )

            shortest_con_per_city = [
                min(CONNECTIONS_DICT[truck_city].values())
                for truck_city in trucks_not_in_sede
            ]
            print("shortest per city", shortest_con_per_city)
            shortest_city_trucks_connection = min(
                shortest_con_per_city
            )

            print(f"heuristic for EXTRA TRUCKS: {extra_trucks_to_move} * max({shortest_sede_connection}, {shortest_city_trucks_connection})")
            print(f"heuristic for EXTRA TRUCKS: {extra_trucks_to_move * max(shortest_sede_connection, shortest_city_trucks_connection)}")
            estimated_km += extra_trucks_to_move * max(
                shortest_sede_connection, shortest_city_trucks_connection
            )


        print("estimated km in heuristic:", estimated_km)

        print("RETURNED HEURISTIC:", estimated_km / KM_FOR_OIL_LITER)
        print("-"*50)
        return estimated_km / KM_FOR_OIL_LITER


def planear_camiones(metodo, camiones=TRUCKS_EXAMPLE, paquetes=PACKAGES_EXAMPLE, debug=False):
    # a state is defined by a tuple of two elements:
    # - trucks with info wich is a tuple of (id, city, oil_liters)
    # - packages info wich is a tuple of (id, city)
    initial_state = (tuple(camiones), tuple(x[:-1] for x in paquetes))
    packages_goal = tuple((x[0], x[2]) for x in paquetes)
    trucks_liters = {x[0]: x[-1] for x in camiones}

    problem = MercadoArtificalProblem(trucks_liters, packages_goal, initial_state)

    search_methods = {
        "astar": astar,
        "breadth_first": breadth_first,
        "depth_first": depth_first,
        "uniform_cost": uniform_cost,
        "greedy": greedy,
    }

    method = search_methods[metodo]

    if debug:
        visor = ConsoleViewer()
        # visor = WebViewer()
    else:
        visor = BaseViewer()
    result = method(problem, graph_search=True, viewer=visor)

    if debug:
        print('estadísticas:')
        print('cantidad de acciones hasta la meta:', len(result.path()))
        print(visor.stats)
        print("FINAL STATE:")
        print(result.state)

        for i, step in enumerate(result.path()):
            cont = input("print step by step? Y/n")
            if cont.upper() == "N":
                break

            print(f"----------- STEP {i} ----------")
            action, state = step

            print("ACTION")
            print(action)

            print("STATE")
            print(state)


    return [action for action, _ in result.path() if action is not None]


if __name__ == "__main__":
    camiones = [
        ("c1", RAFAELA, 40),
    ]
    paquetes = [
        ("p1", RAFAELA, ESPERANZA),
        ("p2", RAFAELA, SANTA_FE),
        ("p3", SANTA_FE, ESPERANZA),
    ]
    camiones = [('c1', 'rafaela', 1.5), ('c2', 'santa_fe', 9999)]
    paquetes = [('p1', 'sunchales', 'sauce_viejo')]
    planear_camiones("astar", camiones, paquetes, debug=True)
