"""Implements movement rules and topology.

Codex of moves with respect to indexing:
    north: (-1,  0)
    west: ( 0, -1)
    south: (+1,  0)
    east: ( 0, +1)

Diagonals can be made from these:
    north_west: north + west
    south_west: south + west
    south_east: south + east
    north_east: north + east

Knight movement:
    north_north_west: north + north_west
    north_west_west: north_west + west
    south_west_west: south_west + west
    south_south_west: south + south_west
    south_south_east: south + south_east
    south_east_east: south_east + east
    north_east_east: north_east + east
    north_north_east: north + north_east

Pawn advance:
    north_north: 2 * north
    south_south: 2 * south

All straight lines can be made by repeating application of theres.

Kings: Castling is special and remember it has viability rules too.
Pawns: both capturing and en-passant are kind of special.
    Capturing logic may be implementable here.
"""

from src.board import Vector

# straight steps (King)
north = Vector(-1, 0)
west = Vector(0, -1)
south = Vector(+1, 0)
east = Vector(0, +1)

# diagonal steps (King)
north_west = north + west
south_west = south + west
south_east = south + east
north_east = north + east

# Knight moves
north_north_west = north + north_west
north_west_west = north_west + west
south_west_west = south_west + west
south_south_west = south + south_west
south_south_east = south + south_east
south_east_east = south_east + east
north_east_east = north_east + east
north_north_east = north + north_east

# Pawn initial moves
north_north = north * 2
south_south = south * 2
