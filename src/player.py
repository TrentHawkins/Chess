"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from dataclasses import dataclass
from types import MethodType

from .board import Board
from .move import Capture, Move
from .moves.castle import Castle
from .piece import Orientation, Piece
from .pieces.melee import King
from .pieces.ranged import Rook
from .square import Square


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

        Also defines player-context-sensitive rules for evaluating piece legal moves.
        King safety is not relevant nor can be resolve here.
        The piece legal moves shall be agnostically updated here though,
        because the squares the player checks are legit, since king safety is irrelevant when it is not their turn!
        In elaboration, if an opponent walks their king in danger, it does not matter if your king will be in danger after;
        their king will die first.
        """
        self.name: str = name
        self.orientation: Orientation = Orientation[color]  # The allegiance of the player.
        self.board: Board = board  # The board this player is playing on.

    #   Assign pieces to player agnostically, so that custom position can also be loaded.
        self.pieces: set[Piece] = set(piece for piece in self.board if piece.orientation == self.orientation)
        self.captured: Counter[Piece] = Counter()  # NOTE: Not yet implemented.

        def piece_deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

            return source_piece.__class__.deployable(source_piece, target) and target_piece is None

        def piece_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            return source_piece.__class__.capturable(source_piece, target) and target_piece is not None \
                and source_piece.orientation != target_piece.orientation

        for piece in self.pieces:
            piece.deployable = MethodType(piece_deployable, piece)
            piece.capturable = MethodType(piece_capturable, piece)

    #   Keep the player's king registered, as it is a special piece.
        for piece in self.pieces:
            if type(piece) is King:
                self.king: King = piece

    #   Castles
        self.castles: set[Castle] = set()

    #   Do not allow castles in custom positions as the `has_moved` conditions is unresolvable mathematically.
        for piece in self.pieces:
            if type(piece) is Rook:
                self.castles.add(Castle(self.king, piece))

    def __repr__(self):
        """Represent a player by name and captured pieces.

        NOTE: Timer is not implemented yet.

        Returns:
            Players name followed by a color window and captured pieces
        """
        ...

    @property
    def squares_checked(self) -> set[Square]:
        """Get all squares checked by player.

        Returns:
            A flattened union of all squares the player has access to.
        """
        return set().union(*(piece.squares for piece in self.pieces))

    def __call__(self, move: Move):
        """Move the source piece to target square if move is valid.

        Args:
            source_piece: The piece to move.
            target: The square in notation the piece wants to go to.
        """
        target_piece = self.board(move)  # Make the move.

        if target_piece is not None:  # If there was a piece there (opponent's),
            self.captured[target_piece] += 1  # Add lost piece to target collection, not that it has lost its square.
