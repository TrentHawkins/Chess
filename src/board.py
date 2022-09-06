"""Implements a chessboard.

Referencing with chess algebraic notation is possible.
"""

from types import MethodType

from .piece import Orientation, Piece
from .pieces.meleed import King, Knight
from .pieces.ranged import Bishop, Queen, Rook
from .pieces.special import Pawn
from .square import Square


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

    def __init__(self, empty: bool = False):
        """Initialize a chessboard with a new game congifuration."""
        self._board: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]

        if not empty:
            for color in ["white", "black"]:
                pawn_rank = (Orientation[color] * 5 + 9) // 2  # Pawn rank per color.
                main_rank = (Orientation[color] * 7 + 9) // 2  # Main rank per color.

            #   The pawns:
                for file in Square.file_range:
                    self[f"{file}{pawn_rank}"] = Pawn(color)

            #   The rest of the pieces:
                self[f"a{main_rank}"] = Rook(color)
                self[f"b{main_rank}"] = Knight(color)
                self[f"c{main_rank}"] = Bishop(color)
                self[f"d{main_rank}"] = Queen(color)
                self[f"e{main_rank}"] = King(color)
                self[f"f{main_rank}"] = Bishop(color)
                self[f"g{main_rank}"] = Knight(color)
                self[f"h{main_rank}"] = Rook(color)

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

    #   If there is another piece on the square, safely remove it from the board first.
        if self[square] is not None:
            del self[square]

    #   If a true piece is assigned, proceed as planned, otherwise leave the square empty.
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

    #   If requesting the content of a true square return a piece or `None`.
        if square is not None:
            return self._board[square.rank][square.file]

        return None

    def __delitem__(self, square: Square | str):
        """Remove the piece of a given square.

        Args:
            square: The rank and file of the square on which to remove a piece (if any).
        """
        square = Square(square)
        piece = self[square]

    #   If there truly is a piece on that square, and referenced elsewhere, best do the book-keeping of taking it off-board.
        if piece is not None:
            piece.square = None

            self._board[square.rank][square.file] = None

    def __iter__(self):
        """Iterate through existent pieces on the board."""
        for rank in self._board:
            for piece in rank:
                if piece is not None:
                    yield piece

    def __contains__(self, piece: Piece | None) -> bool:
        """Check if a piece is on the board.

        Args:
            piece: Basically type and color of piece to be checked.

        Returns:
            If piece is in board.
        """
        return any(piece in rank for rank in self._board)

    @property
    def moves(self):
        """Generate moves for all pieces on the board."""
        _moves = {}

        for piece in self:
            def deployable(source_piece: Piece, target: Square):
                Piece.deployable.__doc__
                target_piece = self[target]

                return Piece.deployable(source_piece, target) and target_piece is None

            def capturable(source_piece: Piece, target: Square):
                Piece.capturable.__doc__
                target_piece = self[target]

                if target_piece is not None:
                    return Piece.capturable(source_piece, target) and source_piece.orientation != target_piece.orientation

                return False

            piece.deployable = MethodType(deployable, piece)
            piece.capturable = MethodType(capturable, piece)

            _moves[piece.square] = piece.moves

        return _moves

    def move(self, source_piece: Piece | None, target: Square | str):
        """Move whatever is in source square to target square if move is valid.

        Args:
            source: The square in notation the piece is on
            target: The square in notation the piece wants to go to.
        """
        if source_piece is not None:
            source = source_piece.square

        else:
            source = None

        target = Square(target)

        if source is not None and source in self.moves:
            if target in self.moves[source]:
                self[source], self[target] = None, source_piece
