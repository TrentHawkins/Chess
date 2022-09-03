"""Implements a chessboard.

Referencing with chess algebraic notation is possible.
"""

import enum
from functools import singledispatchmethod
from typing import Callable

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
        self["a1"] = Rook(Color.white)
        self["b1"] = Knight(Color.white)
        self["c1"] = Bishop(Color.white)
        self["d1"] = Queen(Color.white)
        self["e1"] = King(Color.white)
        self["f1"] = Bishop(Color.white)
        self["g1"] = Knight(Color.white)
        self["h1"] = Rook(Color.white)

    #   White pawns on the second rank.
        self["a2"] = Pawn(Color.white)
        self["b2"] = Pawn(Color.white)
        self["c2"] = Pawn(Color.white)
        self["d2"] = Pawn(Color.white)
        self["e2"] = Pawn(Color.white)
        self["f2"] = Pawn(Color.white)
        self["g2"] = Pawn(Color.white)
        self["h2"] = Pawn(Color.white)

    #   Black pawns on the seventh rank.
        self["a8"] = Rook(Color.black)
        self["b8"] = Knight(Color.black)
        self["c8"] = Bishop(Color.black)
        self["d8"] = Queen(Color.black)
        self["e8"] = King(Color.black)
        self["f8"] = Bishop(Color.black)
        self["g8"] = Knight(Color.black)
        self["h8"] = Rook(Color.black)

    #   Black pieces on the eighth rank.
        self["a7"] = Pawn(Color.black)
        self["b7"] = Pawn(Color.black)
        self["c7"] = Pawn(Color.black)
        self["d7"] = Pawn(Color.black)
        self["e7"] = Pawn(Color.black)
        self["f7"] = Pawn(Color.black)
        self["g7"] = Pawn(Color.black)
        self["h7"] = Pawn(Color.black)

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
                f"▐\033[24m\033[7m{Square.index_to_rank[index]}\033[0m▌"
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
            square = Square(square)
            self._board[square.rank][square.file] = piece

    def __getitem__(self, square: Square | str | None) -> Piece | None:
        """Get the piece of a given square.

        Args:
            square: The rank and file of the square.

        Returns:
            The piece on the given square.
        """
        if square:
            square = Square(square)
            if square.rank < 0 or square.file < 0:
                raise ValueError("Squares have only positive rank and file.")
            if square.rank > 7 or square.file > 7:
                raise ValueError("Squares must be inside the board.")
            return self._board[square.rank][square.file]

    def __delitem__(self, square: Square | str | None):
        """Remove the piece of a given square.

        Args:
            square: The rank and file of the square on which to remove a piece (if any).
        """
        if square:
            square = Square(square)
            self._board[square.rank][square.file] = None

    def __contains__(self, piece: Piece | None) -> bool:
        """Check if a piece is on the board.

        Args:
            piece: Basically type and color of piece to be checked.

        Returns:
            If piece is in board.
        """
        return any(piece in rank for rank in self._board)

    def __eq__(self, other: "Board") -> bool:
        return self._board == other._board

    def square_of(self, piece: Piece | None) -> Square | None:
        """Return the square of a specific piece.

        Args:
            piece: Piece object to fetch the square of.

        Returns:
            The square of the piece in chess notation or indices or None if it is not on the board.
        """
        for rank, board_rank in enumerate(self._board):
            for file, board_square in enumerate(board_rank):
                if board_square is piece:
                    return Square(Vector(rank, file))  # HACK: I do not like that I have to chain constructors like this.

    def square_of_king(self, color: Color) -> King:
        for rank, board_rank in enumerate(self._board):
            for file, board_square in enumerate(board_rank):
                if isinstance(board_square, King) and board_square.color == color:
                    return Square(Vector(rank, file))

    def all_enemy_pieces(self, color: Color) -> list[Piece]:
        pieces: list[Piece] = []
        for rank, board_rank in enumerate(self._board):
            for file, board_square in enumerate(board_rank):
                if board_square is not None and board_square.color == color:
                    square = Square(Vector(rank, file))
                    pieces.append(square)
        return pieces


    @singledispatchmethod
    def _make_condition(self, piece: Piece, square: Square) -> Callable[[Square], tuple[bool, Piece]]:
        """Create a condition function. The conditions take care of the following cases:
        - if the piece moves outside of the board, it discards the move
        - if the piece is of the same color, it discards the move

        It also returns the piece that may exist there to check if it can be captured.
        This happens at the calling function. 

        Args:
            piece: the piece that moves

        Returns:
            whether the move is blocked and any piece that was captured.
        """
        def condition(target_square: Square) -> tuple[bool, Piece]:
            other_piece = None
            try:
                other_piece = self[target_square]
            except ValueError:
                return False, None
            return other_piece is None or piece.color != other_piece.color, other_piece

        return condition
        
    @_make_condition.register
    def _(self, piece: Pawn, square: Square) -> Callable[[Square], tuple[bool, Piece]]:
        """Create a condition function. The conditions take care of the following cases:
        - if the piece moves outside of the board, it discards the move
        - if the piece is of the same color, it discards the move

        It also returns the piece that may exist there to check if it can be captured.
        This happens at the calling function. 

        Args:
            piece: the piece that moves

        Returns:
            whether the move is blocked and any piece that was captured.
        """
        def condition(target_square: Square) -> tuple[bool, Piece]:
            other_piece = None
            move = target_square - square
            try:
                other_piece = self[target_square]
            except ValueError:
                return False, None
            if abs(move.rank) == 2 and square.rank != 6 and not piece.is_black:
                return False, None
            elif abs(move.rank) == 2 and square.rank != 1 and piece.is_black:
                return False, None
            return (other_piece is None or piece.color != other_piece.color), other_piece

        return condition

    @_make_condition.register
    def _(self, piece: King, square: Square) -> Callable[[Square], tuple[bool, Piece]]:
        """Create a condition function. The conditions take care of the following cases:
        - if the piece moves outside of the board, it discards the move
        - if the piece is of the same color, it discards the move

        It also returns the piece that may exist there to check if it can be captured.
        This happens at the calling function. 

        Args:
            piece: the piece that moves

        Returns:
            whether the move is blocked and any piece that was captured.
        """
        def condition(target_square: Square) -> tuple[bool, Piece]:
            other_piece = None
            try:
                other_piece = self[target_square]
            except ValueError:
                return False, None
            # should check if neighboring pieces threaten adjacent squares.
            return other_piece is None or piece.color != other_piece.color, other_piece

        return condition

    def list_moves(self, selected_square: Square) -> set[Square]:
        """Provides context to determine legal moves of a chess piece using the condition function.
        
        Args:
            selected_square: the square selected by the user, which contains a piece to move.
        
        Returns:
            all the legal moves of the selected piece.
        """
        piece = self[selected_square]
        condition = self._make_condition(piece, selected_square)
        moves = set()
        for target_square in piece.legal_moves(selected_square, condition):
            moves.add(target_square)

        return moves
