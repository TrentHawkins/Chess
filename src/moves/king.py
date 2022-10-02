"""Implements castling and check(mat)ing.

This implementation attempts at abstracting the castling logic to its fundamental rules:
1.  The king must not have moved.
    This is cleared here with the king's `has_moved` flag.
2.  The corresponding rook to castle must not have moved.
    This is cleared here with the rook's `has_moved` flag.
3.  The king must not be in check.
    This is can be written here via king's `deployable` method which is context-defined before each round on `chess` level.
4.  The squares the king skips with castling must not be threatened.
    This is can be written here via king's `deployable` method which is context-defined before each round on `chess` level.
    The king's `capturable` method is not needed, as the king can never capture a piece in the process of castling.
5.  There must not be any obstructing pieces (of any color) between the king and the rook.
    This requires a context at `board` level redefintion of the `deployable` function.

The king checking and checkmating are only wrapped here, evaluation is delayed till game context is available.
"""

from dataclasses import dataclass
from re import Pattern, compile
from typing import ClassVar

from ..move import Move
from ..piece import Piece
from ..pieces.melee import King
from ..pieces.ranged import Rook
from ..square import Square, Vector


@dataclass(repr=False)
class Castle(Move):
    """A king skip to castling.

    For each game, two such pairs are created per player, a king-side and a queen-side castle.
    This class attempts at abstracting the castling logic to its fundamental rules:
    1.  The king must not have moved.
        This is cleared here with the king's `has_moved` flag.
    2.  The corresponding rook to castle must not have moved.
        This is cleared here with the rook's `has_moved` flag.
    3.  The king must not be in check.
        This is can be written here via king's `deployable` method which is context-defined before each round on `chess` level.
    4.  The squares the king skips with castling must not be threatened.
        This is can be written here via king's `deployable` method which is context-defined before each round on `chess` level.
        The king's `capturable` method is not needed, as the king can never capture a piece in the process of castling.
    5.  There must not be any obstructing pieces (of any color) between the king and the rook.
        This requires a context at `board` level redefintion of the `deployable` function.

    Castling is indicated by the special notations 0-0 (for kingside castling) and 0-0-0 (queenside castling).
    While the FIDE standard [6] is to use the digit zero (0-0 and 0-0-0), PGN uses the uppercase letter O (O-O and O-O-O).

    Attributes:
        piece: The king that castles.
    """

#   Ask for any ot the piece letters to appear once or nonce (for pawns).
    move_range: ClassVar[str] = "O-O|O-O-O"
    notation: ClassVar[Pattern] = compile(move_range)

    piece: King  # reference to a king piece

    def __post_init__(self):
        """Set up the castling relevant squares."""
        self.step = self.square - self.piece.square

        self.castle = self.piece.square + self.piece.castles[self.step]  # type: ignore
        self.middle = self.piece.square + self.step // 2  # type: ignore

    def __repr__(self):
        """Notation for castle moves."""
        return {
            Vector(0, +2): "O-O",
            Vector(0, -2): "O-O-O",
        }[self.step]

    @classmethod
    def read(cls, move: str, king: King):
        f"""{super(Castle, cls).read.__doc__}"""
        read = cls.notation.match(move)

        if read:
            if read.string == "O-O":
                return cls(king, king.square + king.short)  # type: ignore

            if read.string == "O-O-O":
                return cls(king, king.square + king.other)  # type: ignore

    def is_legal(self) -> bool:
        """Check if castling with the two pieces is still possible.

        Returns:
            Whether castling with the two pieces is still possible.
        """
        return self.piece.castleable(self.square)


@dataclass(repr=False)
class Check(Move):
    """A move that checks the opposing king.

    This particular king of move will require context from the game, so evaluation is delayed.
    """
    ...


@dataclass(repr=False)
class Checkmate(Check):
    """A move that checks the opposing king.

    This particular king of move will require context from the game, so evaluation is delayed.
    """
    ...
