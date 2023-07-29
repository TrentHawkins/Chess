# Chess

This is a chess game engine implemented in python.

Features supported include:
-   Interactive 2-player interface for playing games on a terminal, similarly to [GNU Chess](https://www.gnu.org/software/chess/),
-   Playable demos by loading list of move files:
    -   Demos are interactive, i.e. they are loaded move by move,
    -   Demos are breakable at any point the players wish to continue the game their own way,
-   Graphics (terminal), including:
    -   The (current) board (state),
    -   The players' status:
        -   Their name,
        -   Their captured pieces,
        -   The material difference with opponent, as evaluated by the values of respective captured pieces,
    -   A (buffered) move history in pairs of white and black moves, constantly updated as the game progresses.

# Usage

Run from root of repository with:

```sh
python $(cwd)/main.py
```
A menu will appear that has three choices:
-   `NEW GAME`: Start a new game from scratch,
-   `LOAD GAME`: Replay an annotated game, and continue from whichever point wished.
-   `EXIT`: It is self-explanatory.

## Playing a new game

The prompt accepts move commands in the form that designates a source square (that the piece we want to move is on) and a target square, the square we wish the piece to move to.

The regex pattern for reading moves `[a-h][1-8]-[a-h][1-8][BNRQ=#]?`. The output displayed in the move history is a graphical variation of the [Chess long notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)#Long_algebraic_notation).

The engine prevents illegal moves from being made. If such a move is inputed, the engine will re-ask for a new move. This includes dynamic rules, like movement blocks, or prohibitions due to king checks.

### Pawn promotion

If it is a pawn promotion in particular, append the type of piece you want to promote the pawn to:
-   `B` for a bishop
-   `N` for a rook
-   `R` for a ropk
-   `Q` for a queen

### Castling

Castling has special symbols:
-   `O-O` for castling short
-   `O-O-O` for caslting long

### Draw

One player may add `=` to their move to offer a draw. If the other player also adds `=` to their immediately next move, the game is drawn, by agreement, otherwise the game continues and a new draw offer has to be re-invoked from scratch if any. Note that a game may be drawn by stalemate as well.

### Resignation

One player may add `#` to their move to indicate they resign from the game. The game ends instantly at that point. Mind that the game ends with a checkmate as well.

As soon as the game ends, the application exits with the last output printed.

## Load game from file

A file with a move per line following the aforementioned regex pattern may be used to load a game and prescribe it move by move. The interface looks the same, but by pressing `Enter`, it will advance a move in the history provided by the file.

You may interrupt the file reading by entering a move of your own, instead of just pressing `Enter`, in which case the game will enter in "new game" mode. This way you can alway continue a saved game from any point you want as an alternative.
