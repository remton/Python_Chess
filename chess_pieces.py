import math
import util
from numpy import sign
from util import row_to_board, col_to_board, empty_abr, empty_color


class EmptyPiece:
    def __init__(self):
        # location is [y, x]
        self.location = []
        self.name = 'Empty'
        self.attacked_spaces = [[]]
        self.img_name = f'Empty'
        self.points = 0
        self.color = empty_color
        self.abr = empty_abr

    def is_legal_move(self, board, start, end):
        return False

    # sets the spaces that this piece attacks to attacked
    def attack(self, board, location):
        self.attacked_spaces.clear()


# Note: en passant currently does not exist
class Pawn:
    def __init__(self, color):
        self.location = []
        self.name = 'Pawn'
        self.img_name = f'Pawn_{color}'
        self.points = 1
        self.color = color
        self.abr = 'P'
        self.attacked_spaces = [[]]
        self.is_first_move = True
        self.took_en_passant = False
        self.en_passant_capture = []
        if color != 'w':
            self.forward = 1
        else:
            self.forward = -1

    def is_legal_move(self, board, start, end):
        x_difference = abs(end[1] - start[1])
        y_difference = abs(end[0] - start[0])
        if board[end[0]][end[1]].piece.color == self.color:
            return False
        if x_difference > 1 or y_difference > 2:
            return False
        if x_difference == 0 and board[end[0]][end[1]].piece.name != 'Empty':
            return False
        if sign(start[0] - end[0]) != sign(self.forward):
            return False
        if y_difference != 1 and not self.is_first_move:
            return False
        # sets up en passant
        if y_difference == 2:
            if board[start[0] - self.forward][end[1]].piece.abr != empty_abr:
                return False
            if x_difference == 0:
                if self.color == 'w':
                    board[end[0] + self.forward][end[1]].can_black_en_passant = True
                if self.color == 'b':
                    board[end[0] + self.forward][end[1]].can_white_en_passant = True
                return True
        # Takes en passant
        if x_difference == 1 and board[end[0]][end[1]].piece.name == 'Empty':
            if self.color == 'w' and board[end[0]][end[1]].can_white_en_passant:
                self.took_en_passant = True
                self.en_passant_capture = [end[0] + self.forward, end[1]]
            elif self.color == 'b' and board[end[0]][end[1]].can_black_en_passant:
                self.took_en_passant = True
                self.en_passant_capture = [end[0] + self.forward, end[1]]
            else:
                return False
        return True

    def attack(self, board, location):
        self.attacked_spaces.clear()
        # This is a white pawn
        if self.forward > 0:
            try:
                board[location[0] + 1][location[1] + 1].set_attack(self.color, self.name)
                self.attacked_spaces.append([location[0] + 1, location[1] + 1])
            except IndexError:
                pass
            try:
                board[location[0] + 1][location[1] - 1].set_attack(self.color, self.name)
                self.attacked_spaces.append([location[0] + 1, location[1] - 1])
            except IndexError:
                pass
        # This is a black pawn
        if self.forward < 0:
            try:
                board[location[0] - 1][location[1] + 1].set_attack(self.color, self.name)
                self.attacked_spaces.append([location[0] - 1, location[1] + 1])
            except IndexError:
                pass
            try:
                board[location[0] - 1][location[1] - 1].set_attack(self.color, self.name)
                self.attacked_spaces.append([location[0] - 1, location[1] - 1])
            except IndexError:
                pass


