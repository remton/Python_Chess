# gui.py
# Handles all the gui
from tkinter import *
from util import col_to_board, row_to_board
import util

# First thing when working with tkinter
root = Tk()
root.title("Remi's Chess Game")
def on_close():
    raise SystemExit
root.protocol("WM_DELETE_WINDOW", on_close)


# PhotoImage must keep the original variable so this dict allows access to images whenever we want
piece_images = {
    'Empty': PhotoImage(file='Images/Empty.png'),
    'Pawn_w': PhotoImage(file='Images/Pawn_w.png'),
    'Pawn_b': PhotoImage(file='Images/Pawn_b.png'),
    'Knight_w': PhotoImage(file='Images/Knight_w.png'),
    'Knight_b': PhotoImage(file='Images/Knight_b.png'),
    'Bishop_w': PhotoImage(file='Images/Bishop_w.png'),
    'Bishop_b': PhotoImage(file='Images/Bishop_b.png'),
    'Rook_w': PhotoImage(file='Images/Rook_w.png'),
    'Rook_b': PhotoImage(file='Images/Rook_b.png'),
    'Queen_w': PhotoImage(file='Images/Queen_w.png'),
    'Queen_b': PhotoImage(file='Images/Queen_b.png'),
    'King_w': PhotoImage(file='Images/King_w.png'),
    'King_b': PhotoImage(file='Images/King_b.png'),
}


last_move = ''
is_first_button = True
first_space = ''
def on_button_press(space_str):
    global last_move
    global first_space
    global is_first_button
    if is_first_button:
        # This is a weird way to check if the space is empty but it works
        # board is updated in update_grid
        global board
        x = util.board_to_space[space_str[0]]
        y = util.board_to_space[space_str[1]]
        if board[y][x].piece.name == 'Empty':
            return
        first_space = space_str
        is_first_button = False
    else:
        last_move = f'{first_space},{space_str}'
        is_first_button = True
        first_space = ''
        root.quit()


# Unlike with the ChessBoard grid is indexed [x][y]
grid = [[]]

def create_grid():
    back_color = 'gray'
    front_color = 'white'
    grid.clear()
    row = []
    for x in range(8):
        row.clear()
        for y in range(8):
            space = row_to_board[x] + col_to_board[y]
            new_button = Button(root, padx=20, pady=20, bg=back_color, fg=front_color, image=piece_images['Empty'],
                                text=space, command=util.create_lambda(on_button_press, space))
            row.append(new_button)
            temp = back_color
            back_color = front_color
            front_color = temp
        grid.append(row.copy())
        temp = back_color
        back_color = front_color
        front_color = temp

    for x in range(0, 8):
        for y in range(0, 8):
            grid[x][7 - y].grid(column=x+1, row=y)

    # Create the labels for space names
    for x in range(8):
        new_label = Label(root, height=2, width=8, text=row_to_board[x])
        new_label.grid(column=x+1, row=8)
    for y in range(8):
        new_label = Label(root, height=4, width=4, text=col_to_board[y])
        new_label.grid(column=0, row=7-y)


board = None
def update_grid(chess_board):
    global grid
    global board
    board = chess_board.board
    for x in range(8):
        for y in range(8):
            piece = board[y][x].piece
            grid[x][y]['image'] = piece_images[piece.img_name]


def open_window(chess_board, run_loop=True):
    create_grid()
    update_grid(chess_board)
    if run_loop:
        root.mainloop()


def endgame_window_close(end_root):
    end_root.quit()

def open_endgame_window(is_checkmate=False, is_draw=False):
    end_root = Tk()
    if is_checkmate:
        message = "Checkmate!"
    elif is_draw:
        message = "Draw."
    else:
        message = "Error: open_endgame_window needs checkmate or is_draw to be true"
    message_label = Label(end_root, height=5, width=10, text=message)
    message_label.pack()
    continue_button = Button(end_root, padx=20, pady=20, text='continue', command=lambda: endgame_window_close(end_root))
    continue_button.pack()
    end_root.mainloop()
