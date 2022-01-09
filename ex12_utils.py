##############################################################################
# FILE: ex12.py
# WRITER: Yuval Fishman, yuvalfishman , 325711398. Erel Nahum,
# EXERCISE: Intro2cs ex12 2021-2022
# DESCRIPTION:a file that realizes functions that contend with identifying words
##############################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from copy import deepcopy
import trie
import itertools

##############################################################################
#                                 Constants                                  #
##############################################################################
DICT_FILE = "boggle_dict.txt"


##############################################################################
#                              Finder Class                                  #
##############################################################################
class Finder:
    """
    this class is a helper class to find paths of words in a specific board
    """
    def __init__(self, board, words, root):
        self.board = board
        self.paths = []
        self.words = words
        self.root = root

    def find_length_n_words_path_from_cell(self, start_cell, n, path, is_check_word):
        """
            this function finds length n paths/words from a certain cell in a board that are legal
            param: start_cell - the cell to start the path search from
            param: n - the length of path/word that is searched
            param: path - a helper meanwhile path recursive param
            param: is_check_word - a boolean param that decides whether the function searches length n words or paths
            return: a list of paths of legal words in the length of n from a certain cell
        """
        if n > 1:
            # check if the word created by meanwhile path can even create a word within all the words in dict
            # this part is realized by a tree of letters that represent all the words inside the dict. it is realized
            # like that so the computer would not have to check all the words inside the dict to determine whether
            # a certain combination of letters has the potential to create a word.

            # footnote - this tree is not truly nescecery for this perticullar board (4*4) and dict of words because
            # there aren't enough paths inside the board and too many words inside the dict so it would be worth it
            # to even create the tree (it takes time to create a tree of 20 thousand words). however, if you'd make the
            # board much bigger our program would run faster than non-tree programs
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

##############################################################################
#                                 Functions                                  #
##############################################################################


def initialize_trie(words):
    """
        this function gets a list of words and creates a letter tree out of them
        param: words - a list of words to create word tree
        return: a root object of the letter tree
    """
    root = trie.TrieNode('*')
    for word in words:
        trie.add(root, word)

    return root


def get_word_list(file_name = DICT_FILE):
    """
        this function gets a file name and reads all the data from the file
        param: file_name - the file to extract data from
        return: a string of all the data
    """
    with open(file_name, "r") as myfile:
        return myfile.read()


def is_valid_path(board, path, words):
    """
        this function gets a board, path in it and words and returns whether the path is legal (is acctually a walkable
        path inside the board limits and represents a legal word
        param: board - a board of letters, list of lists
        param: path - the path to check, a list of tuple coordinates
        param: words - a list of legal words
        return: an str of the word tha path represents if the path is legal and None if it isn't
    """
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
    """
        this function gets a list of words and returns the length of the longest word
    """
    max_len = 0
    for word in words:
        if len(word) > max_len:
            max_len = len(word)
    return max_len


def find_length_n_paths(n, board, words, root = None):
    """
        this function gets a board and returns a list of length n legal paths in it that represent legal words
        param: n - the length of paths to find
        param: board - a board of letters, list of lists
        param: words - a list of legal words
        param: root - a root object of a letter tree of the words, this is a helper param to help the running time of the program
        return: a list of length n legal paths that represent legal words in the board
    """
    if root is None:
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
    """
        this function gets a board of letters and a path in it and returns the word represented by the path
    """
    word = ""
    for cell in path:
        word += board[cell[0]][cell[1]]
    return word


def find_length_n_words(n, board, words, root = None):
    """
        this function gets a board and returns a list of length n legal words in it
        param: n - the length of paths to find
        param: board - a board of letters, list of lists
        param: words - a list of legal words
        param: root - a root object of a letter tree of the words, this is a helper param to help the running time of the program
        return: a list of length n legal words in the board
    """
    if root is None:
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


def max_score_paths(board, words, root = None):
    """
        this function gets a board and returns a list of paths that represent all the words in the board when each path
        is the longest path possible to get to the word. in a certain board there could be several paths to get to the
        same word.
        param: board - a board of letters, list of lists
        param: words - a list of legal words
        param: root - a root object of a letter tree of the words, this is a helper param to help the running time of the program
        return: a list of paths that represent all the words in the board when each path is the longest path possible
        to get to the word
    """
    if root is None:
        root = initialize_trie(words)

    word_max = get_max_len_word(words)
    path_max = len(board) * len(board[0])
    all_paths = []
    for i in range(min(path_max, word_max)):
        all_paths.extend(find_length_n_paths(i, board, words, root))
        all_paths.extend(find_length_n_words(i, board, words, root))

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

    max_score_path = []
    for path in max_score_words.values():
        max_score_path.append(path)

    return max_score_path
