"""Implements the chess pieces that are placed in a chessboard.

Of the 6 type of chess pieces the following are units with range:
    Bishop: Moves along diagonals. Worth 3. WOrth 3+ when in pairs of two or in an open game.
    Rook: Moves along ranks and files. Worth 5.
    Queen: Moves both like a rook and bishop. Worth 9.
"""

from dataclasses import dataclass
from typing import ClassVar

from ..piece import Piece
from ..square import Square, Vector


@dataclass(init=False, repr=False)
class Ranged(Piece):
    """A long range piece:
        - Rook
        - Bishop
        - Queen

    Testing.
    """

    @property
    def moves(self) -> set[Square]:
        f"""{super().moves.__doc__}"""
        squares = super().moves

        if self.square is not None:  # If ranged piece is on a board,
            for step in self.steps:  # For all legal directions,
                square = self.square + step  # Get next square in direction,

                while self.deployable(square):  # If said square is inside board limits,
                    squares.add(square)  # Add said square to ranged piece.
                    square += step  # Advance to the next square in said direction.

                if self.capturable(square):  # NOTE: This check will become relevant as soon as condition is defined too.
                    squares.add(square)  # Do not forget to add trailing square to targets.

        return squares


@dataclass(init=False, repr=False)
class Rook(Ranged):
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

    has_moved: bool = False  # For castling.

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": "♖",
            "black": "♜",
        }[self.orientation.name]


@dataclass(init=False, repr=False)
class Bishop(Ranged):
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
            "white": "♗",
            "black": "♝",
        }[self.orientation.name]


@dataclass(init=False, repr=False)
class Queen(Ranged):
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
            "white": "♕",
            "black": "♛",
        }[self.orientation.name]