class Knight:
    def __init__(self, color):
        self.location = []
        self.name = 'Knight'
        self.img_name = f'Knight_{color}'
        self.points = 3
        self.color = color
        self.abr = 'N'
        self.attacked_spaces = [[]]

    def is_legal_move(self, board, start, end):
        if (abs(start[0] - end[0]) + abs(start[1] - end[1])) != 3:
            return False
        if board[end[0]][end[1]].piece.color == self.color:
            return False
        return True

    def attack(self, board, location):
        self.attacked_spaces.clear()
        if util.has_index2D(board, location[0] + 1, location[1] + 2):
            board[location[0] + 1][location[1] + 2].set_attack(self.color, self.name)
            self.attacked_spaces.append([location[0] + 1, location[1] + 2])

        if util.has_index2D(board, location[0] - 1, location[1] + 2):
            board[location[0] - 1][location[1] + 2].set_attack(self.color, self.name)
            self.attacked_spaces.append([location[0] - 1, location[1] + 2])

        if util.has_index2D(board, location[0] + 1, location[1] - 2):
            board[location[0] + 1][location[1] - 2].set_attack(self.color, self.name)
            self.attacked_spaces.append([location[0] + 1, location[1] - 2])

        if util.has_index2D(board, location[0] - 1, location[1] - 2):
            board[location[0] - 1][location[1] - 2].set_attack(self.color, self.name)
            self.attacked_spaces.append([location[0] - 1, location[1] - 2])

        if util.has_index2D(board, location[0] + 2, location[1] + 1):
            board[location[0] + 2][location[1] + 1].set_attack(self.color, self.name)
            self.attacked_spaces.append([location[0] + 2, location[1] + 1])

        if util.has_index2D(board, location[0] - 2, location[1] + 1):
            board[location[0] - 2][location[1] + 1].set_attack(self.color, self.name)
            self.attacked_spaces.append([location[0] - 2, location[1] + 1])

        if util.has_index2D(board, location[0] + 2, location[1] - 1):
            board[location[0] + 2][location[1] - 1].set_attack(self.color, self.name)
            self.attacked_spaces.append([location[0] + 2, location[1] - 1])

        if util.has_index2D(board, location[0] - 2, location[1] - 1):
            board[location[0] - 2][location[1] - 1].set_attack(self.color, self.name)
            self.attacked_spaces.append([location[0] - 2, location[1] - 1])


class Bishop:
    def __init__(self, color):
        self.location = []
        self.name = 'Bishop'
        self.img_name = f'Bishop_{color}'
        self.points = 3
        self.color = color
        self.abr = 'B'
        self.attacked_spaces = [[]]

    def is_legal_move(self, board, start, end):
        if board[end[0]][end[1]].piece.color == self.color:
            return False
        if end not in self.attacked_spaces:
            return False
        return True

    def attack(self, board, location):
        self.attacked_spaces.clear()
        y = location[0]
        x = location[1]
        # up and to the right
        for i in range(1, util.get_lower(8 - location[0], 8 - location[1])):
            y = y + 1
            x = x + 1
            board_piece = board[y][x].piece
            if board_piece.color == empty_color:
                board[y][x].set_attack(self.color, self.name)
                self.attacked_spaces.append([y, x])
            else:
                if self.color == board_piece.color:
                    break
                else:
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y, x])
                    break
        y = location[0]
        x = location[1]
        # up and to the left
        for i in range(1, util.get_lower(8 - location[0], location[1] + 1)):
            y = y + 1
            x = x - 1
            board_piece = board[y][x].piece
            if board_piece.color == empty_color:
                board[y][x].set_attack(self.color, self.name)
                self.attacked_spaces.append([y, x])
            else:
                if self.color == board_piece.color:
                    break
                else:
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y, x])
                    break
        y = location[0]
        x = location[1]
        # down and to the right
        for i in range(1, util.get_lower(location[0] + 1, 8 - location[1])):
            y = y - 1
            x = x + 1
            board_piece = board[y][x].piece
            if board_piece.color == empty_color:
                board[y][x].set_attack(self.color, self.name)
                self.attacked_spaces.append([y, x])
            else:
                if self.color == board_piece.color:
                    break
                else:
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y, x])
                    break
        y = location[0]
        x = location[1]
        # down and to the left
        for i in range(1, util.get_lower(location[0] + 1, location[1] + 1)):
            y = y - 1
            x = x - 1
            board_piece = board[y][x].piece
            if board_piece.color == empty_color:
                board[y][x].set_attack(self.color, self.name)
                self.attacked_spaces.append([y,x])
            else:
                if self.color == board_piece.color:
                    break
                else:
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y,x])
                    break


