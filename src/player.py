"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from types import MethodType

from .board import Board
from .move import Capture, Move
from .moves.king import Castle
from .moves.pawn import Jump, Promotion
from .piece import Orientation, Piece
from .pieces.melee import King, Knight
from .pieces.pawn import Pawn
from .pieces.ranged import Bishop, Queen, Rook
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
        """
        self.name: str = name
        self.orientation: Orientation = Orientation[color]  # The allegiance of the player.
        self.board: Board = board  # The board this player is playing on.

    #   Assign pieces to player agnostically, so that custom position can also be loaded.
        self.pieces: set[Piece] = set(piece for piece in self.board if piece.orientation == self.orientation)
        self.captured: Counter[Piece] = Counter(
            {
                Pawn(-self.orientation): 0,
                Bishop(-self.orientation): 0,
                Knight(-self.orientation): 0,
                Rook(-self.orientation): 0,
                Queen(-self.orientation): 0,
            }
        )
        self.material: int = 0  # Total material in terms of captured pieces' values.

    #   Keep track of moves made here, indexed by rounds.
        self.history: list[Move] = []

    #   Keep track of draw offer or resignation intent, as consent from both players is needed (for draw):
        self.draw: bool = False
        self.victory: bool = False

    #   Keep the player's king registered, as it is a special piece.
        for piece in self.pieces:
            if type(piece) is King:
                self.king: King = piece

    def __repr__(self):
        """Represent a player by name and captured pieces.

        NOTE: Timer is not implemented yet.

        Returns:
            Players name followed by a color window and captured pieces
        """
        return f"         │ {' '.join(str(piece) for piece in self.captured.keys())}     \n" + \
        f" {self.name:7s} │ {' '.join(str(count) for count in self.captured.values())} {self.material:+03d} "

    def update(self):
        """Define player-context-sensitive rules for evaluating piece legal moves.

        This is a necessary step, because what rules opponent obeys must be a bit trimmed to that of the current player.
        This will be invoked by the chess engine for the corresponding opponent player.

        King safety is not relevant nor can be resolved here.
        The piece legal moves shall be agnostically updated here though,
        because the squares the player checks are legit, since king safety is irrelevant when it is not their turn!
        In elaboration, if an opponent walks their king in danger, it does not matter if your king will be in danger after;
        their king will die first.
        """

        def piece_deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

            is_empty = target_piece is None or type(target_piece) is Piece

            return Piece.deployable(source_piece, target) and is_empty

        def piece_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            is_not_empty = target_piece is not None and type(target_piece) is not Piece \
                and source_piece.orientation != target_piece.orientation

            return Piece.capturable(source_piece, target) and is_not_empty

    #   Add ghost pieces to target of pawns:
        def pawns_capturable(source_piece: Pawn, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            is_not_empty = target_piece is not None \
                and source_piece.orientation != target_piece.orientation

            return Pawn.capturable(source_piece, target) and is_not_empty

        for piece in self.pieces:
            piece.deployable = MethodType(piece_deployable, piece)

            if type(piece) is Pawn:
                piece.capturable = MethodType(pawns_capturable, piece)

            else:
                piece.capturable = MethodType(piece_capturable, piece)

    #   Castleability has to be reset too to avoid infinite recursion.
    #   Castling is not a cpaturing move to so completely reset it for opponent's sake.
        self.king.castleable = MethodType(King.castleable, self.king)

    #   Count material off-line to allow contextual editing (to make this a material difference).
        self.material = sum(piece.value * count for piece, count in self.captured.items())

    def __call__(self, move: Move):
        """Move the source piece to target square if move is valid.

        Jumps should be checked here, because a ghost piece of the same color as the player must be generated with them.

        Args:
            move: The move to make.
        """
        target_piece = self.board(move)  # Make the move.

        if type(move) is Jump:
            self.board[move.middle] = Piece(self.orientation)  # This will have to go on the next round (2 turns).

    #   NOTE: The en-passant can only be detected by type-checking, as it is otherwise a normal capture.
        if type(target_piece) is Piece:  # If target piece is a ghost,
            if type(move.piece) is Pawn:  # If it is a pawn targeting it en-passant,
                target = move.square + move.piece.step * target_piece.orientation

                target_piece, self.board[target] = self.board[target], None

    #   If there was a opponent piece there, properly dispose of it.
        if target_piece is not None:
            target_piece.square = None

            self.captured[target_piece] += 1

    def read(self) -> Move:
        """Read move from standard input with a prompt.

        Infinite movement reading till the user gets it right.

        Returns:
            A valid movemement or nothing at all.
        """
        prompt = "your turn"

        while True:
            notation = input(f"\033[H\033[18B{self.name}, {prompt}: \033[K")

            move = \
                Promotion.read(notation, self.pieces) or \
                Capture  .read(notation, self.pieces) or \
                Jump     .read(notation, self.pieces) or \
                Move     .read(notation, self.pieces) or \
                Castle   .read(notation, self.king)

        #   Check move here too to catch the re-try:
            if move is not None:
                self.history.append(move)  # Add move to history.
                self.draw = move.draw  # Delegate draw offer intent or response to player.

                print("033[12B")

                return move

            else:
                prompt = "try again"

                continue

    @property
    def squares(self) -> set[Square]:
        """Get all squares checked by player.

        Returns:
            A flattened union of all squares the player has access to.
        """
        return {square for piece in self.pieces for square in piece.squares}
