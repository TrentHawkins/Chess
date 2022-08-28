"""Implements a chessboard.

Referencing with chess algebraic notation is possible.
"""

from dataclasses import dataclass
from .pieces import Piece, Pawn, Bishop, Knight, Rook, Queen, King


Rank = int
File = int
Indices = tuple[Rank, File]


class Square:
    """A square on the chessboard."""

    index_to_file = {index_: file_ for index_, file_ in zip(range(8), "abcdefgh")}  # translate range index to file in chess
    file_to_index = {file_: index_ for index_, file_ in zip(range(8), "abcdefgh")}  # translate file in chess to range index
    index_to_rank = {index_: rank_ for index_, rank_ in zip(range(8), "87654321")}  # translate range index to rank in chess
    rank_to_index = {rank_: index_ for index_, rank_ in zip(range(8), "87654321")}  # translate rank in chess to range index

    @classmethod
    def _indices(cls, square: str) -> Indices:
        """Provide the array indices for a given square.

        Args:
            square: The rank and file.

        Returns:
            Indices.
        """
        return cls.rank_to_index[square[1]], cls.file_to_index[square[0]]

    @classmethod
    def _algebraic_notation(cls, indices: Indices) -> str:
        """Provide the square notation of given array indices.

        Args:
            square: The rank and file of the given square.

        Returns:
            The square in chess notation.
        """
        return cls.index_to_file[indices[1]]+cls.index_to_rank[indices[0]]

    def __init__(self, square: str | Indices):
        """Make square.

        Args:
            square: A square in either chess notation or a couple of indices.
        """
        self.indices = self._indices(square) if isinstance(square, str) else square

    def __repr__(self) -> str:
        """Display indices.

        Returns:
            Indices of square.
        """
        return self._algebraic_notation(self.indices)

    def __add__(self, other: Indices) -> "Square":
        """Move square.

        Args:
            other: index difference to apply to square

        Returns:
            Moved square.
        """
        return Square((self.indices[0] + other[0], self.indices[1] + other[1]))


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
    def _square(cls, square: Square | str):
        """Return square object from string format if such is given.

        Args:
            square: Can be an object or a string in chess notation.
        """
        return square if isinstance(square, Square) else Square(square)

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

    def __setitem__(self, square: Square | str | None, piece: Piece | None):
        """Add a piece to a square.

        Args:
            square: The rank and file of the square.
            piece: The piece to be placed on the square.
        """
        if square:
            i, j = self._square(square).indices
            self._board[i][j] = piece

    def __getitem__(self, square: Square | str | None) -> Piece | None:
        """Get the piece of a given square.

        Args:
            square: The rank and file of the square.

        Returns:
            The piece on the given square.
        """
        if square:
            i, j = self._square(square).indices
            return self._board[i][j]

    def __delitem__(self, square: Square | str | None):
        """Remove the piece of a given square.

        Args:
            square: The rank and file of the square on which to remove a piece (if any).
        """
        if square:
            i, j = self._square(square).indices
            self._board[i][j] = None

    def __contains__(self, piece: Piece | None) -> bool:
        """Check if a piece is on the board.

        Args:
            piece: Basically type and color of piece to be checked.

        Returns:
            If piece is in board.
        """
        return any(piece in rank for rank in self._board)

    def square_of(self, piece: Piece | None) -> Square | None:
        """Return the square of a specific piece.

        Args:
            piece: Piece object to fetch the square of.

        Returns:
            The square of the piece in chess notation or indices or None if it is not on the board.
        """
        for i, rank in enumerate(self._board):
            for j, piece_in_square in enumerate(rank):
                if piece_in_square is piece:
                    return Square((i, j))
