import numpy as np
import random

from rubik.cube import Cube

class BruteForceSolver:

    GOD_NUMBER = 20
    MAX_SEQENCE_LENGTH = 10000
    SOLVED_STATE_STRING = "OOOOOOOOOGGGWWWBBBYYYGGGWWWBBBYYYGGGWWWBBBYYYRRRRRRRRR"
    ALLOWED_MOVES = ['R', 'Ri', 'L', 'Li', 'U', 'Ui', 'D', 'Di', 'F', 'Fi', 'B', 'Bi']

    def __init__(self, scramble=None):
        if scramble is None:
            self.scramble = []
        else:
            self.scramble = scramble

        self.cube = Cube(self.SOLVED_STATE_STRING)
        self.cube.sequence(self.scramble)
        self.initial_state = self.cube.flat_str()

        # [Sequence, Current State, Reverse of last Move, Score]
        self.solution_list = [['', '', '', 0] for _ in self.ALLOWED_MOVES]
        self.longest_sequence = 0

    def iterate_solve(self):
        solution_list = self.solution_list.copy()
        for sol in solution_list:
            # Create a cube with the desired state
            if len(sol[1]) > 0:
                sequence_cube = Cube(sol[1])
            else:
                sequence_cube = Cube(self.initial_state)
            # Generate possible moves
            if len(sol[2]) > 0:
                possible_moves = [_ for _ in self.ALLOWED_MOVES if not _ == sol[2][0]]
            else:
                possible_moves = self.ALLOWED_MOVES.copy()

            # Iterate possible moves and asses score for each
            for move in possible_moves:
                reverse_move = move[0] if len(move) == 2 else move + 'i'
                sequence_cube.sequence(move)
                sequence_score = self._asses_sequence(sequence_cube.flat_str())
                total_sequence = sol[0] + move + ' '
                self.solution_list.append([total_sequence, sequence_cube.flat_str(), reverse_move, sequence_score])
                # Revert cube state before next move
                sequence_cube.sequence(reverse_move)

        self._clean_solution_list()

    def _asses_sequence(self, state_string):
        score = 0
        if Cube(state_string).is_solved():
            return 10000

        for face_no in range(6):
            face_colors = self._get_face(state_string, face_no)

            # Sum of stickers equal to the center color
            score += sum(face_colors == face_colors[4]) - 1

        return score

    def _clean_solution_list(self):
        sl_length = len(self.solution_list)
        for s in self.solution_list:
            if len(s[0].split(' ')) < self.longest_sequence:
                self.solution_list.remove(s)

        self._order_solution_list()

        if len(self.solution_list) > self.MAX_SEQENCE_LENGTH:
            self._trim_solution_list()

    def _get_face(self, cube_string, face_no):
        if face_no == 0:
            return np.array(list(cube_string[0:9]))
        elif face_no == 5:
            return np.array(list(cube_string[-9:]))
        else:
            face_colors = []
            i = 9 + 3 * (face_no - 1)
            for _ in range(3):
                face_colors += list(cube_string[i:i + 3])
                i += 12
            return np.array(face_colors)

    def _order_solution_list(self):
        self.solution_list.sort(key=lambda row: (row[-1], row[0]), reverse=True)

    def _trim_solution_list(self):
        self.solution_list = self.solution_list[0:self.MAX_SEQENCE_LENGTH]


def generate_scramble(length=30):
    seq = ""
    for _ in range(length):
        seq += random.choice(ALLOWED_MOVES) + ' '

    return seq


ALLOWED_MOVES = ['R', 'Ri', 'L', 'Li', 'U', 'Ui', 'D', 'Di', 'F', 'Fi', 'B', 'Bi']

if __name__ == '__main__':
    scramble = generate_scramble(15)
    print(f'Initial scamble is:\n\t{scramble}')
    solver = BruteForceSolver(scramble)
    stall_index = 0
    best_score = 0
    # Nomber of iterations to try
    n = 30

    print(solver.cube)
    for i in range(0, n):
        print(f'{i/n*100}%')
        solver.iterate_solve()
        if solver.solution_list[0][-1] == best_score:
            stall_index += 1
        best_score = solver.solution_list[0][-1]
        print(f'Best solution has score of {best_score}')
        if best_score > 48 or stall_index > 5:
            break

    print(solver.solution_list[0])
