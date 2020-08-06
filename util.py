# util.py
# Has some miscellaneous utilities used throughout this program

# Due to how this code is written indexing a space in the board is done [number][letter] like ['1']['a'] meaning a1
# Dictionaries used to convert between strings like 'a4' to indexes like [5][0]
board_to_space = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7
}
def str_to_space(space_str):
    space = [board_to_space[space_str[1]], board_to_space[space_str[0]]]
    return space

col_to_board = {
    0: '1',
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6',
    6: '7',
    7: '8',
}
row_to_board = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
}

# Most of the time colors are represented by their character abbreviations
# This dict allows us to convert back easily their names
color_abr_to_name = {
    'w': 'white',
    'b': 'black',
    ' ': ' '
}

# Stuff used for empty spaces/pieces (changing these has not been tested)
empty_abr = ' '
empty_color = ' '

# This was needed to create lambdas in a loop for each button in gui
# using lambda: obj(param) in the loop led to one lambda being used for all buttons
def create_lambda(obj, param):
    return lambda: obj(param)

def get_lower(num1, num2):
    if num1 < num2:
        return num1
    else:
        return num2

# Stops negative indexing and IndexErrors used extensively in chess_pieces
def has_index2D(list, index_1, index_2):
    if index_1 < 0 or index_2 < 0:
        return False
    try:
        list[index_1][index_2]
        return True
    except IndexError:
        return False
