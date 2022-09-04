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
from enum import IntEnum
from itertools import combinations, product
from typing import ClassVar, Optional

from .square import Square, Vector


class Color(IntEnum):
    """Annotate direction on the board with the corresponding color."""

    white = -1
    black = +1


@dataclass(init=False, repr=False)
class Piece:
    """A generic chess piece.

    Class Attributes:
        value: How much a piece is worth:
            1: Pawn
            3: Knight/Bishop
            5: Rook
            9: Queen
            ∞: King
        steps: Default move patterns characteristic for each piece.

    Attributes:
        color: One of two colors, black or white. Holds direction of the board.
        square: Where on (any) board is it (as far as rules go).

    A few generic rules applied to all pieces:
        Pinning: If moving a piece will discover a check on your king, the piece is pinned and cannot move.
        If your king is checked, no other piece can move except for the ones and with only the moves that resolve the check.

    Straight steps:
        ↑ north
        ← west
        ↓ south
        → east

    Diagonal steps (via combinations of straight steps):
        → + ← = · center (removed)
        → + ↑ = ↗ north-east
        → + ↓ = ↘ south-east
        ← + ↑ = ↖ north-west
        ← + ↓ = ↙ south-west
        ↑ + ↓ = · center (removed)
    """

    center: ClassVar[Vector] = Vector(0, 0)  # · no movement

    north: ClassVar[Vector] = Vector(-1, 0)  # ↑ up
    south: ClassVar[Vector] = Vector(+1, 0)  # ↓ down

    west: ClassVar[Vector] = Vector(0, -1)  # ← left
    east: ClassVar[Vector] = Vector(0, +1)  # → right

#   Straight steps:
    straights: ClassVar[set[Vector]] = {
        north, west,
        south, east,
    }

#   Diagonal steps:
    diagonals: ClassVar[set[Vector]] = \
        {straight0 + straight1 for straight0, straight1 in combinations(straights, 2)} - {center}

    steps: ClassVar[set[Vector]] = set()

    def __init__(self, color: str, square: Optional[Square] = None):
        f"""Give a {self.__class__.__name__} a color and a square.

        Args:
            square: Location on a board (which board is irrelevant).
        """
        self.color = Color[color]
        self.square = square

    def __repr__(self) -> str:
        f"""Represent a {self.__class__.__name__}.

        Returns:
            The representation of a {self.__class__.__name__}.
        """
        return " "  # An unspecified piece is a ghost piece.

    def has_friend(self, other):
        """Check weather `target` is a foe of `source`.

        NOTE: this can be done with `Piece` objects instead of `Square` ones.

        Args:
            source: The source piece.
            source: The target piece to check allegiance of.

        Returns:
            True if `target` square has a foe of whatever is on `source` square.
        """
        if self and other:
            return self.color == other.color
        return False

    def has_foe(self, other):
        """Check weather `target` is a friend of `source`.

        NOTE: this can be done with `Piece` objects instead of `Square` ones.

        Args:
            source: The source piece.
            source: The target piece to check allegiance of.

        Returns:
            True if `target` square has a foe of whatever is on `source` square.
        """
        if self and other:
            return self.color != other.color
        return False

    def condition(self, target: Square) -> bool:
        """Special conditions pertaining the particular piece type and source square.

        This method is to be lazily-defined in board, access to current piece data makes it appropriate to sign it in here.

        Args:
            target: The source square is `self.square`.

        Returns:
            Whether the specific condition are met.
        """
        return self.square is not None  # The most basic condition if for a piece to be on a legal square.

    def legal_moves(self) -> set[Square]:
        f"""Generate all legal moves a {self.__class__.__name__} can apriori make.

        Args:
            square: Square on which piece is placed.
                Default is no square, in which case displacements are not resolved into squares and generators not unfold.
            condition: A condition that depends on a square, usually a target square.

        Returns:
            A list of all possible moves.
        """
        return set()  # A ghost piece cannot move.


@dataclass(init=False, repr=False)
class Pawn(Piece):
    """A Pawn.

    Moves forward a square, unless its first move where it can move two and unless blocked by any piece.
    It captured forward-diagonally. I can capture en-passant:
        If an enemy pawn passes yours trying to escape capture, well... it cannot, not for this round.
    NOTE: That probably means that board will invoke this method multiple times (unti a better way is thought).
    Upon reaching the end of the board, it is promoted to an officer:
        - Rook
        - Bishop
        - Knight
        - Queen

    Pawn steps:
        black:
            ↓ one step
            ↓ + ↓ two step
            ↓ + ← = ↙ capture west
            ↓ + → = ↘ capture east
        white:
            ↑ one step
            ↑ + ↑ two step
            ↑ + ← = ↖ capture west
            ↑ + → = ↗ capture east
    """

#   Pawn value:
    value: ClassVar[int] = 1