class Rook:
    def __init__(self, color):
        self.location = []
        self.name = 'Rook'
        self.img_name = f'Rook_{color}'
        self.points = 5
        self.color = color
        self.abr = 'R'
        self.attacked_spaces = [[]]
        self.is_first_move = True

    def is_legal_move(self, board, start, end):
        if board[end[0]][end[1]].piece.color == self.color:
            return False
        if end not in self.attacked_spaces:
            return False
        return True

    def attack(self, board, location):
        self.attacked_spaces.clear()
        y = location[0]
        x = location[1]
        # Up
        for y in range(location[0] + 1, 8):
            board_piece = board[y][x].piece
            if board_piece.color == empty_color:
                board[y][x].set_attack(self.color, self.name)
                self.attacked_spaces.append([y, x])
            else:
                if self.color == board_piece.color:
                    break
                else:
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y, x])
                    break
        y = location[0]
        x = location[1]
        # Down
        for y in range(location[0] - 1, 0, -1):
            board_piece = board[y][x].piece
            if board_piece.color == empty_color:
                board[y][x].set_attack(self.color, self.name)
                self.attacked_spaces.append([y, x])
            else:
                if self.color == board_piece.color:
                    break
                else:
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y, x])
                    break
        y = location[0]
        x = location[1]
        # Left
        for x in range(location[1] - 1, 0, -1):
            board_piece = board[y][x].piece
            if board_piece.color == empty_color:
                board[y][x].set_attack(self.color, self.name)
                self.attacked_spaces.append([y, x])
            else:
                if self.color == board_piece.color:
                    break
                else:
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y, x])
                    break
        y = location[0]
        x = location[1]
        # Right
        for x in range(location[1] + 1, 8):
            board_piece = board[y][x].piece
            if board_piece.color == empty_color:
                board[y][x].set_attack(self.color, self.name)
                self.attacked_spaces.append([y, x])
            else:
                if self.color == board_piece.color:
                    break
                else:
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y, x])
                    break


class Queen:
    def __init__(self, color):
        self.location = []
        self.name = 'Queen'
        self.img_name = f'Queen_{color}'
        self.points = 8
        self.color = color
        self.abr = 'Q'
        self.attacked_spaces = [[]]

    def is_legal_move(self, board, start, end):
        if board[end[0]][end[1]].piece.color == self.color:
            return False
        if end not in self.attacked_spaces:
            return False
        return True

    def attack(self, board, location):
        self.attacked_spaces.clear()
        rook_check = Rook(self.color)
        bishop_check = Bishop(self.color)
        rook_check.attack(board, location)
        bishop_check.attack(board, location)
        for space in rook_check.attacked_spaces:
            self.attacked_spaces.append(space)
        for space in bishop_check.attacked_spaces:
            self.attacked_spaces.append(space)


class King:
    def __init__(self, color):
        self.location = []
        self.name = 'King'
        self.img_name = f'King_{color}'
        self.points = math.inf
        self.color = color
        self.abr = 'K'
        self.attacked_spaces = [[]]
        self.is_first_move = True
        self.need_castle = False
        self.castle_rook_start = [0, 0]
        self.castle_rook_end = [0, 0]

    def is_legal_move(self, board, start, end):
        if board[end[0]][end[1]].piece.color == self.color:
            return False
        y_difference = end[0] - start[0]
        x_difference = end[1] - start[1]
        if abs(y_difference) > 1:
            return False

        if board[end[0]][end[1]].is_enemy_attacking(self.color):
            return False

        # Castling implementation
        self.need_castle = False
        self.castle_rook_start = [0, 0]
        self.castle_rook_end = [0, 0]
        if abs(x_difference) > 1:
            self.need_castle = True
            if not self.is_first_move or abs(x_difference) != 2:
                return False
            if self.color == 'w':
                # white castles short
                if x_difference == 2:
                    if board[0][7].piece.name == 'Rook' and board[0][7].piece.is_first_move:
                        self.castle_rook_start = [0, 7]
                        self.castle_rook_end = [0, 5]
                    else:
                        return False
                # white castles long
                elif x_difference == -2:
                    if board[0][0].piece.name == 'Rook' and board[0][0].piece.is_first_move:
                        self.castle_rook_start = [0, 0]
                        self.castle_rook_end = [0, 3]
                    else:
                        return False
            else:
                # black castles short
                if x_difference == 2:
                    if board[7][7].piece.name == 'Rook' and board[7][7].piece.is_first_move:
                        self.castle_rook_start = [7, 7]
                        self.castle_rook_end = [7, 5]
                    else:
                        return False
                # black castles long
                elif x_difference == -2:
                    if board[7][0].piece.name == 'Rook' and board[7][0].piece.is_first_move:
                        self.castle_rook_start = [7, 0]
                        self.castle_rook_end = [7, 3]
                    else:
                        return False
        return True

    def attack(self, board, location):
        self.attacked_spaces.clear()
        for y in range(location[0] - 1, location[0] + 2):
            for x in range(location[1] - 1, location[1] + 2):
                if [y, x] == location:
                    continue
                if util.has_index2D(board, y, x):
                    board[y][x].set_attack(self.color, self.name)
                    self.attacked_spaces.append([y, x])

    def is_in_check(self, board):
        if board[self.location[0]][self.location[1]].is_enemy_attacking(self.color):
            return True
