##############################################################################
#                            FILE DESCRIPTION                                #
##############################################################################
# ex11_utils.py WRITER : Adi zuarets - 208708925, renana gabbai - 207743089
# intro cs ex11 2022-2023 DESCRIPTION: A program that runs 4 main functions
# related to the BOGGLE game, and auxiliary functions that support the
# main functions

##############################################################################
#                                  IMPORT                                    #
##############################################################################
from typing import List, Tuple, Iterable, Optional

##############################################################################
#                                  PERMANENT                                #
##############################################################################

# Typing templates
Board = List[List[str]]
Path = List[Tuple[int, int]]

# Reserved text
EMPTY = ""
FLAG_PATH = "path"
FLAG_WORD = "word"

##############################################################################
#                                  FUNCTIONS                                #
##############################################################################


def helper_next_cell_val(cell: tuple, next_cell: tuple) -> bool:
    """
    This function check if the next cell is near to the current cell
    :param cell: current cell
    :param next_cell: the next cell in the path
    :return: True if valid, else False
    """
    row_cell, col_cell = cell
    row_next, col_next = next_cell

    if (row_cell == row_next) and (col_cell == col_next + 1
                                   or col_cell == col_next - 1):
        return True

    if (col_cell == col_next) and (row_cell == row_next + 1 or
                                   row_cell == row_next - 1):
        return True

    if (row_cell == row_next + 1 and col_cell == col_next + 1) or \
            (row_cell == row_next - 1 and col_cell == col_next - 1):
        return True

    if (row_cell == row_next + 1 and col_cell == col_next - 1) or \
            (row_cell == row_next - 1 and col_cell == col_next + 1):
        return True

    return False


def is_valid_path(board: Board, path: Path, words: Iterable[str]) \
        -> Optional[str]:
    """
    This function check if the chosen path is valid to this board
    :param board: Boggle board game
    :param path: path of chosen cells from board
    :param words: a list of legal words
    :return: None if not valid, else return the word that is given from the path
    """
    if len(path) == 0:
        return None

    last_cell_row, last_cell_col = path[-1]
    word = EMPTY

    if not in_range(board, last_cell_row, last_cell_col):  # the last cell
        return None

    checked_path = [(last_cell_row, last_cell_col)]
    for i in range(len(path) - 1):
        row_path, col_path = path[i]
        if in_range(board, row_path, col_path) and path[i] \
                not in checked_path:  # checks if in range
            if helper_next_cell_val(path[i], path[i + 1]):
                checked_path.append((row_path, col_path))
                word += board[row_path][col_path]
                continue
        return None

    word += board[last_cell_row][last_cell_col]

    if word in words:
        return word


def path_to_word(board: Board, path: Path) -> str:
    """
    Helper function, This function gets a path of cells from
    the bord and create the chosen word
    :param board:Boggle board game
    :param path:path of chosen cells from board
    :return: chosen word
    """
    word = EMPTY
    for cell in path:
        word += board[cell[0]][cell[1]]

    return word


def in_range(board: Board, row: int, col: int) -> bool:
    """
    Helper function, this function get specific index and checks
    whether it is in the range of the board
    :param board: Boggle board game
    :param row: index row
    :param col: index row
    :return: True - if in the range, False otherwise
    """
    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        return True
    else:
        return False


def list_val_neighbors_cells(row: int, col: int) -> list:
    """
    helper function. Gets the last cell that the main function
    inserted and returns a list of all optional cells for the next insertion
    :param row: current cell row
    :param col: current cell col
    :return: List of optional cells
    """
    list_cells = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                  (row, col - 1), (row, col + 1), (row + 1, col - 1),
                  (row + 1, col), (row + 1, col + 1)]
    return list_cells


def val_letter_board(board: Board) -> str:
    """
    Helper function for building a word bank adapted to the game board.
    The function receives all the letters that
    appear on the game board and creates a
    str of letters relevant to that game board
    :param board: Boggle board game
    :return: str of letters relevant to the game board
    """
    letters = EMPTY
    for row in range(len(board)):
        for col in range(len(board[0])):
            letters += (board[row][col])
    return letters


