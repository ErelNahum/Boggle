from copy import deepcopy
import trie
import itertools


DICT_FILE = "boggle_dict.txt"


def initialize_trie(words):
    root = trie.TrieNode('*')
    for word in words:
        trie.add(root, word)

    return root


def get_word_list(file_name):
    with open(file_name, "r") as myfile:
        return myfile.read()


class Finder:
    def __init__(self, board, words, root):
        self.board = board
        self.paths = []
        self.words = words
        self.root = root

    def find_length_n_words_path_from_cell(self, start_cell, n, path, is_check_word):
        if n > 1:
            path_word = path_2_word(self.board, path)
            if not trie.find_prefix(self.root, path_word)[1]:
                return ""

            start_x = start_cell[0]
            start_y = start_cell[1]
            cells_to_append = []

            # 8 directions to check (all around the cell)
            if start_x > 0:
                new_cell = (start_x - 1, start_y)
                cells_to_append.append(new_cell)
            if start_x < len(self.board[0]) - 1:
                new_cell = (start_x + 1, start_y)
                cells_to_append.append(new_cell)
            if start_y > 0:
                new_cell = (start_x, start_y - 1)
                cells_to_append.append(new_cell)
            if start_y < len(self.board) - 1:
                new_cell = (start_x, start_y + 1)
                cells_to_append.append(new_cell)
            if start_y > 0 and start_x > 0:
                new_cell = (start_x - 1, start_y - 1)
                cells_to_append.append(new_cell)
            if start_y < len(self.board) - 1 and start_x < len(self.board[0]) - 1:
                new_cell = (start_x + 1, start_y + 1)
                cells_to_append.append(new_cell)
            if start_y < len(self.board) - 1 and start_x > 0:
                new_cell = (start_x - 1, start_y + 1)
                cells_to_append.append(new_cell)
            if start_y > 0 and start_x < len(self.board[0]) - 1:
                new_cell = (start_x + 1, start_y - 1)
                cells_to_append.append(new_cell)

            for cell in cells_to_append:
                if cell not in path:
                    new_path = deepcopy(path)
                    new_path.append(cell)

                    if is_check_word:
                        i = len(self.board[cell[0]][cell[1]])
                    else:
                        i = 1
                    self.find_length_n_words_path_from_cell(cell, n - i, new_path, is_check_word)

        elif n > 0:
            return self.paths.append(path)


def is_valid_path(board, path, words):
    word = ""
    for path_node_index in range(len(path)):
        check_path = deepcopy(path)
        del check_path[path_node_index]
        path_node = path[path_node_index]
        if path_node in check_path:
            return None

        if path_node[0] < 0 or path_node[1] < 0 or path_node[0] > len(board)-1 or path_node[1] > len(board)-1:
            return None

        if path_node_index > 0:
            prev_node = path[path_node_index - 1]
            if abs(prev_node[0] - path_node[0]) > 1 or abs(prev_node[1] - path_node[1]) > 1:
                return None

        word += board[path_node[0]][path_node[1]]

    if word in words:
        return word
    else:
        return None


def get_max_len_word(words):
    max_len = 0
    for word in words:
        if len(word) > max_len:
            max_len = len(word)
    return max_len


def find_length_n_paths(n, board, words):
    root = initialize_trie(words)
    if n > get_max_len_word(words) or n <= 0:
        return []

    finder = Finder(board, words, root)
    for x_index in range(len(board[0])):
        for y_index in range(len(board)):
            start_cell = (x_index, y_index)
            i = n
            finder.find_length_n_words_path_from_cell(start_cell, i, [start_cell], False)

    all_paths = finder.paths
    legal_paths = []

    for path in all_paths:
        word = ""
        for cell in path:
            word += board[cell[0]][cell[1]]
        if word in words:
            legal_paths.append(path)

    return legal_paths


def path_2_word(board, path):
    word = ""
    for cell in path:
        word += board[cell[0]][cell[1]]
    return word


def find_length_n_words(n, board, words):
    root = initialize_trie(words)
    if n > get_max_len_word(words) or n <= 0:
        return []

    finder = Finder(board, words, root)
    for x_index in range(len(board[0])):
        for y_index in range(len(board)):
            start_cell = (x_index, y_index)
            i = n
            i = i - len(board[start_cell[0]][start_cell[1]])+1
            finder.find_length_n_words_path_from_cell(start_cell, i, [start_cell], True)

    all_paths = finder.paths
    legal_paths = []

    for path in all_paths:
        word = path_2_word(board, path)
        if word in words:
            legal_paths.append(path)

    return legal_paths


def max_score_paths(board, words):
    word_max = get_max_len_word(words)
    path_max = len(board) * len(board[0])
    all_paths = []
    for i in range(min(path_max, word_max)):
        all_paths.extend(find_length_n_paths(i, board, words))
        all_paths.extend(find_length_n_words(i, board, words))

    max_score_words = {}
    for path in all_paths:
        word = path_2_word(board, path)
        if word not in max_score_words.keys():
            max_score_words[word] = path
        else:
            prev_word_path = max_score_words[word]
            if len(prev_word_path) < len(path):
                print(word)
                max_score_words[word] = path

    print(max_score_words)
    max_score_path = []
    for path in max_score_words.values():
        max_score_path.append(path)

    return max_score_path