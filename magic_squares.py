from itertools import combinations
from random import shuffle

from simpleai.search import SearchProblem, hill_climbing

from utils import print_grid


SQUARE_SIZE = 10
MAX_NUMBER = SQUARE_SIZE ** 2

TARGET_TOTAL = sum(range(1, MAX_NUMBER+1)) / SQUARE_SIZE


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

        return totals.count(TARGET_TOTAL)

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
    expected_value = SQUARE_SIZE * 2
    iterations = 0
    while True:
        iterations += 1
        random_state = MagicSquareProblem().generate_random_state()
        problem = MagicSquareProblem(random_state)
        result = hill_climbing(problem, 1000)
        if result.value == expected_value:
            print("solution found! Iterations:", iterations)
            break
        if iterations % 10 == 0:
            print(f"{iterations} iterations and the solution hasn't been found yet :(")


    problem.print_state(result.state)
    print("value:", problem.value(result.state))
