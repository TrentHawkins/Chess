"""Implements a chessboard.

Referencing with chess algebraic notation is possible.
"""

from itertools import cycle
from types import MethodType

from .piece import Orientation, Piece
from .pieces.meleed import King, Knight
from .pieces.ranged import Bishop, Queen, Rook
from .pieces.special import Castle, Pawn
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

    default_board_theme = {
        'white': 3,
        'black': 1,
    }

    def __init__(self, *, empty: bool = False, theme: dict[str, int] = default_board_theme):
        """Initialize a chessboard with a new game congifuration."""
        self._board: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]
        self.theme = theme  # Set board color theme.

    #   NOTE: Temporarily assign castles to board:
        self.castle = {}

        main_pieces = {
            "a": Rook,
            "b": Knight,
            "c": Bishop,
            "d": Queen,
            "e": King,
            "f": Bishop,
            "g": Knight,
            "h": Rook,
        }

        if not empty:
            for color in ['white', 'black']:
                pawn_rank = (Orientation[color] * 5 + 9) // 2  # Pawn rank per color.
                main_rank = (Orientation[color] * 7 + 9) // 2  # Main rank per color.

            #   All the pieces:
                for file, Main in main_pieces.items():
                    self[f"{file}{main_rank}"] = Main(color)  # The main pieces (rooks, knights, bishops, queen, king)
                    self[f"{file}{pawn_rank}"] = Pawn(color)  # The pawns.

            #   NOTE: Temporarily assign castles to board:
                self.castle[color] = {
                    "king-side": Castle(
                        self[f"e{main_rank}"],  # type: ignore
                        self[f"h{main_rank}"],  # type: ignore
                    ),
                    "queen-side": Castle(
                        self[f"e{main_rank}"],  # type: ignore
                        self[f"a{main_rank}"],  # type: ignore
                    ),
                }

    def __repr__(self) -> str:
        """Represent the board in proper direction and use the representation of each piece.

        Returns:
            The board representation.
        """
        white = 3
        black = 1

        square_color = cycle(
            [
                f"\033[0m\033[4{self.theme['white']}m",  # white
                f"\033[0m\033[4{self.theme['black']}m",  # black
            ]
        )
        edge_color = cycle(
            [
                f"\033[0m\033[3{self.theme['black']};4{self.theme['white']}m▐",
                f"\033[0m\033[3{self.theme['white']};4{self.theme['black']}m▐",
            ]
        )
        border_color = cycle(
            [
                f"\033[0m\033[3{self.theme['white']}m▐",
                f"\033[0m\033[3{self.theme['black']}m▌\033[0m\n",
                f"\033[0m\033[3{self.theme['black']}m▐",
                f"\033[0m\033[3{self.theme['white']}m▌\033[0m\n",
            ]
        )

        representation = "\n"

        for rank in self._board:
            representation += next(border_color)
            representation += (
                next(square_color) + str(rank[0]) + next(edge_color) +
                next(square_color) + str(rank[1]) + next(edge_color) +
                next(square_color) + str(rank[2]) + next(edge_color) +
                next(square_color) + str(rank[3]) + next(edge_color) +
                next(square_color) + str(rank[4]) + next(edge_color) +
                next(square_color) + str(rank[5]) + next(edge_color) +
                next(square_color) + str(rank[6]) + next(edge_color) +
                next(square_color) + str(rank[7])
            )
            representation += next(border_color)

            next(square_color)  # Flip colors for next rank to make a checkerboard.

        return representation.replace("None", "\033[8m🨅\033[0m")

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

    #   HACK: A square outside the boarfd may be requested.
        if square is not None:
            return self._board[square.rank][square.file]

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
        """Generate moves for all pieces on the board.

        Return:
            A dictionary containing all possible moves for each square player has a piece on.

        NOTE: Ideally the piece would be used as key but it is unhashable.
        """
        _moves = {}

        for piece in self:
            def deployable(source_piece: Piece, target: Square):
                Piece.deployable.__doc__
                target_piece = self[target]

                return Piece.deployable(source_piece, target) and target_piece is None

            def capturable(source_piece: Piece, target: Square):
                Piece.capturable.__doc__
                target_piece = self[target]

            #   If there is a piece on the target, check their allegiance.
                if target_piece is not None:
                    return Piece.capturable(source_piece, target) and source_piece.orientation != target_piece.orientation

                return False

            piece.deployable = MethodType(deployable, piece)
            piece.capturable = MethodType(capturable, piece)

            _moves[piece.square] = piece.moves

        return _moves

    def move(self, source: Square | str, target: Square | str):
        """Move whatever is in source square to target square if move is valid.

        Args:
            source: The square in notation the piece is on
            target: The square in notation the piece wants to go to.
        """
        source = Square(source)
        target = Square(target)

        if source is not None and source in self.moves:
            if target in self.moves[source]:
                piece = self[source]

                if piece is not None:
                    piece.has_moved = True

                self[source], self[target] = None, piece
