import random
from ex12_utils import *

BOARD_SIZE = 4
LETTERS = [
    ['A', 'E', 'A', 'N', 'E', 'G'],
    ['A', 'H', 'S', 'P', 'C', 'O'],
    ['A', 'S', 'P', 'F', 'F', 'K'],
    ['O', 'B', 'J', 'O', 'A', 'B'],
    ['I', 'O', 'T', 'M', 'U', 'C'],
    ['R', 'Y', 'V', 'D', 'E', 'L'],
    ['L', 'R', 'E', 'I', 'X', 'D'],
    ['E', 'I', 'U', 'N', 'E', 'S'],
    ['W', 'N', 'G', 'E', 'E', 'H'],
    ['L', 'N', 'H', 'N', 'R', 'Z'],
    ['T', 'S', 'T', 'I', 'Y', 'D'],
    ['O', 'W', 'T', 'O', 'A', 'T'],
    ['E', 'R', 'T', 'T', 'Y', 'L'],
    ['T', 'O', 'E', 'S', 'S', 'I'],
    ['T', 'E', 'R', 'W', 'H', 'V'],
    ['N', 'U', 'I', 'H', 'M', 'QU']
]


def randomize_board(dice_list=LETTERS):
    dice_indices = list(range(len(dice_list)))
    random.shuffle(dice_indices)
    dice_indices_iter = iter(dice_indices)
    board = []
    for i in range(BOARD_SIZE):
        row = []
        for j in range(BOARD_SIZE):
            die = dice_list[next(dice_indices_iter)]
            letter = random.choice(die)
            row.append(letter)
        board.append(row)
    return board


if __name__ == "__main__":
    from pprint import pprint
    board = randomize_board()
    pprint(board)
    # path_node_x = int(input("Enter Path Node X: "))
    # path_node_y = int(input("Enter Path Node Y: "))
    # path_node = [(path_node_y, path_node_x)]
    # print(path_node)
    # while ((-1, -1) not in path_node):
    #     path_node_x = int(input("Enter Path Node X: "))
    #     path_node_y = int(input("Enter Path Node Y: "))
    #     path_node.append((path_node_y, path_node_x))
    #
    # path_node.remove((-1, -1))
    words = get_word_list("boggle_dict.txt").split()

    # print(find_length_n_words(1, board, words))
    # print(find_length_n_paths(3, board, words))
    # print(find_length_n_words(4, board, words))
    print(find_length_n_paths(5, board, words))


