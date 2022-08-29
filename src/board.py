"""Implements a chessboard.

Referencing with chess algebraic notation is possible.
"""

from .pieces import Piece, Pawn, Bishop, Knight, Rook, Queen, King, Move, horizontal, vertical


Rank = int
File = int
Square = tuple[Rank, File]


def rank(square:Square) -> Rank:
    return square[0]


def file(square:Square) -> File:
    return square[1]


def difference(square_left: Square, square_right:Square) -> Move:
    horizontal_ = rank(square_right) - rank(square_left)
    vertical_ = file(square_right) - file(square_left)
    return horizontal_, vertical_       


def advancement(square:Square, move:Move) -> Square:
    rank_ = rank(square) + horizontal(move)
    file_ = file(square) + vertical(move)
    return rank_, file_   


def decrement(move:Move, unit_move:Move) -> Move:
    horizontal_ = horizontal(move) - horizontal(unit_move)
    vertical_ = vertical(move) - vertical(unit_move)
    return horizontal_, vertical_


class Board:
    """A Chessboard.

    Pieces can be assigned, obtained or removed by referencing squares with chess algebraic notation.
    The notation consists of a letter ('A' through 'H') for the file (column) of a square and a number (1-8) for the rank (row).
    The convention here is to match `index+1` to file for columns (inner lists) and `8-index` for rows (reverse row referencing).

    Examples:
        Item at [2][3] is referenced as ["d6"].
        Item at [5][3] is referenced as ["d3"].
        Item at [0][7] is referenced as ["h8"].
        Item at [7][0] is referenced as ["a1"].
    """

    index_to_file = {index_: file_ for index_, file_ in zip(range(8), "abcdefgh")}  # translate range index to file in chess
    file_to_index = {file_: index_ for index_, file_ in zip(range(8), "abcdefgh")}  # translate file in chess to range index
    index_to_rank = {index_: rank_ for index_, rank_ in zip(range(8), "87654321")}  # translate range index to rank in chess
    rank_to_index = {rank_: index_ for index_, rank_ in zip(range(8), "87654321")}  # translate rank in chess to range index

    @classmethod
    def _indices(cls, square: str) -> Square:
        """Provide the array indices for a given square.

        Args:
            square: The rank and file.

        Returns:
            Square.
        """
        return cls.rank_to_index[square[1]], cls.file_to_index[square[0]]

    @classmethod
    def _square(cls, indices: Square) -> str:
        """Provide the square notation of given array indices.

        Args:
            square: The rank and file of the given square.

        Returns:
            The square in chess notation.
        """
        return cls.index_to_file[indices[1]]+cls.index_to_rank[indices[0]]

    def __init__(self):
        """Initialize a chessboard with a new game congifuration."""
        self._board: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]

    #   White pieces on the first rank.
        self["a1"] = Rook("white")
        self["b1"] = Knight("white")
        self["c1"] = Bishop("white")
        self["d1"] = Queen("white")
        self["e1"] = King("white")
        self["f1"] = Bishop("white")
        self["g1"] = Knight("white")
        self["h1"] = Rook("white")

    #   White pawns on the second rank.
        self["a2"] = Pawn("white")
        self["b2"] = Pawn("white")
        self["c2"] = Pawn("white")
        self["d2"] = Pawn("white")
        self["e2"] = Pawn("white")
        self["f2"] = Pawn("white")
        self["g2"] = Pawn("white")
        self["h2"] = Pawn("white")

    #   Black pawns on the seventh rank.
        self["a8"] = Rook("black")
        self["b8"] = Knight("black")
        self["c8"] = Bishop("black")
        self["d8"] = Queen("black")
        self["e8"] = King("black")
        self["f8"] = Bishop("black")
        self["g8"] = Knight("black")
        self["h8"] = Rook("black")

    #   Black pieces on the eighth rank.
        self["a7"] = Pawn("black")
        self["b7"] = Pawn("black")
        self["c7"] = Pawn("black")
        self["d7"] = Pawn("black")
        self["e7"] = Pawn("black")
        self["f7"] = Pawn("black")
        self["g7"] = Pawn("black")
        self["h7"] = Pawn("black")

    def __repr__(self) -> str:
        """Represent the board in proper direction and use the representation of each piece.

        Returns:
            The board representation.
        """
        return (
            "\n▐\033[7m  A B C D E F G H  \033[0m▌\n" +
            "\n".join(
                f"▐\033[7m{self.index_to_rank[index]}\033[27m\033[4m▌" +
                "│".join(str(piece) for piece in rank) +
                f"▐\033[24m\033[7m{self.index_to_rank[index]}\033[0m▌"
                for index, rank in enumerate(self._board)
            ) +
            "\n▐\033[7m  A B C D E F G H  \033[0m▌\n\n"
        ).replace("None", " ")

    def __setitem__(self, square: str | None, piece: Piece | None):
        """Add a piece to a square.

        Args:
            square: The rank and file of the square.
            piece: The piece to be placed on the square.
        """
        if square:
            i, j = self._indices(square)
            self._board[i][j] = piece

    def __getitem__(self, square: str | None) -> Piece | None:
        """Get the piece of a given square.

        Args:
            square: The rank and file of the square.

        Returns:
            The piece on the given square.
        """
        if square:
            i, j = self._indices(square) 
            return self._board[i][j]

    def __delitem__(self, square: str | None):
        """Remove the piece of a given square.

        Args:
            square: The rank and file of the square on which to remove a piece (if any).
        """
        if square:
            i, j = self._indices(square)
            self._board[i][j] = None

    def __contains__(self, piece: Piece | None) -> bool:
        """Check if a piece is on the board.

        Args:
            piece: Basically type and color of piece to be checked.

        Returns:
            If piece is in board.
        """
        return any(piece in rank for rank in self._board)

    def square_of(self, piece: Piece | None, algebraic_notation: bool = True) -> Square | Square | None:
        """Return the square of a specific piece.

        Args:
            piece: Piece object to fetch the square of.

        Returns:
            The square of the piece in chess notation or indices or None if it is not on the board.
        """
        for i, rank in enumerate(self._board):
            for j, square in enumerate(rank):
                if square is piece:
                    return self._square((i, j)) if algebraic_notation else (i, j)

    def movement(self, cur_square:str, goto_square:str) -> bool:
        """Move a piece from its current square to the desired one.

        Checks that there is a piece to move and the movement is valid for the specific piece.
        If it is, execute the move and check whether a piece is captured and update the game score.
        Currently, this does not check if movement is blocked by another piece, be it friend or enemy.
        Args:
            cur_square: the square from which a piece is moved
            got_square: the desired destination square for the piece
        Returns:
            whether the move was valid and carried out.
        """
        piece = self[cur_square]
        if piece is None:
            return False
        move = difference(self._indices(cur_square), self._indices(goto_square))
        # need to check if move is blocked from another piece.
        captured = self[goto_square]
        valid = piece.check_movement(move, captured)
        print(cur_square, valid, move)
        if not valid:
            return False
        blocked = self.check_move_blocked(self._indices(cur_square), move)
        print(cur_square, valid, blocked)
        if not blocked:
            self[cur_square] = None
            self[goto_square] = piece
        if captured is not None:
            # currently this does nothing.
            self.count_score(captured)

        return valid and not blocked

    def count_score(self, captured:Piece) -> None:
        """Counts the score of the game. Not implemented."""
        ...

    def check_move_blocked(self, square:Square, move:Move) -> bool:
        piece = self._board[rank(square)][file(square)]
        # a knight is a special case, it immediatly moves to the goto-square and is only blocked by 
        # piece of the same color.
        if isinstance(piece, Knight):
            square = advancement(square, move)
            other_piece = self._board[rank(square)][file(square)]
            return other_piece is not None and other_piece.is_black == piece.is_black
        blocked = False
        while not blocked:
            # a pawn moving diagonally is a special case, currently not addressed here.
            # we can do this in a previous call (checks whether the move is a valid move for the piece independent of blocking)
            unit_move = piece.unit_move(move)
            move = decrement(move, unit_move)
            # if move reaches goto_square and the color of any chest piece there is different, the chess piece is not blocked
            square = advancement(square, unit_move)
            if move == (0, 0):
                other_piece = self._board[rank(square)][file(square)]
                if other_piece is not None:
                    return other_piece.is_black == piece.is_black
                else:
                    return False
            # even if there is another piece of the opposite color on the square, we decide it blocks movement.
            # another way to handle this is to automatically move the piece up to that square instead of the go-to one.
            # in that case we should return the position the piece moves to, in order to update the board properly.
            blocked = self._board[rank(square)][file(square)] is not None

        return blocked