"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from dataclasses import dataclass
from types import MethodType

from .board import Board
from .piece import Orientation, Piece
from .pieces.meleed import King
from .square import Square


@dataclass(init=False, repr=False)
class Player:
    """A player.

    Attributes:
        name: The player's name.
        board: The board this player is playing on.
        orientation: The allegiance of the player, defining the correspponding orientation of the board.
        pieces: A collection of the player's pieces on the board.
        captured: A collection of captured pieces hashed by piece type.
            NOTE: All captured pieces are expected to have `square == None` making them distinct only by type.
    """

    def __init__(self, name: str, color: str, board: Board):
        """Create collections for player.

        Args:
            name: The player's name.
            color: The color of the player's pieces.
            board: The board this player is playing on.
        """
        self.name: str = name
        self.orientation: Orientation = Orientation[color]  # The allegiance of the player.
        self.board: Board = board  # The board this player is playing on.

    #   Assign pieces to player agnostically, so that custom position can also be loaded.
        self.pieces: set[Piece] = set(piece for piece in self.board if piece.orientation == self.orientation)
        self.captured: Counter = Counter()  # In custom positions, captured material is immaterial.

        def deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

        #   NOTE: Applying method directly to `source_piece` causes infinite recursion.
        #   A more explicit resolution is required.
        #   However, since method is updated for all pieces on the board,
        #   and since each one of them is a strict `Piece` subclass,
        #   we need the actual class name to resolve the redefinition.

            return source_piece.__class__.deployable(source_piece, target) \
                and target_piece is None

        def capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

        #   NOTE: Applying method directly to `source_piece` causes infinite recursion.
        #   A more explicit resolution is required.
        #   However, since method is updated for all pieces on the board,
        #   and since each one of them is a strict `Piece` subclass,
        #   we need the actual class name to resolve the redefinition.

        #   If there is a piece on the target, check their allegiance.
            if target_piece is not None:
                return source_piece.__class__.capturable(source_piece, target) \
                    and source_piece.orientation != target_piece.orientation

            return False

    #   Register the updated rules at player initialization to make sure it "takes".
        for piece in self.pieces:
            piece.deployable = MethodType(deployable, piece)  # Update deployability context for specific piece.
            piece.capturable = MethodType(capturable, piece)  # Update capturability context for specific piece.

        #   Keep the player's king registered, as it is a special piece.
            if isinstance(piece, King):
                self.king: King = piece

    def __repr__(self):
        """Represent a player by name and captured pieces.

        NOTE: Timer is not implemented yet.

        Returns:
            Players name followed by a color window and captured pieces
        """
        ...

    @property
    def checks(self) -> set[Square]:
        """Get all squares checked by player.

        Returns:
            A flattened union of all squares the player has access to.
        """
        return set().union(*(piece.moves for piece in self.pieces))

    def move(self, piece: Piece, target: Square | str):
        """Move whatever is in source square to target square if move is valid.

        Args:
            source: The square in notation the piece is on
            target: The square in notation the piece wants to go to.
        """
        target = Square(target)

        source = piece.square

        if source is not None:
            if target in piece.moves:
                self.board[source], self.board[target] = None, piece

                piece.has_moved = True
