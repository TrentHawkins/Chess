"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from dataclasses import dataclass
from types import MethodType

from .board import Board
from .piece import Orientation, Piece
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
        self.pieces = set(piece for piece in self.board if piece.orientation == self.orientation)
        self.captured = Counter()  # In custom positions, captured material is immaterial.

    def __repr__(self):
        """Represent a player by name and captured pieces.

        NOTE: Timer is not implemented yet.

        Returns:
            Players name followed by a color window and captured pieces
        """
        ...

    @property
    def checked(self) -> set[Square]:
        """Get all squares checked by player.

        As a bonus define the `Square.is_checked` flag based on the result.
        """
        return set().union(*self.moves.values())

    @property
    def moves(self):
        """Generate moves for all pieces of player on the board.

        Return:
            A dictionary containing all possible moves for each square player has a piece on.

        NOTE: Ideally the piece would be used as key but it is unhashable.
        """
        _moves = {}

        def deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

            return source_piece.deployable(target) and target_piece is None

        def capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

        #   If there is a piece on the target, check their allegiance.
            if target_piece is not None:
                return source_piece.capturable(target) and source_piece.orientation != target_piece.orientation

            return False

    #   Check only pieces of player:
        for piece in self.pieces:
            _moves[piece] = piece.moves  # Add the moves of specific piece keyed by itself.

            piece.deployable = MethodType(deployable, piece)  # Update deployability context for specific piece.
            piece.capturable = MethodType(capturable, piece)  # Update capturability context for specific piece.

        return _moves

    def move(self, piece: Piece, target: Square | str):
        """Move whatever is in source square to target square if move is valid.

        Args:
            source: The square in notation the piece is on
            target: The square in notation the piece wants to go to.
        """
        target = Square(target)

        source = piece.square

        if source is not None and piece in self.moves:
            if target in self.moves[piece]:
                self.board[source], self.board[target] = None, piece

                piece.has_moved = True
