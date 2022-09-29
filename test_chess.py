"""Unit tests for the Chess project."""

from unittest import TestCase
from unittest.mock import patch  # To mock user input for interactive tests.


class TestChess(TestCase):
    """Unit tests for the game engine."""

    def test_simple_chess_game(self):
        """Test initial game setup with players."""
        from src.chess import Chess
        from src.pieces.melee import King, Knight
        from src.pieces.pawn import Pawn
        from src.pieces.ranged import Bishop, Queen, Rook

        new_game = Chess()

    #   White pieces:
        assert new_game.current.pieces == {
            Rook("white", "a1"),
            Knight("white", "b1"),
            Bishop("white", "c1"),
            Queen("white", "d1"),
            King("white", "e1"),
            Bishop("white", "f1"),
            Knight("white", "g1"),
            Rook("white", "h1"),
        } | set(Pawn("white", f"{file}2") for file in "abcdefgh")

    #   Black pieces:
        assert new_game.opponent.pieces == {
            Rook("black", "a8"),
            Knight("black", "b8"),
            Bishop("black", "c8"),
            Queen("black", "d8"),
            King("black", "e8"),
            Bishop("black", "f8"),
            Knight("black", "g8"),
            Rook("black", "h8"),
        } | set(Pawn("white", f"{file}7") for file in "abcdefgh")

    def test_captured_counting(self):
        """Check if reduced implied hashing of captured pieces works on piece counters."""
        from collections import Counter

        from src.pieces.melee import King, Knight
        from src.pieces.pawn import Pawn
        from src.pieces.ranged import Bishop, Queen, Rook

        captured = Counter()

    #   Lets capture some pawns.
        captured += Counter({Pawn("white")})
        captured += Counter({Pawn("white")})

    #   Lets get the queen.
        captured += Counter({Queen("white")})

    #   Emulate pawn promotion to queen?
        captured -= Counter({Queen("white")})
        captured += Counter({Pawn("white")})

    #   Notice how color is ignored, as it should; pieces are binned by player.  # NOTE: Probably remove color attribute?
        captured += Counter({Pawn("black")})

        assert captured == Counter({
            Pawn("white"): 4,
        })

    def test_moves(self):
        """Test legal moves on initial board.

        This board presents a famous game by Michai Tal the moment both players castled.
        NOTE: At this point this board is made by manually filling the pieces into their squares.
        NOTE: At a later point this board will be made by making the actual moves of the Tal game from a new game position.
        NOTE: For now all moves are listed indistinct of player.
        NOTE: A lot of this code will be encapsulated into `Piece` specialized `move` functions.
        """
        from src.board import Board
        from src.chess import Chess
        from src.square import Square

    #   The chosen position is only a few moves from the start so it is faster to start from a new game and delete pieces.
        tal = Board()

    #   Pawns lost:
        del tal["e2"]
        del tal["e7"]
        del tal["d2"]
        del tal["d7"]

    #   Pawns:
        tal["c7"], tal["c6"] = tal["c6"], tal["c7"]
        tal["c6"].has_moved = True  # type: ignore  # Pawn has moved

    #   Knights:
        tal["g1"], tal["f3"] = tal["f3"], tal["g1"]
        tal["b8"], tal["d7"] = tal["d7"], tal["b8"]
        tal["b1"], tal["e4"] = tal["e4"], tal["b1"]
        tal["g8"], tal["f6"] = tal["f6"], tal["g8"]

    #   Bishops:
        tal["c1"], tal["g5"] = tal["g5"], tal["c1"]
        tal["f8"], tal["e7"] = tal["e7"], tal["f8"]

    #   Queens and King castles:
        tal["d1"], tal["d4"] = tal["d4"], tal["d1"]

    #   King castles:
        tal["e1"], tal["a1"], tal["c1"], tal["d1"] = tal["c1"], tal["d1"], tal["e1"], tal["a1"]
        tal["e8"], tal["h8"], tal["g8"], tal["f8"] = tal["g8"], tal["f8"], tal["e8"], tal["h8"]

    #   A player, designated ONLY after the board is all set to the desired position:
        new_game = Chess(tal)

        piece = tal["c1"]
        assert piece is not None
        assert piece.squares == {  # King (white)
            Square("d2"),  # ↗
            Square("b1"),  # ←
        }
        piece = tal["d4"]
        assert piece is not None
        assert piece.squares == {  # Queen (white)
            Square("e5"),  # ↗
            Square("f6"),  # ↗  # capture
            Square("d5"),  # ↑
            Square("d6"),  # ↑
            Square("d7"),  # ↑  # capture
            Square("c5"),  # ↖
            Square("b6"),  # ↖
            Square("a7"),  # ↖  # capture
            Square("c4"),  # ←
            Square("b4"),  # ←
            Square("a4"),  # ←
            Square("c3"),  # ↙
            Square("d3"),  # ↓
            Square("d2"),  # ↓
            Square("e3"),  # ↘
        }
        piece = tal["f1"]
        assert piece is not None
        assert piece.squares == {  # Bishop (white/white)
            Square("e2"),  # ↖
            Square("d3"),  # ↖
            Square("c4"),  # ↖
            Square("b5"),  # ↖
            Square("a6"),  # ↖
        }
        piece = tal["g5"]
        assert piece is not None
        assert piece.squares == {  # Bishop (white/black)
            Square("f6"),  # ↖  # capture
            Square("f4"),  # ↙
            Square("e3"),  # ↙
            Square("d2"),  # ↙
            Square("h4"),  # ↘
            Square("h6"),  # ↗
        }
        piece = tal["e4"]
        assert piece is not None
        assert piece.squares == {  # Knight (white/white)
            Square("f6"),  # ↗ + ↑  # capture
            Square("g3"),  # ↘ + →
            Square("d2"),  # ↙ + ↓
            Square("c3"),  # ↙ + ←
            Square("c5"),  # ↖ + ←
            Square("d6"),  # ↖ + ↑
        }
        piece = tal["f3"]
        assert piece is not None
        assert piece.squares == {  # Knight (white/black)
            Square("h4"),  # ↗ + →
            Square("g1"),  # ↘ + ↓
            Square("e1"),  # ↙ + ↓
            Square("d2"),  # ↙ + ←
            Square("e5"),  # ↖ + ↑
        }
        piece = tal["h1"]
        assert piece is not None
        assert piece.squares == {  # Rook (white/white)
            Square("g1"),  # ↑
        }
        piece = tal["d1"]
        assert piece is not None
        assert piece.squares == {  # Rook (white/black)
            Square("e1"),  # ↑
            Square("d2"),  # ↑
            Square("d3"),  # ↑
        }
        piece = tal["a2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/A)
            Square("a3"),  # ↑
            Square("a4"),  # ↑
        }
        piece = tal["b2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/B)
            Square("b3"),  # ↑
            Square("b4"),  # ↑
        }
        piece = tal["c2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/C)
            Square("c3"),  # ↑
            Square("c4"),  # ↑
        }
        piece = tal["f2"]
        assert piece is not None
        assert piece.squares == set()  # Pawn (white/F)
        piece = tal["g2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/G)
            Square("g3"),  # ↑
            Square("g4"),  # ↑
        }
        piece = tal["h2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/H)
            Square("h3"),  # ↑
            Square("h4"),  # ↑
        }

    def test_king(self):
        """Test king movements and related movements."""
        from src.board import Board
        from src.chess import Chess
        from src.square import Square

    #   Make a custom board first:
        board = Board()

    #   Manually put the king in semi-danger:
        board["e2"], board["e4"] = board["e4"], board["e2"]
        board["c8"], board["a6"] = board["a6"], board["c8"]
        board["f8"], board["a5"] = board["a5"], board["f8"]

        set_game = Chess(board)

        pawn = set_game.board["d2"]
        king = set_game.board["e1"]

        assert king is not None
        assert king.squares == set()  # Because it puts the king in check from "Ba6".
        assert pawn is not None
        assert pawn.squares == set()  # Because it discovers a check to the king from "Ba5".  # FIXME: Not implemented yet.

    def test_castling(self):
        """Test castling."""
        from src.board import Board
        from src.chess import Chess
        from src.move import Move
        from src.pieces.melee import King
        from src.pieces.ranged import Bishop, Rook
        from src.square import Square

    #   Make board empty to test singular castling conditions.
        board = Board(empty=True)

    #   Put castling pieces on the board to be found by the players' castles.
        board["e1"] = King("white")
        board["a1"] = Rook("white")
        board["h1"] = Rook("white")
        board["e8"] = King("black")
        board["e6"] = Bishop("black")
        board["e7"] = Bishop("black")
        board["a8"] = Rook("black")
        board["h8"] = Rook("black")

    #   Make new game with custom position.
        new_game = Chess(board=board)

    #   HACK: This is a custom position, however for the sake of castling tests, we must assume pieces haven't moved.
        for piece in board:
            piece.has_moved = False

    #   King castling squares:
        short = Square("g1")
        other = Square("c1")

    #   They should both be deployable:
        assert new_game.current.king.castleable(short)
        assert new_game.current.king.castleable(other)

    #   Add some benigh danger to castling long:
        new_game.opponent(Move(board["a8"], "b8"))  # type: ignore

    #   They should still be both deployable.
        assert new_game.current.king.castleable(short)
        assert new_game.current.king.castleable(other)

    #   Castling other square checked.
        new_game.opponent(Move(board["b8"], "c8"))  # type: ignore

    #   Should only see one.
        assert new_game.current.king.castleable(short)
        assert not new_game.current.king.castleable(other)

    #   Castling other middle checked.
        new_game.opponent(Move(board["c8"], "d8"))  # type: ignore

    #   Should only see one.
        assert new_game.current.king.castleable(short)
        assert not new_game.current.king.castleable(other)

    #   King checked. Pull other danger away to see if king check kills both castles.
        new_game.opponent(Move(board["d8"], "b8"))  # type: ignore
        new_game.opponent(Move(board["e7"], "b4"))  # type: ignore

    #   Should see none.
        assert not new_game.current.king.castleable(short)
        assert not new_game.current.king.castleable(other)

    #   Lets see if we can retrive them when the danger is gone.
        new_game.opponent(Move(board["b4"], "e7"))  # type: ignore

    #   Should see both.
        assert new_game.current.king.castleable(short)
        assert new_game.current.king.castleable(other)

    #   Lets put an obstacle on the other castle near the rook, where the king doesn't even reach.
        new_game.current(Move(board["e6"], "f5"))  # type: ignore
        new_game.current(Move(board["f5"], "b1"))  # type: ignore

    #   Should see one.
        assert new_game.current.king.castleable(short)
        assert not new_game.current.king.castleable(other)

    #   Remove block.
        new_game.current(Move(board["b1"], "f5"))  # type: ignore
        new_game.current(Move(board["f5"], "e6"))  # type: ignore

    #   Should see both.
        assert new_game.current.king.castleable(short)
        assert new_game.current.king.castleable(other)

    #   Lets move the king back and forth.
        new_game.current(Move(board["e1"], "d1"))  # type: ignore
        new_game.current(Move(board["d1"], "e1"))  # type: ignore

    #   Should see none.
        assert not new_game.current.king.castleable(short)
        assert not new_game.current.king.castleable(other)

    @patch(
        'builtins.input',
        side_effect=[
            "e2-e4",
            "c7-c5",
            "e4-e5",
            "d7-d5",
            "e5xd6",  # This is the en-passant move.
            "e7-e6",  # Just a response to feed an even number of moves.
        ],
    )
    def test_en_passant(self, mock_input):
        """Test if en-passant works in full. Careful, this is an interactive test."""
        from src.chess import Chess

        new_game = Chess()


