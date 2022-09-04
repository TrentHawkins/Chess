"""Implements a chessboard.

Referencing with chess algebraic notation is possible.
"""

from functools import singledispatchmethod

from .piece import Bishop, Color, King, Knight, Pawn, Piece, Queen, Rook
from .square import Square, Vector


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

    def __init__(self):
        """Initialize a chessboard with a new game congifuration."""
        self._board: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]

    #   White pieces on the first rank.
        self["a1"] = Rook(Color.WHITE)
        self["b1"] = Knight(Color.WHITE)
        self["c1"] = Bishop(Color.WHITE)
        self["d1"] = Queen(Color.WHITE)
        self["e1"] = King(Color.WHITE)
        self["f1"] = Bishop(Color.WHITE)
        self["g1"] = Knight(Color.WHITE)
        self["h1"] = Rook(Color.WHITE)

    #   White pawns on the second rank.
        self["a2"] = Pawn(Color.WHITE)
        self["b2"] = Pawn(Color.WHITE)
        self["c2"] = Pawn(Color.WHITE)
        self["d2"] = Pawn(Color.WHITE)
        self["e2"] = Pawn(Color.WHITE)
        self["f2"] = Pawn(Color.WHITE)
        self["g2"] = Pawn(Color.WHITE)
        self["h2"] = Pawn(Color.WHITE)

    #   Black pawns on the seventh rank.
        self["a8"] = Rook(Color.BLACK)
        self["b8"] = Knight(Color.BLACK)
        self["c8"] = Bishop(Color.BLACK)
        self["d8"] = Queen(Color.BLACK)
        self["e8"] = King(Color.BLACK)
        self["f8"] = Bishop(Color.BLACK)
        self["g8"] = Knight(Color.BLACK)
        self["h8"] = Rook(Color.BLACK)

    #   Black pieces on the eighth rank.
        self["a7"] = Pawn(Color.BLACK)
        self["b7"] = Pawn(Color.BLACK)
        self["c7"] = Pawn(Color.BLACK)
        self["d7"] = Pawn(Color.BLACK)
        self["e7"] = Pawn(Color.BLACK)
        self["f7"] = Pawn(Color.BLACK)
        self["g7"] = Pawn(Color.BLACK)
        self["h7"] = Pawn(Color.BLACK)

    def __repr__(self) -> str:
        """Represent the board in proper direction and use the representation of each piece.

        Returns:
            The board representation.
        """
        return (
            "\n▐\033[7m  A B C D E F G H  \033[0m▌\n" +
            "\n".join(
                f"▐\033[7m{Square.index_to_rank[index]}\033[27m\033[4m▌" +
                "│".join(str(piece) for piece in rank) +
                f"▐\033[24m\033[7m{Square.index_to_rank[index]}\033[0m▌" for index, rank in enumerate(self._board)
            ) + "\n▐\033[7m  A B C D E F G H  \033[0m▌\n\n"
        ).replace("None", " ")

    def __setitem__(self, square: Square | str, piece: Piece | None):
        """Add a piece to a square.

        Args:
            square: The rank and file of the square.
            piece: The piece to be placed on the square.
        """
        square = Square(square)
        if piece is not None:
            piece.square = square
        self._board[square.rank][square.file] = piece

    def __getitem__(self, square: Square | str) -> Piece | None:
        """Get the piece of a given square.

        Args:
            square: The rank and file of the square.

        Returns:
            The piece on the given square.
        """
        square = Square(square)
        return self._board[square.rank][square.file]

    def __delitem__(self, square: Square | str):
        """Remove the piece of a given square.

        Args:
            square: The rank and file of the square on which to remove a piece (if any).
        """
        square = Square(square)
        piece = self._board[square.rank][square.file]
        if piece is not None:
            piece.square = None
        self._board[square.rank][square.file] = None

    def __contains__(self, piece: Piece | None) -> bool:
        """Check if a piece is on the board.

        Args:
            piece: Basically type and color of piece to be checked.

        Returns:
            If piece is in board.
        """
        return any(piece in rank for rank in self._board)
