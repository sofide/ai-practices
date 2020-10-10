from simpleai.search.viewers import BaseViewer


def grid_drawer(rows, columns, elements, cell_size=5):
    """
    generate the string of a grid of size `rows` x `columns` with each cell of size
    `cell_size`.  `elements` is expected to be a dict with the string to draw in a cell
    as a key and the positions where to draw it as a value.
    """
    matrix = []
    for row in range(rows):
        row_elements = []
        for column in range(columns):
            cell_elements = ""
            for element, element_positions in elements.items():
                if (row, column) in element_positions:
                    cell_elements += element
            row_elements.append(cell_elements.center(cell_size))
        matrix.append(row_elements)


    row_separation = "\n" + ("+" + ("-" * cell_size)) * columns + "+" + "\n"
    column_separation = "|"

    grid_to_print = row_separation

    for row in matrix:
        grid_to_print += column_separation
        grid_to_print += column_separation.join(row)
        grid_to_print += column_separation
        grid_to_print += row_separation

    return grid_to_print


def print_grid(rows, columns, elements, cell_size=5):
    print(grid_drawer(rows, columns, elements, cell_size))



def try_search_method(search_method, problem_class, initial_state):
    print()
    print('=' * 50)

    print("corriendo:", search_method.__name__)
    visor = BaseViewer()
    problem = problem_class(initial_state)
    result = search_method(problem, graph_search=True, viewer=visor)

    print('estado final:')
    if result is None:
        print("RESULTADO NO ENCONTRADO")
        return
    else:
        print(result.state)

    print('-' * 50)

    print('estadísticas:')
    print('cantidad de acciones hasta la meta:', len(result.path()))
    print(visor.stats)

    draw_path = input("Do you want to draw the path? [y/N]: ")
    if draw_path.lower() == "y":
        for _, state in result.path():
            problem.print_state_representation(state)
            continue_printing = input("Print the next state [Y/n]: ")

            if continue_printing.lower() == "n":
                break