class TestPlayer:
    """Unit tests for players."""

    def test_move(self):
        """Test draft move method."""
        from src.board import Board
        from src.chess import Chess
        from src.move import Capture, Move

        new_game = Chess()

    #   HACK: Do not swirl players, just use both as is for simplicity:
        white = new_game.current
        black = new_game.opponent
        board = new_game.board

        white_pawn = board["e2"]
        white(Move(white_pawn, "e4"))  # type: ignore  # The most famous opening move in the history of chess!
        assert board["e2"] is None
        assert board["e4"] is white_pawn

        black_pawn = board["d7"]
        black(Move(black_pawn, "d5"))  # type: ignore  # An untypical response to create a capturing scenario.
        assert board["d7"] is None
        assert board["d5"] is black_pawn

        white_pawn = board["e4"]
        black_pawn = board["d5"]
        white(Capture(white_pawn, "d5"))  # type: ignore  # The pawn at "e4" takes the pawn at "d5".
        assert board["e4"] is None
        assert board["d5"] is white_pawn

    #   Ascertain that the captured pawn is properly gone:
        assert black_pawn is not None
        assert black_pawn.square is None
        assert black_pawn not in black.pieces
        assert black_pawn in white.captured and white.captured[black_pawn] == 1


class TestPieces:
    """Unit tests for various pieces."""

    def test_pawn_promotion(self):
        """Test that pawn promotion successfully mutates pawn."""
        from src.board import Board
        from src.moves.pawn import Promotion
        from src.pieces.pawn import Pawn
        from src.pieces.ranged import Queen
        from src.square import Square

        board = Board(empty=True)

        pawn = Pawn("white")
        board["e7"] = pawn

        assert pawn.square == Square("e7")

        board(Promotion(pawn, Square("e8"), Queen))

        assert pawn.square == Square("e8")  # Check if promoted pawn is still in-place.
        assert type(pawn) is Queen  # Check if pawn was indeed promoted.
        assert pawn.squares == {
            Square("d8"),
            Square("c8"),
            Square("b8"),
            Square("a8"),
            Square("d7"),
            Square("c6"),
            Square("b5"),
            Square("a4"),
            Square("e7"),
            Square("e6"),
            Square("e5"),
            Square("e4"),
            Square("e3"),
            Square("e2"),
            Square("e1"),
            Square("f7"),
            Square("g6"),
            Square("h5"),
            Square("f8"),
            Square("g8"),
            Square("h8"),
        }  # Check if pawn has the priviligies of its new rank.


class TestSquare:
    """Unit tests exclusive to the squares."""

    def test_square_operations(self):
        """Test that squares can safely be operated on and that operations can be stacked."""
        from src.square import Square, Vector

        assert Square("e4") + Vector(-1, 0) == Square("e5")
        assert Square("e4") + Vector(0, -1) == Square("d4")
        assert Square("e4") + Vector(+1, 0) == Square("e3")
        assert Square("e4") + Vector(0, +1) == Square("f4")
