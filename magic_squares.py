from itertools import combinations
from random import shuffle

from simpleai.search import SearchProblem, hill_climbing_random_restarts

from utils import print_grid


SQUARE_SIZE = 4
MAX_NUMBER = SQUARE_SIZE ** 2


def find(element, state):
    for row_i, row in enumerate(state):
        for column_i, this_element in enumerate(row):
            if element == this_element:
                return row_i, column_i


class MagicSquareProblem(SearchProblem):
    def actions(self, state):
        return list(combinations(range(1, MAX_NUMBER +1), 2))

    def result(self, state, action):
        state = [list(row) for row in state]
        number_a, number_b = action

        a_row, a_column = find(number_a, state)
        b_row, b_column = find(number_b, state)

        state[a_row][a_column] = number_b
        state[b_row][b_column] = number_a

        return tuple(tuple(row) for row in state)

    def value(self, state):
        totals = []

        for row in state:
            totals.append(sum(row))

        for column in zip(*state):
            totals.append(sum(column))

        target_total = sum(range(1, MAX_NUMBER+1)) / SQUARE_SIZE

        return totals.count(target_total)

    def generate_random_state(self):
        numbers = list(range(1, MAX_NUMBER + 1))
        shuffle(numbers)

        state = []
        for row_index in range(SQUARE_SIZE):
            from_index = row_index * SQUARE_SIZE
            to_index = from_index + SQUARE_SIZE
            state.append(tuple(numbers[from_index:to_index]))

        return tuple(state)

    def print_state(self, state):
        elements = {
            str(element): [(row_i, column_i)]
            for row_i, row in enumerate(state)
            for column_i, element in enumerate(row)
        }

        print_grid(SQUARE_SIZE, SQUARE_SIZE, elements)


if __name__ == "__main__":
    problem = MagicSquareProblem()
    result =  hill_climbing_random_restarts(problem, 1000)
    problem.print_state(result.state)
    print("value:", problem.value(result.state))
