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
        assert next(new_game.player).pieces == {
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
        assert next(new_game.player).pieces == {
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

    def test_moves(self):
        """Test legal moves on initial board.

        This board presents a famous game by Michai Tal the moment both players castled.
        NOTE: At this point this board is made by manually filling the pieces into their squares.
        NOTE: At a later point this board will be made by making the actual moves of the Tal game from a new game position.
        NOTE: For now all moves are listed indistinct of player.
        NOTE: A lot of this code will be encapsulated into `Piece` specialized `move` functions.
        """
        from src.board import Board
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

        tal_moves = \
        {
            tal["c1"]:  # King (white)
            {
                Square("d2"),  # ↗
                Square("b1"),  # ←
            },
            tal["d4"]:  # Queen (white)
            {
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
            },
            tal["f1"]:  # Bishop (white/white)
            {
                Square("e2"),  # ↖
                Square("d3"),  # ↖
                Square("c4"),  # ↖
                Square("b5"),  # ↖
                Square("a6"),  # ↖
            },
            tal["g5"]:  # Bishop (white/black)
            {
                Square("f6"),  # ↖  # capture

                Square("f4"),  # ↙
                Square("e3"),  # ↙
                Square("d2"),  # ↙

                Square("h4"),  # ↘

                Square("h6"),  # ↗
            },
            tal["e4"]:  # Knight (white/white)
            {
                Square("f6"),  # ↗ + ↑  # capture
                Square("g3"),  # ↘ + →
                Square("d2"),  # ↙ + ↓
                Square("c3"),  # ↙ + ←
                Square("c5"),  # ↖ + ←
                Square("d6"),  # ↖ + ↑
            },
            tal["f3"]:  # Knight (white/black)
            {
                Square("h4"),  # ↗ + →
                Square("g1"),  # ↘ + ↓
                Square("e1"),  # ↙ + ↓
                Square("d2"),  # ↙ + ←
                Square("e5"),  # ↖ + ↑
            },
            tal["h1"]:  # Rook (white/white)
            {
                Square("g1"),  # ↑
            },
            tal["d1"]:  # Rook (white/black)
            {
                Square("e1"),  # ↑

                Square("d2"),  # ↑
                Square("d3"),  # ↑
            },
            tal["a2"]:  # Pawn (white/A)
            {
                Square("a3"),  # ↑
                Square("a4"),  # ↑
            },
            tal["b2"]:  # Pawn (white/B)
            {
                Square("b3"),  # ↑
                Square("b4"),  # ↑
            },
            tal["c2"]:  # Pawn (white/C)
            {
                Square("c3"),  # ↑
                Square("c4"),  # ↑
            },
            tal["f2"]:  # Pawn (white/F)
            set(),
            tal["g2"]:  # Pawn (white/G)
            {
                Square("g3"),  # ↑
                Square("g4"),  # ↑
            },
            tal["h2"]:  # Pawn (white/H)
            {
                Square("h3"),  # ↑
                Square("h4"),  # ↑
            },
            tal["g8"]:  # King (black)
            {
                Square("h8"),  # →
            },
            tal["d8"]:  # Queen (black)
            {
                Square("e8"),  # →

                Square("c7"),  # ↙
                Square("b6"),  # ↙
                Square("a5"),  # ↙
            },
            tal["c8"]:  # Bishop (black/white)
            set(),
            tal["e7"]:  # Bishop (black/black)
            {
                Square("d6"),  # ↙
                Square("c5"),  # ↙
                Square("b4"),  # ↙
                Square("a3"),  # ↙
            },
            tal["f6"]:  # Knight (black/white)
            {
                Square("h5"),  # ↘ + →
                Square("g4"),  # ↘ + ↓
                Square("e4"),  # ↙ + ↓  # capture
                Square("d5"),  # ↙ + ←
                Square("e8"),  # ↖ + ↑
            },
            tal["d7"]:  # Knight (black/black)
            {
                Square("e5"),  # ↘ + ↓
                Square("c5"),  # ↙ + ↓
                Square("b6"),  # ↙ + ←
                Square("b8"),  # ↖ + ←
            },
            tal["a8"]:  # Rook (black/white)
            {
                Square("b8"),  # →
            },
            tal["f8"]:  # Rook (black/black)
            {
                Square("e8"),  # ←
            },
            tal["a7"]:  # Pawn (black/A)
            {
                Square("a6"),  # ↓
                Square("a5"),  # ↓
            },
            tal["b7"]:  # Pawn (black/B)
            {
                Square("b6"),  # ↓
                Square("b5"),  # ↓
            },
            tal["c6"]:  # Pawn (white/C)
            {
                Square("c5"),  # ↓
            },
            tal["f7"]:  # Pawn (white/F)
            set(),
            tal["g7"]:  # Pawn (black/G)
            {
                Square("g6"),  # ↓
            },
            tal["h7"]:  # Pawn (black/H)
            {
                Square("h6"),  # ↓
                Square("h5"),  # ↓
            },
        }

        assert tal.moves == tal_moves

    def test_move(self):
        """Test draft move method."""
        from src.board import Board

        board = Board()
        pawn = board["e2"]

        assert pawn is not None

        board.move(pawn, "e4")  # The most famous opening move in the history of chess!

        assert board["e2"] is None
        assert board["e4"] is pawn


class TestSquare:
    """Unit tests exclusive to the squares."""

    def test_square_operations(self):
        """Test that squares can safely be operated on and that operations can be stacked."""
        from src.square import Square, Vector

        assert Square("e4") + Vector(-1, 0) == Square("e5")
        assert Square("e4") + Vector(0, -1) == Square("d4")
        assert Square("e4") + Vector(+1, 0) == Square("e3")
        assert Square("e4") + Vector(0, +1) == Square("f4")