def filter_words(board: Board, words: Iterable[str]) -> tuple:
    """
    This function building a word bank adapted to the game board.
    :param board: Boggle board game
    :param words: All optional words in Boggle game
    :return: two sets, One with all the words relevant
     to a game board and the other with the parts of the relevant words
    """
    val_words = set()
    part_words = set()
    val_letters = val_letter_board(board)

    for word in words:
        flag = True

        for char in word:  # if letter in word not in board
            if char not in val_letters:
                flag = False
                break

        if flag:
            val_words.add(word)  # set of val words
            seq_word = EMPTY

            for letter in word:  # set of parts val words
                seq_word += letter
                part_words.add(seq_word)

    return part_words, val_words


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) \
        -> List[Path]:
    """
    This function receives a path length,
    the function builds all possible paths in the game board that
    present a valid word
    :param n: path length
    :param board: Boggle board game
    :param words: Bank of valid words
    :return: all the valid paths on the board game in n long
    """
    paths_list = []
    part_words, val_words = filter_words(board, words)

    for row_cell in range(len(board)):
        for col_cell in range(len(board[0])):
            helper_length_n(n, board, paths_list, part_words, val_words,
                                  [(row_cell, col_cell)], row_cell, col_cell,
                                  FLAG_PATH)

    return paths_list


def helper_length_n(n: int, board: list, paths_list: list,
                          part_words: set, val_words: set, cur_path: Path,
                          cur_row: int, cur_col: int, flag: str) -> None:
    """
    Backtracking function that creates a valid path of words from the
     board, and according to the flag returns a path of length n or a
     path of a word of length n
    :param n: a number which represents the length of the returned path
    :param board: a Boggle board
    :param paths_list: a list of all the paths
    :param part_words: a list of part of legal words
    :param val_words: a list of legal words
    :param cur_path: the current path we are checking
    :param cur_row: current row that we are checking
    :param cur_col: current column that we are checking
    :param flag: a flag that alerts the type of list that be returned
    :return: None
    """

    if flag == FLAG_PATH:
        if len(cur_path) == n:  # stop conditions for find n length path
            if path_to_word(board, cur_path) in val_words:
                paths_list.append(list(cur_path))
            return None

    if flag == FLAG_WORD:
        word = path_to_word(board, cur_path)
        if len(word) == n:  # stop conditions for find n length word
            if word in val_words:
                paths_list.append(list(cur_path))
            return None

    list_cells = list_val_neighbors_cells(cur_row, cur_col)

    for row, col in list_cells:

        if in_range(board, row, col) and (row, col) not in cur_path:
            word = path_to_word(board, cur_path)

            if word in part_words:
                cur_path.append((row, col))
                helper_length_n(n, board, paths_list, part_words, val_words,
                                cur_path, row, col, flag)
                cur_path.pop()


def find_length_n_words(n: int, board: Board, words: Iterable[str]) \
        -> List[Path]:
    """
    This function receives a word length,
    the function builds all possible paths in the game board that
    present a valid word
    :param n: word length
    :param board: Boggle board game
    :param words: Bank of valid words
    :return: all the valid paths on the board game that present words in n long
    """
    part_words, val_words = filter_words(board, words)
    paths_list = []
    for row_cell in range(len(board)):
        for col_cell in range(len(board[0])):
            helper_length_n(n, board, paths_list, part_words, val_words,
                                  [(row_cell, col_cell)], row_cell, col_cell,
                                  FLAG_WORD)

    return paths_list


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    This function builds all the legal paths in
     the game which earn the player the most points he can get
    :param board: Boggle board game
    :param words:Bank of valid words
    :return: all the valid paths on the board game
     with the highest score
    """
    dict_high_grade = {}
    max_size = min(len(board) * len(board[0]), len(max(words, key=len)))
    # max length between the size of the board and the longest word in words

    for num in range(max_size, 0, -1):  # start from max len word (=max grade)
        list_paths = find_length_n_paths(num, board, words)

        for path in list_paths:
            cur_word = path_to_word(board, path)

            if cur_word not in dict_high_grade:  # no duplicates
                dict_high_grade[cur_word] = path

    return list(dict_high_grade.values())
