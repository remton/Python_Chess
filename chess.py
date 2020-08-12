# Chess.py
# This is the main file that is run in this program
import chess_board
import chess_pieces
import util
from chess_board import ChessBoard
import preset_boards
import gui


# colors are represented by their first letter everywhere except here
color_playing = 'white'
color_waiting = 'black'
starting_pos = preset_boards.checkmate_1
cb = ChessBoard(starting_pos)
is_game_over = False
checkmate_end = False
draw_end = False
while not is_game_over:
    while True:
        gui.open_window(cb)
        move_str = gui.last_move
        split_move_str = move_str.split(',')
        start_str = split_move_str[0]
        end_str = split_move_str[1]

        move_results = cb.move(start_str, end_str, color_playing)
        if move_results.success:
            if move_results.white_in_check or move_results.black_in_check:
                print('Check!')
            if move_results.white_checkmated or move_results.black_checkmated:
                print('Checkmate!')
                checkmate_end = True
                is_game_over = True
            if move_results.is_draw:
                print('Game is a draw')
                draw_end = True
                is_game_over = True
            temp = color_playing
            color_playing = color_waiting
            color_waiting = temp
            break
        else:
            print(f"Move Failed: {move_results.fail_cause}")
gui.open_endgame_window(checkmate_end, draw_end)
