# preset_boards.py
# Holds 2D lists representing board positions
# Starting position is set at the start of chess.py
from chess_pieces import EmptyPiece, Pawn, Knight, Bishop, Rook, Queen, King


# Since chess boards count from bottom to top, this is not actually upside down
default_board = [
    [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')],
    [Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')],
    [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')]
]

checkmate_1 = [
    [King('w'), EmptyPiece(), Rook('w'), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), Rook('w'), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece()],
    [EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), EmptyPiece(), King('b'), EmptyPiece()]
]
