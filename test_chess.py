"""Unit tests for the Chess project."""


class TestChess:
    """Unit tests for the game engine."""

    def test_simple_chess_game(self):
        """Test initial game setup with players."""
        from src.chess import Chess
        from src.pieces.meleed import King, Knight
        from src.pieces.ranged import Bishop, Queen, Rook
        from src.pieces.special import Pawn

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

        from src.pieces.meleed import King, Knight
        from src.pieces.ranged import Bishop, Queen, Rook
        from src.pieces.special import Pawn

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

    def testKing(self):
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


class TestPlayer:
    """Unit tests for players."""

    def test_moves(self):
        """Test legal moves on initial board.

        This board presents a famous game by Michai Tal the moment both players castled.
        NOTE: At this point this board is made by manually filling the pieces into their squares.
        NOTE: At a later point this board will be made by making the actual moves of the Tal game from a new game position.
        NOTE: For now all moves are listed indistinct of player.
        NOTE: A lot of this code will be encapsulated into `Piece` specialized `move` functions.
        """
        from src.board import Board
        from src.player import Player
        from src.square import Square

    #   The chosen position is only a few moves from the start so it is faster to start from a new game and delete pieces.
        talB = Board()

    #   Pawns lost:
        del talB["e2"]
        del talB["e7"]
        del talB["d2"]
        del talB["d7"]

    #   Pawns:
        talB["c7"], talB["c6"] = talB["c6"], talB["c7"]
        talB["c6"].has_moved = True  # type: ignore  # Pawn has moved

    #   Knights:
        talB["g1"], talB["f3"] = talB["f3"], talB["g1"]
        talB["b8"], talB["d7"] = talB["d7"], talB["b8"]
        talB["b1"], talB["e4"] = talB["e4"], talB["b1"]
        talB["g8"], talB["f6"] = talB["f6"], talB["g8"]

    #   Bishops:
        talB["c1"], talB["g5"] = talB["g5"], talB["c1"]
        talB["f8"], talB["e7"] = talB["e7"], talB["f8"]

    #   Queens and King castles:
        talB["d1"], talB["d4"] = talB["d4"], talB["d1"]

    #   King castles:
        talB["e1"], talB["a1"], talB["c1"], talB["d1"] = talB["c1"], talB["d1"], talB["e1"], talB["a1"]
        talB["e8"], talB["h8"], talB["g8"], talB["f8"] = talB["g8"], talB["f8"], talB["e8"], talB["h8"]

    #   A player, designated ONLY after the board is all set to the desired position:
        Player("Tal", "white", talB)  # NOTE: THIS IS CRITICAL, otherwise constraints do not become board-sentsitive.

        piece = talB["c1"]
        assert piece is not None
        assert piece.squares == {  # King (white)
            Square("d2"),  # ↗
            Square("b1"),  # ←
        }
        piece = talB["d4"]
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
        piece = talB["f1"]
        assert piece is not None
        assert piece.squares == {  # Bishop (white/white)
            Square("e2"),  # ↖
            Square("d3"),  # ↖
            Square("c4"),  # ↖
            Square("b5"),  # ↖
            Square("a6"),  # ↖
        }
        piece = talB["g5"]
        assert piece is not None
        assert piece.squares == {  # Bishop (white/black)
            Square("f6"),  # ↖  # capture
            Square("f4"),  # ↙
            Square("e3"),  # ↙
            Square("d2"),  # ↙
            Square("h4"),  # ↘
            Square("h6"),  # ↗
        }
        piece = talB["e4"]
        assert piece is not None
        assert piece.squares == {  # Knight (white/white)
            Square("f6"),  # ↗ + ↑  # capture
            Square("g3"),  # ↘ + →
            Square("d2"),  # ↙ + ↓
            Square("c3"),  # ↙ + ←
            Square("c5"),  # ↖ + ←
            Square("d6"),  # ↖ + ↑
        }
        piece = talB["f3"]
        assert piece is not None
        assert piece.squares == {  # Knight (white/black)
            Square("h4"),  # ↗ + →
            Square("g1"),  # ↘ + ↓
            Square("e1"),  # ↙ + ↓
            Square("d2"),  # ↙ + ←
            Square("e5"),  # ↖ + ↑
        }
        piece = talB["h1"]
        assert piece is not None
        assert piece.squares == {  # Rook (white/white)
            Square("g1"),  # ↑
        }
        piece = talB["d1"]
        assert piece is not None
        assert piece.squares == {  # Rook (white/black)
            Square("e1"),  # ↑
            Square("d2"),  # ↑
            Square("d3"),  # ↑
        }
        piece = talB["a2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/A)
            Square("a3"),  # ↑
            Square("a4"),  # ↑
        }
        piece = talB["b2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/B)
            Square("b3"),  # ↑
            Square("b4"),  # ↑
        }
        piece = talB["c2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/C)
            Square("c3"),  # ↑
            Square("c4"),  # ↑
        }
        piece = talB["f2"]
        assert piece is not None
        assert piece.squares == set()  # Pawn (white/F)
        piece = talB["g2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/G)
            Square("g3"),  # ↑
            Square("g4"),  # ↑
        }
        piece = talB["h2"]
        assert piece is not None
        assert piece.squares == {  # Pawn (white/H)
            Square("h3"),  # ↑
            Square("h4"),  # ↑
        }

    def test_move(self):
        """Test draft move method."""
        from src.board import Board
        from src.chess import Chess

        new_game = Chess()

    #   HACK: Do not swirl players, just use both as is for simplicity:
        white = new_game.current
        black = new_game.opponent
        board = new_game.board

        white_pawn = board["e2"]
        white.move(white_pawn, "e4")  # type: ignore  # The most famous opening move in the history of chess!
        assert board["e2"] is None
        assert board["e4"] is white_pawn

        black_pawn = board["d7"]
        black.move(black_pawn, "d5")  # type: ignore  # An untypical response to create a capturing scenario.
        assert board["d7"] is None
        assert board["d5"] is black_pawn

        white_pawn = board["e4"]
        black_pawn = board["d5"]
        white.move(white_pawn, "d5")  # type: ignore  # The pawn at "e4" takes the pawn at "d5".
        assert board["e4"] is None
        assert board["d5"] is white_pawn

    #   Ascertain that the captured pawn is properly gone:
        assert black_pawn is not None
        assert black_pawn.square is None
        assert black_pawn not in black.pieces
        assert black_pawn in white.captured and white.captured[black_pawn] == 1


class TestBoard:
    """Unit tests for the board."""

    def test_board_piece_relations(self):
        """Test the various logical conditions imposed at board level."""
        from src.board import Board

        board = Board()

        source = board["h1"]
        friend = board["h2"]
        foe = board["h8"]

        assert source
        assert friend
        assert foe

        assert source.has_friend(friend)
        assert not source.has_friend(foe)
        assert not source.has_foe(friend)
        assert source.has_foe(foe)


class TestSquare:
    """Unit tests exclusive to the squares."""

    def test_square_operations(self):
        """Test that squares can safely be operated on and that operations can be stacked."""
        from src.square import Square, Vector

        assert Square("e4") + Vector(-1, 0) == Square("e5")
        assert Square("e4") + Vector(0, -1) == Square("d4")
        assert Square("e4") + Vector(+1, 0) == Square("e3")
        assert Square("e4") + Vector(0, +1) == Square("f4")
