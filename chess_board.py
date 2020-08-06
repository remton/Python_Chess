from chess_pieces import EmptyPiece
from util import board_to_space, row_to_board, col_to_board
import copy
import preset_boards


# Due to how this code is written indexing a space in the board is done [number][letter] like ['1']['a'] meaning a1
def str_to_space(space_str):
    space = [board_to_space[space_str[1]], board_to_space[space_str[0]]]
    return space


class Space:
    def __init__(self, piece):
        self.piece = piece
        self.white_attacks = False
        self.black_attacks = False
        self.can_white_en_passant = False
        self.can_black_en_passant = False
        self.white_attackers = []
        self.black_attackers = []

    # Called right after a move is made see ChessBoard.on_move()
    def on_move(self, color):
        if color == 'w':
            self.can_white_en_passant = False
        if color == 'b':
            self.can_black_en_passant = False

    def clear_attacks(self):
        self.white_attacks = False
        self.black_attacks = False
        self.white_attackers.clear()
        self.black_attackers.clear()

    def set_attack(self, color, piece=None):
        if color == 'w' or color == 'white':
            self.white_attacks = True
            if piece is not None:
                self.white_attackers.append(piece)
        if color == 'b' or color == 'black':
            self.black_attacks = True
            if piece is not None:
                self.black_attackers.append(piece)

    def is_enemy_attacking(self, color):
        if color == 'w' and self.black_attacks:
            return True
        if color == 'b' and self.white_attacks:
            return True
        return False


def preset_to_board(preset):
    board = []
    row = []
    for y in range(8):
        row.clear()
        for x in range(8):
            row.append(Space(preset[y][x]))
        board.append(row.copy())
    return board


# This class holds the results of the move which is used by app.py
class MoveResults:
    def __init__(self, success, fail_cause='',
                 white_checkmated=False, black_checkmated=False,
                 white_in_check=False, black_in_check=False):
        self.white_checkmated = white_checkmated
        self.black_checkmated = black_checkmated
        self.white_in_check = white_in_check
        self.black_in_check = black_in_check
        if success:
            self.success = True
            self.fail = False
            self.fail_cause = 'No Failure'
        else:
            self.success = False
            self.fail = True
            self.fail_cause = fail_cause


class ChessBoard:
    def __init__(self, preset=preset_boards.default_board):
        self.board = preset_to_board(preset)
        self.set_piece_locations()
        self.set_attacks()

    # print_board prints out a text representation of the board NOT a gui representation
    def print_board(self):
        output = '\n=========================================\n| '
        for y in range(8):
            for x in range(8):
                output += self.board[7 - y][x].piece.color + self.board[7 - y][x].piece.abr + ' | '
            if y != 7:
                output += '\n=========================================\n| '
            else:
                output += '\n========================================='
        print(output)

    def set_piece_locations(self):
        for y in range(8):
            for x in range(8):
                self.board[y][x].piece.location = [y, x]

    def set_attacks(self):
        for y in range(8):
            for x in range(8):
                self.board[y][x].clear_attacks()
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x].piece
                self.board[y][x].piece.attack(self.board, [y, x])

    # Called right before move() returns True
    def on_move(self, color):
        for y in range(8):
            for x in range(8):
                self.board[y][x].on_move(color)

    # Makes the move regardless of legality (used in move() after legality check)
    def force_move(self, start, end):
        piece = self.board[start[0]][start[1]].piece
        self.board[end[0]][end[1]].piece = piece
        self.board[start[0]][start[1]].piece = EmptyPiece()
        if piece.name == 'Pawn':
            piece.is_first_move = False
            if piece.took_en_passant:
                self.board[piece.en_passant_capture[0]][piece.en_passant_capture[1]].piece = EmptyPiece()
        if piece.name == 'Rook':
            piece.is_first_move = False
        if piece.name == 'King':
            piece.is_first_move = False
            if piece.need_castle:
                castle_rook = self.board[piece.castle_rook_start[0]][piece.castle_rook_start[1]].piece
                castle_rook.is_first_move = False
                self.board[piece.castle_rook_end[0]][piece.castle_rook_end[1]].piece = castle_rook
                self.board[piece.castle_rook_start[0]][piece.castle_rook_start[1]].piece = EmptyPiece()
        self.set_piece_locations()
        self.set_attacks()

    # Makes the given move on a copy of this board and checks if the given color has a king in check
    def does_move_into_check(self, start, end, color):
        temp_cb = copy.deepcopy(self)
        temp_cb.force_move(start, end)
        temp_cb.set_attacks()
        for y in range(8):
            for x in range(8):
                piece = temp_cb.board[y][x].piece
                if piece.name == 'King' and piece.color == color:
                    if piece.is_in_check(temp_cb.board):
                        return True
        return False

    # Returns if the given color is in check
    def is_in_check(self, color):
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x].piece
                if piece.name == 'King' and piece.color == color:
                    return piece.is_in_check(self.board)

    # Brute-Force approach is ugly but it works*
    # Returns if the given color is checkmated
    def is_checkmated(self, color):
        temp_cb = None
        for y in range(8):
            for x in range(8):
                temp_cb = copy.deepcopy(self)
                piece = temp_cb.board[y][x].piece
                if piece.color == color:
                    for check_y in range(8):
                        for check_x in range(8):
                            start = [y, x]
                            end = [check_y, check_x]
                            if temp_cb.check_legal(start, end):
                                if not temp_cb.does_move_into_check(start, end, color):
                                    return False
        return True


    # start_str and end_str should be strings like a1, c4, etc.
    def check_legal(self, start, end):
        return self.board[start[0]][start[1]].piece.is_legal_move(self.board, start, end)

    # This does check if the move is legal and will not make illegal moves
    # Returns True if the move was made
    # Note: color_playing is the only place in code where the colors aren't abbreviated
    # that's why you see color_playing[0] to get the abbreviation
    def move(self, start_str, end_str, color_playing):
        start = str_to_space(start_str)
        end = str_to_space(end_str)
        piece = self.board[start[0]][start[1]].piece
        if piece.color != color_playing[0]:
            return MoveResults(success=False, fail_cause=f'{color_playing} to move')
        if self.check_legal(start, end):
            if not self.does_move_into_check(start, end, color_playing[0]):
                self.force_move(start, end)
                self.on_move(color_playing[0])
                if self.is_checkmated('w'):
                    return MoveResults(success=True, white_checkmated=True)
                if self.is_checkmated('b'):
                    return MoveResults(success=True, black_checkmated=True)
                if self.is_in_check('w'):
                    return MoveResults(success=True, white_in_check=True)
                if self.is_in_check('b'):
                    return MoveResults(success=True, black_in_check=True)
                return MoveResults(success=True)
            else:
                return MoveResults(success=False, fail_cause=f'Move leaves {color_playing} in check')
        else:
            return MoveResults(success=False, fail_cause='Illegal move by piece definition')