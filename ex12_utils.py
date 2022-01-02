from copy import deepcopy
import ast



def is_valid_path(board, path, words):
    word = ""
    for path_node_index in range(len(path)):
        path_node = path[path_node_index]
        if path_node_index > 0:
            prev_node = path[path_node_index-1]
            if path_node[0] != prev_node[0] and path_node[1] != prev_node[1]:
                return None
        print(path_node)
        word += board[path_node[0]][path_node[1]]
    print(word)
    if word in words:
        return word
    else:
        return None


def get_word_list(file_name):
    with open(file_name, "r") as myfile:
        return myfile.read()


def write_in_file(file_name, to_write):
    allready_in_file = get_word_list(file_name)
    to_write = str(to_write)
    with open(file_name, "w") as myfile:
        if allready_in_file is not None:
            to_write = allready_in_file + "!" + to_write
        if to_write is not None:
            myfile.write(to_write)


def get_max_len_word(words):
    max_len = 0
    for word in words:
        if len(word) > max_len:
            max_len = len(word)
    return max_len


def find_length_n_paths(n, board, words):
    if n > get_max_len_word(words) or n <= 0:
        return []
    with open(SAVE_PATH_FILE, "w") as myfile:
        myfile.write("")

    all_paths = []
    for x_index in range(len(board[0])):
        for y_index in range(len(board)):
            start_cell = (x_index, y_index)
            all_paths.append(find_length_n_path_from_cell(start_cell, n, board, [start_cell], [], []))

    legal_paths = []
    for i in range(n-1):
        all_paths = flatten(all_paths)
    for path in all_paths:
        word = ""
        for cell in path:
            word += board[cell[0]][cell[1]]
        if word in words:
            if len(word) == n:
                path_to_append = []
                for cell in path:
                    reversed_cell = tuple(reversed(cell))
                    path_to_append.append(reversed_cell)
                legal_paths.append(path_to_append)
                print(word)

    return legal_paths


def flatten(t):
    return [item for sublist in t for item in sublist]


def find_length_n_path_from_cell(start_cell, n, board, path, added_path, all_paths):
    if n > 1:
        start_x = start_cell[0]
        start_y = start_cell[1]
        cells_to_append = []
        if start_x > 0:
            new_cell = (start_x-1, start_y)
            cells_to_append.append(new_cell)
        if start_x < len(board[0]) - 1:
            new_cell = (start_x + 1, start_y)
            cells_to_append.append(new_cell)
        if start_y > 0:
            new_cell = (start_x, start_y-1)
            cells_to_append.append(new_cell)
        if start_y < len(board) - 1:
            new_cell = (start_x, start_y+1)
            cells_to_append.append(new_cell)
        if start_y > 0 and start_x > 0:
            new_cell = (start_x-1, start_y-1)
            cells_to_append.append(new_cell)
        if start_y < len(board)-1 and start_x < len(board[0])-1:
            new_cell = (start_x+1, start_y+1)
            cells_to_append.append(new_cell)
        if start_y < len(board) - 1 and start_x > 0:
            new_cell = (start_x-1, start_y+1)
            cells_to_append.append(new_cell)
        if start_y > 0 and start_x < len(board[0])-1:
            new_cell = (start_x+1, start_y-1)
            cells_to_append.append(new_cell)
        path_to_return = deepcopy(all_paths)
        for cell in cells_to_append:
            if cell not in path:
                new_path = deepcopy(path)
                new_path.append(cell)

                path_to_return.append(find_length_n_path_from_cell(cell, n - len(board[cell[0]][cell[1]]), board, new_path, added_path, all_paths))
        return path_to_return
    else:
        return(path)


def find_length_n_words_path_from_cell(start_cell, n, board, path, added_path, all_paths):
    if n > 1:
        start_x = start_cell[0]
        start_y = start_cell[1]
        cells_to_append = []

        if start_x > 0:
            new_cell = (start_x-1, start_y)
            cells_to_append.append(new_cell)
        if start_x < len(board[0]) - 1:
            new_cell = (start_x + 1, start_y)
            cells_to_append.append(new_cell)
        if start_y > 0:
            new_cell = (start_x, start_y-1)
            cells_to_append.append(new_cell)
        if start_y < len(board) - 1:
            new_cell = (start_x, start_y+1)
            cells_to_append.append(new_cell)
        if start_y > 0 and start_x > 0:
            new_cell = (start_x-1, start_y-1)
            cells_to_append.append(new_cell)
        if start_y < len(board)-1 and start_x < len(board[0])-1:
            new_cell = (start_x+1, start_y+1)
            cells_to_append.append(new_cell)
        if start_y < len(board) - 1 and start_x > 0:
            new_cell = (start_x-1, start_y+1)
            cells_to_append.append(new_cell)
        if start_y > 0 and start_x < len(board[0])-1:
            new_cell = (start_x+1, start_y-1)
            cells_to_append.append(new_cell)

        path_to_return = deepcopy(all_paths)
        for cell in cells_to_append:
            if cell not in path:
                new_path = deepcopy(path)
                new_path.append(cell)

                path_to_extend = find_length_n_path_from_cell(cell, n - 1, board, new_path, added_path, all_paths)
                path_to_return.append(path_to_extend)
        return path_to_return
    else:
        return path


def find_length_n_words(n, board, words):
    with open(SAVE_PATH_FILE, "w") as myfile:
        myfile.write("")

    all_paths = []
    for x_index in range(len(board[0])):
        for y_index in range(len(board)):
            start_cell = (x_index, y_index)
            all_paths.append(find_length_n_words_path_from_cell(start_cell, n, board, [start_cell], [], []))

    legal_paths = []
    for i in range(n-1):
        all_paths = flatten(all_paths)
    for path in all_paths:
        word = ""
        # print(path)
        for cell in path:
            word += board[cell[0]][cell[1]]
        if word in words:
            path_to_append = []
            for cell in path:
                reversed_cell = tuple(reversed(cell))
                path_to_append.append(reversed_cell)
            print(word)
            legal_paths.append(path_to_append)

    return legal_paths



def max_score_paths(board, words):
    pass