#   Pawn moves:
    steps: ClassVar[set[Vector]] = {
        Piece.south,  # One step.
        Piece.south + Piece.south,  # Two step.
        Piece.south + Piece.west,  # Capturing to the west.
        Piece.south + Piece.east,  # Capturing to the east.
    }

    def __repr__(self) -> str:
        self.__repr__.__doc__
        return {
            Color.white: "♙",
            Color.black: "♟",
        }[self.color]

    def legal_moves(self) -> set[Square]:
        super().legal_moves.__doc__
        squares = set()
        for step in self.steps:
            if self.square is not None:
                square_step = self.square + step * self.color
                if square_step is not None and self.condition(square_step):
                    squares.add(square_step)
        return squares


@dataclass(init=False, repr=False)
class Melee(Piece):
    """A close ranged piece:
        - King
        - Knight (has reach)

    Pawns are special.
    """

    def legal_moves(self) -> set[Square]:
        super().legal_moves.__doc__
        squares = set()
        for step in self.steps:  # For each direction.
            if self.square is not None:
                square_step = self.square + step  # Start looking at advanced squares
                if square_step is not None and self.condition(square_step):  # If we don't hit something.
                    squares.add(square_step)  # Add the damn square to legal destination squares.
        return squares


@dataclass(init=False, repr=False)
class King(Melee):
    """A King.

    Moves one square in any direction that is not blocked by same side piece or targeted by enemy piece.

    King steps:
        ↑ north
        ← west
        ↓ south
        → east
        ↗ north-east
        ↘ south-east
        ↖ north-west
        ↙ south-west
    """

#   King moves:
    steps: ClassVar[set[Vector]] = Piece.straights | Piece.diagonals

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            Color.white: "♔",
            Color.black: "♚",
        }[self.color]


@dataclass(init=False, repr=False)
class Knight(Melee):
    """A knight.

    Moves two squares in any direction and one square in a vertical to that direction as one move.
    It therefore can jump over other pieces. Target square must not be blocked by a same side piece.

    Knight steps (via product of diagonal steps with straigh steps:
        ↗ + ↑ north-north-east
        ↗ + ← = ↑ north (removed)
        ↗ + ↓ = → east (removed)
        ↗ + → north-east-east
        ↘ + ↑ = → east (removed)
        ↘ + ← = ↓ south (removed)
        ↘ + ↓ south-south-east
        ↘ + → south-east-east
        ↖ + ↑ north-north-west
        ↖ + ← north-west-west
        ↖ + ↓ = ← west (removed)
        ↖ + → = ↑ north (removed)
        ↙ + ↑ = ← west (removed)
        ↙ + ← south-west-west
        ↙ + ↓ south-south-west
        ↙ + → = ↓ south (removed)
    """

#   Knight value:
    value: ClassVar[int] = 3

#   Knight moves:
    steps: ClassVar[set[Vector]] = \
        {diagonal + straight for diagonal, straight in product(Piece.diagonals, Piece.straights)} - Piece.straights

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            Color.white: "♘",
            Color.black: "♞",
        }[self.color]


@dataclass(init=False, repr=False)
class Range(Piece):
    """A long range piece:
        - Rook
        - Bishop
        - Queen
    """

    def legal_moves(self) -> set[Square]:
        super().legal_moves.__doc__
        squares = set()
        for step in self.steps:  # For each direction.
            if self.square is not None:
                square_step = self.square + step  # Start looking at advanced squares
                while square_step is not None and self.condition(square_step):  # While we don't hit something.
                    squares.add(square_step)  # Add the damn square to legal destination squares.
                    square_step += step  # Advance to the next square in line.
        return squares


@dataclass(init=False, repr=False)
class Rook(Range):
    """A rook.

    Moves anywhere along its rank xor its file, unless blocked by enemy (which captures) or same piece.

    Rook steps:
        ↑ north
        ← west
        ↓ south
        → east
    """

#   Knight value:
    value: ClassVar[int] = 5

#   Straight lines:
    steps: ClassVar[set[Vector]] = Piece.straights

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            Color.white: "♖",
            Color.black: "♜",
        }[self.color]


@dataclass(init=False, repr=False)
class Bishop(Range):
    """A bishop.

    Moves anywhere along a diagonal, unless blocked by enemy (which captures) or same piece.
    This means that a bishop never leaves the color of the square it is on.
    A player starts with two bishops:
        A black-square bishop.
        A white-square bishop.
    So both cover the squares of the whole board, and it is the reason the worth more when both on the board.

    Bishop steps:
        ↗ north-east
        ↘ south-east
        ↖ north-west
        ↙ south-west
    """

#   Knight value:
    value: ClassVar[int] = 3

#   Diagonal lines:
    steps: ClassVar[set[Vector]] = Piece.diagonals

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            Color.white: "♗",
            Color.black: "♝",
        }[self.color]


@dataclass(init=False, repr=False)
class Queen(Range):
    """A queen.

    Moves both like a rook and bishop, unless blocked by enemy (which captures) or same piece.
    Can access all squares.

    Inherits the steps of a King but the movement of Range.

    Queen steps:
        ↑ north
        ← west
        ↓ south
        → east
        ↗ north-east
        ↘ south-east
        ↖ north-west
        ↙ south-west
    """

#   Knight value:
    value: ClassVar[int] = 9

#   Queen lines:
    steps: ClassVar[set[Vector]] = Piece.straights | Piece.diagonals

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            Color.white: "♕",
            Color.black: "♛",
        }[self.color]
