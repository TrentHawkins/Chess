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
        color: One of two colors, black or white. Holds direction of the board.
        value: How much a piece is worth:
            1: Pawn
            3: Knight/Bishop
            5: Rook
            9: Queen
            ∞: King

    A few generic rules applied to all pieces:
        Pinning: If moving a piece will discover a check on your king, the piece is pinned and cannot move.
        If your king is checked, no other piece can move except for the ones and with only the moves that resolve the check.
    """

    north: ClassVar[Vector] = Vector(-1, 0)
    south: ClassVar[Vector] = Vector(+1, 0)

    west: ClassVar[Vector] = Vector(0, -1)
    east: ClassVar[Vector] = Vector(0, +1)

#   Straight steps:
    rizontals: ClassVar[set[Vector]] = set((
        west,
        east,
    ))
    verticals: ClassVar[set[Vector]] = set((
        north,
        south,
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
    """A pawn.

    Moves forward a square, unless its first move where it can move two and unless blocked by any piece.
    It captured forward-diagonally. I can capture en-passant:
        If an enemy pawn passes yours trying to escape capture, well... it cannot, not for this round.
    NOTE: That probably means that board will invoke this method multiple times (unti a better way is thought).
    Upon reaching the end of the board, it is promoted to an officer:
        - Rook
        - Bishop
        - Knight
        - Queen
    """

    pawn_step = Piece.south

    steps = Piece.steps.union({
        pawn_step,  # One step.
        pawn_step + Piece.west,  # Capturing to the left.
        pawn_step + Piece.east,  # Capturing to the right.
    })

    value: int = 1

#   Extra flags for the pawn:
    has_moved: bool = False

    def __repr__(self) -> str:
        self.__repr__.__doc__
        return "♟" if self.is_black else "♙"

#   NOTE: Probably a board will invoke this method multiple times (until a better way is thought).
    def legal_moves(self, square: Square, condition: Callable[[Square], bool]) -> set[Square]:
        super().legal_moves.__doc__
        squares = set()
        for move in self.steps:
            if condition(square + move * self.color.value):
                squares.add(square + move * self.color.value)
        if not self.has_moved:
            squares.add(square + (self.pawn_step + self.pawn_step) * self.color.value)
        return squares


@dataclass
class Melee(Piece):
    """A close ranged piece:
        - King
        - Knight (has reach)

    Pawns are special.
    """

    def legal_moves(self, square: Square, condition: Callable[[Square], bool]) -> set[Square]:
        super().legal_moves.__doc__
        squares = set()
        for move in self.steps:
            if condition(square + move):
                squares.add(square + move)
        return squares


@dataclass
class King(Melee):
    """A King.

    Moves one square in any direction that is not blocked by same side piece or targeted by enemy piece.
    """

    steps = Melee.steps.union(Piece.straights.union(Piece.diagonals))

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♚" if self.is_black else "♔"


@dataclass
class Knight(Melee):
    """A knight.

    Moves two squares in any direction and one square in a vertical to that direction as one move.
    It therefore can jump over other pieces. Target square must not be blocked by a same side piece.
    """

#   Knight moves
    steps = Melee.steps.union(diagonal + straight for diagonal, straight in product(Piece.diagonals, Piece.straights))
    steps = steps.difference(Piece.rizontals.union(Piece.straights))  # remove the non-knight moves

    value: int = 3

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♞" if self.is_black else "♘"


@dataclass
class Range(Piece):
    """A long range piece:
        - Rook
        - Bishop
        - Queen
    """

    def legal_moves(self, square: Square, condition: Callable[[Square], bool]) -> set[Square]:
        super().legal_moves.__doc__
        squares = set()
        for move in self.steps:  # For each direction.
            advanced_square = square + move  # Start looking at advanced squares
            while condition(advanced_square):  # While we don't hit something.
                squares.add(advanced_square)  # Add the damn square to legal destination squares.
                advanced_square += move  # Advance to the next square in line.
        return squares


@dataclass
class Rook(Range):
    """A rook.

    Moves anywhere along its rank xor its file, unless blocked by enemy (which captures) or same piece.
    """

#   Straight lines:
    steps = Range.steps.union(Piece.straights)

    value: int = 5

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♜" if self.is_black else "♖"


@dataclass
class Bishop(Range):
    """A bishop.

    Moves anywhere along a diagonal, unless blocked by enemy (which captures) or same piece.
    This means that a bishop never leaves the color of the square it is on.
    A player starts with two bishops:
        A black-square bishop.
        A white-square bishop.
    So both cover the squares of the whole board, and it is the reason the worth more when both on the board.
    """

#   Diagonal lines:
    steps = Range.steps.union(Piece.diagonals)

    value: int = 3

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♝" if self.is_black else "♗"


@dataclass
class Queen(Range, King):
    """A queen.

    Moves both like a rook and bishop, unless blocked by enemy (which captures) or same piece.
    Can access all squares.

    Inherits the steps of a King but the Range of a ranger. :)
    """

    value: int = 9

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return "♛" if self.is_black else "♕"
