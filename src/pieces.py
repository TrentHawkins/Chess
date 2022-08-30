"""Implements the chess pieces that are placed in a chessboard.

Chess has 6 types of pieces with predifined rules of movement and worth in-game:
    Pawn: Moves one step forward, unless first move, where it may move two squares forward.
        Captures diagonally. Can en-pasant. Can be promoted to a higher value piece at the end of a player's board. Worth 1.
    Bishop: Moves along diagonals. Worth 3. WOrth 3+ when in pairs of two or in an open game.
    Knights: Moves 2 squares in one directions and 1 in a vertical to that direction).
        Can jump over other pieces. Worth 3. Worth 3+ in closed games.
    Rook: Moves along ranks and files. Worth 5.
    Queen: Moves both like a rook and bishop. Worth 9.
    King: Moves one square in any direction. Worth N/A (you loose the king it's game over).

Variable annotations:
    n: north
    w: west
    s: south
    e: east

Concatenation of aforementioned annotations means combination of directions (see self-documenting code).
Trailing '_' means indefinite.
"""

from dataclasses import dataclass
from enum import Enum
from itertools import product, cycle
from typing import Callable, ClassVar, Iterable

from .square import Vector, Square


class Color(Enum):
    """Annotate direction on the board with the corresponding color."""

    white = -1
    black = +1


@dataclass
class Piece:
    """A generic chess piece.

    Attributes:
        color: One of two colors, black or white.
        targets: Squares that a piece has a target. (NOTE: EXPERIMENTAL)
    """

#   Straight steps:
    rizontals: ClassVar[set[Vector]] = set((
        Vector(-1, 0),
        Vector(0, -1),
    ))
    verticals: ClassVar[set[Vector]] = set((
        Vector(+1, 0),
        Vector(0, +1),
    ))
    straights: ClassVar[set[Vector]] = rizontals.union(verticals)

#   Diagonal steps:
    diagonals: ClassVar[set[Vector]] = set((rizontal + vertical for rizontal, vertical in product(
        rizontals,
        verticals,
    )))

    steps: ClassVar[set[Vector]] = set()  # a set to be filled by various subclasses

    color: Color

    @property
    def is_black(self):
        """Binary switch for color, since it is either black or white.

        Returns:
            Whether piece is black or not.
        """
        return self.color == Color.black

    def __repr__(self) -> str:
        f"""Represent a {self.__class__.__name__}.

        Returns:
            The representation of a {self.__class__.__name__}.
        """
        return " "  # An unspecified piece is a ghost piece.

#   NOTE: Remember that target resolution is still unresolved.
    def legal_moves(self, square: Square, condition: Callable[[Square], bool]) -> set[Square]:
        f"""Generate all legal moves a {self.__class__.__name__} can apriori make.

        Args:
            square: Square on which piece is placed.
                Default is no square, in which case displacements are not resolved into squares and generators not unfold.

        Returns:
            A list of all possible moves.
        """
        return set()  # A ghost piece cannot move.


class Pawn(Piece):
    """A pawn."""

    value: int = 1

    def __repr__(self) -> str:
        self.__repr__.__doc__
        return "♟" if self.is_black else "♙"

#   NOTE TO SELF: LOTS OF TEARS


@dataclass
class Meleer(Piece):
    """ A close ranged piece liek a knight or bishop."""

    def legal_moves(self, square: Square, condition: Callable[[Square], bool]) -> set[Square]:
        super().legal_moves.__doc__
        squares = set()
        for move in self.steps:
            if condition(square):
                squares.add(square + move)
        return squares  # If empty, its game over.


@dataclass
class King(Meleer):
    """A king."""

    steps = Meleer.steps.union(Piece.straights.union(Piece.diagonals))

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♚" if self.is_black else "♔"


@dataclass
class Knight(Meleer):
    """A knight."""

#   Knight moves
    steps = Meleer.steps.union(diagonal + straight for diagonal, straight in product(Piece.diagonals, Piece.straights))
    steps = steps.difference(Piece.rizontals.union(Piece.straights))  # remove the non-knight moves

    value: int = 3

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♞" if self.is_black else "♘"


@dataclass
class Ranger(Piece):
    """A Rook, Bishop or Queen. (I mean... in `python` you only say things once, right?)"""

    def legal_moves(self, square: Square, condition: Callable[[Square], bool]) -> set[Square]:
        super().legal_moves.__doc__
        squares = set()
        for move in self.steps:  # For each direction.
            advanced_square = square + move  # Start looking at advanced squares
            while condition(advanced_square):  # While we don't hit something.
                squares.add(square)  # Add the damn square to legal destination squares.
                advanced_square += move  # Advance to the next square in line.
        return squares


@dataclass
class Rook(Ranger):
    """A rook."""

#   Straight lines:
    steps = Ranger.steps.union(Piece.straights)

    value: int = 5

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♜" if self.is_black else "♖"


@dataclass
class Bishop(Ranger):
    """A bishop."""

#   Diagonal lines:
    steps = Ranger.steps.union(Piece.diagonals)

    value: int = 3

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♝" if self.is_black else "♗"


@dataclass
class Queen(Rook, Bishop):
    """A queen."""

    value: int = 9

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♛" if self.is_black else "♕"
