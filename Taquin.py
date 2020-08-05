import sys
import random
from copy import deepcopy


def simulate(board, depth=1, list_moves=[], max_depth=1, current_move=None):
    """
    :param board: Game board
    :param depth: Current depth of the Depth-first search
    :param list_moves: List of all movements to solve the game
    :param max_depth: Maximum depth reachable of the Depth-first search
    :param current_move: Current movement performed
    :return: the list of movement or None

    The current movement is added to the list of completed movements.
    If it is a winning situation, the list of all movements made to reach this situation is returned.
    When a movement is made, the reverse movement is remove fom the list of possible moves.
    This function calls itself while it is not a winning situation or the maximum depth is not achievable.
    """

    if current_move is not None:
        simulate_move(board, current_move)
        list_moves.append(current_move)

    if is_win_situation(board):
        return list_moves
    elif depth > max_depth:
        return None

    moves = get_possible_moves(board)

    if current_move is not None:
        reversed_move = (current_move[0] * -1, current_move[1] * -1)
        if reversed_move in moves:
            moves.remove(reversed_move)

    for move in moves:
        res = simulate(deepcopy(board), depth + 1, deepcopy(list_moves), max_depth, move)
        if res is not None:
            return res

    return None


def simulate_move(board, move):
    """Return the board upgraded after a movement.

    The next position is the sum of the actual index and the index of the movement.
    """
    empty_cell_pos = get_empty_cell_pos(board)
    next_pos = (empty_cell_pos[0] + move[0], empty_cell_pos[1] + move[1])
    board[empty_cell_pos[1]][empty_cell_pos[0]] = board[next_pos[1]][next_pos[0]]
    board[next_pos[1]][next_pos[0]] = 0

    return board


def get_possible_moves(board):
    """Return the set of possible moves from the empty cell.

    From the case 0, the four possibles movements (left, right, up, down) are tested.
    If the movement is possible it is added to the list of available movements from this cell.
    """
    all_moves = [(+0, -1), (+0, +1), (+1, +0), (-1, +0)]
    random.shuffle(all_moves)
    available_moves = []

    for i, j in all_moves:
        new_index = (get_empty_cell_pos(board)[0] + i, get_empty_cell_pos(board)[1] + j)
        if 0 <= new_index[0] < len(board[0]) and 0 <= new_index[1] < len(board):
            available_moves.append((i, j))

    return available_moves


def get_empty_cell_pos(board):
    """Return the index x and y of the cell 0"""
    for j, line in enumerate(board):
        if 0 in line:
            return line.index(0), j


def is_win_situation(board):
    """Return True if the board is winning. Otherwise return False."""
    return board == list(split_list(list(range(1, len(board) * len(board[0]))) + [0], len(board)))


def create_random_board(size):
    """Generate a randomly shuffle board."""
    board_values = list(range(0, size * size))
    random.shuffle(board_values)
    board = list(split_list(board_values, size))
    return board


def split_list(l, n):
    """Take a list and return this list split in sublist."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def moves_to_directions(moves):
    """Transform a movement list (vectors) into directions."""
    moves_dict = {
        (0, -1): "Up",
        (0, +1): "Down",
        (+1, 0): "Right",
        (-1, 0): "Left"
    }

    return list(map(lambda x: moves_dict[x], moves))


def init_board():
    """Initialization of the game board."""
    default_board_size = 3
    board_size = int(sys.argv[1]) if len(sys.argv) == 2 else default_board_size

    return create_random_board(size=board_size)


def solve():
    """Manage the resolution of a 15 puzzle board."""
    board = init_board()
    current_depth, max_depth = 1, 20
    response = None

    print(*board, sep='\n')

    while response is None and current_depth < max_depth:
        response = simulate(deepcopy(board), depth=0, list_moves=[], max_depth=current_depth, current_move=None)
        print("Testing for max-depth = {}".format(current_depth))
        current_depth = current_depth + 1

    return response


if __name__ == "__main__":
    res = solve()

    if res is None:
        print("No solution found")
    else:
        print("Solution found in {} moves".format(len(res)))
        print(" → ".join(moves_to_directions(res)))




