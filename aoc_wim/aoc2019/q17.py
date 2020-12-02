"""
--- Day 17: Set and Forget ---
https://adventofcode.com/2019/day/17
"""
from aocd import data
from aoc_wim.aoc2019 import IntComputer
from aoc_wim.zgrid import ZGrid


test_calibration = """\
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""


test_path = """\
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......"""


# this next example is from an AoC beta tester
# https://www.reddit.com/r/adventofcode/comments/ebz338/2019_day_17_part_2_pathological_pathfinding/
test_pathological = """\
.........................................
...................#############.........
...................#.....................
...................#.....................
...................#.....................
...................#.....................
...................#.....................
...................###########...........
.............................#...........
...................#######...#...........
...................#.....#...#...........
...................#.....#...#...........
...................#.....#...#...........
...................#.....#...#...........
...................#.....#...#...........
.###########.......#.....#...#...........
.#.........#.......#.....#...#...........
.#.........#.....#####...#...#...........
.#.........#.....#.#.#...#...#...........
.#.....#############.#...#...###########.
.#.....#...#.....#...#...#.............#.
.#.....#...#######...#...#####.........#.
.#.....#.............#.......#.........#.
.#.....#.............#.......#.........#.
.#.....#.............#.......#.........#.
.#.....#.........#######################.
.#.....#.........#...#.......#...........
.#.....#.......#######.#######...........
.#.....#.......#.#.....#.................
.#######.......#.#.....#.................
...............#.#.....#.................
...#######.....#.###########.............
...#.....#.....#.......#...#.............
...#.....#.....#####...#...#.............
...#.....#.........#...#...#.............
...#.....#.........#...#...#.............
...#.....#.........#...#...#.............
...#.....###########...#####.............
...#.....................................
...#.....................................
...#.....................................
...###########...........................
.............#...........................
.............#...........................
.............#...........................
.............#...........................
.............#...........................
...^##########...........................
........................................."""

test_pathological_intcode = "1,330,331,332,109,3470,1101,1182,0,15,1101,1481,0,24,1002,0,1,570,1006,570,36,1001,571,0,0,1001,570,-1,570,1001,24,1,24,1105,1,18,1008,571,0,571,1001,15,1,15,1008,15,1481,570,1006,570,14,21102,1,58,0,1106,0,786,1006,332,62,99,21101,0,333,1,21102,73,1,0,1105,1,579,1102,0,1,572,1101,0,0,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,102,1,574,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1105,1,81,21101,0,340,1,1105,1,177,21102,477,1,1,1106,0,177,21101,514,0,1,21101,176,0,0,1106,0,579,99,21102,1,184,0,1106,0,579,4,574,104,10,99,1007,573,22,570,1006,570,165,1002,572,1,1182,21101,375,0,1,21101,0,211,0,1106,0,579,21101,1182,11,1,21102,222,1,0,1105,1,979,21102,388,1,1,21101,233,0,0,1105,1,579,21101,1182,22,1,21102,1,244,0,1105,1,979,21102,401,1,1,21101,255,0,0,1105,1,579,21101,1182,33,1,21101,266,0,0,1106,0,979,21101,414,0,1,21102,1,277,0,1105,1,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21102,1,1182,1,21102,1,313,0,1105,1,622,1005,575,327,1102,1,1,575,21102,327,1,0,1106,0,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,2,48,0,109,4,1202,-3,1,587,20102,1,0,-1,22101,1,-3,-3,21102,1,0,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1105,1,597,109,-4,2106,0,0,109,5,1202,-4,1,630,20102,1,0,-2,22101,1,-4,-4,21101,0,0,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,652,21002,0,1,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21102,1,702,0,1106,0,786,21201,-1,-1,-1,1105,1,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21102,731,1,0,1106,0,786,1106,0,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21101,0,756,0,1105,1,786,1106,0,774,21202,-1,-11,1,22101,1182,1,1,21101,0,774,0,1105,1,622,21201,-3,1,-3,1105,1,640,109,-5,2105,1,0,109,7,1005,575,802,21002,576,1,-6,20102,1,577,-5,1106,0,814,21101,0,0,-1,21101,0,0,-5,21101,0,0,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,39,-3,22201,-6,-3,-3,22101,1481,-3,-3,1202,-3,1,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21101,1,0,-1,1105,1,924,1205,-2,873,21102,1,35,-4,1106,0,924,1201,-3,0,878,1008,0,1,570,1006,570,916,1001,374,1,374,1201,-3,0,895,1101,0,2,0,2101,0,-3,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,922,20101,0,0,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,39,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,51,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1101,0,1,575,21101,0,973,0,1105,1,786,99,109,-7,2105,1,0,109,6,21101,0,0,-4,21101,0,0,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1106,0,1041,21101,0,-4,-2,1106,0,1041,21102,-5,1,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,1201,-2,0,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,2101,0,-2,0,1105,1,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1105,1,989,21101,439,0,1,1106,0,1150,21102,477,1,1,1106,0,1150,21102,1,514,1,21102,1149,1,0,1106,0,579,99,21101,0,1157,0,1105,1,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,2101,0,-5,1176,2101,0,-4,0,109,-6,2106,0,0,96,13,26,1,38,1,38,1,38,1,38,1,38,11,38,1,28,7,3,1,28,1,5,1,3,1,28,1,5,1,3,1,28,1,5,1,3,1,28,1,5,1,3,1,28,1,5,1,3,1,10,11,7,1,5,1,3,1,10,1,9,1,7,1,5,1,3,1,10,1,9,1,5,5,3,1,3,1,10,1,9,1,5,1,1,1,1,1,3,1,3,1,10,1,5,13,1,1,3,1,3,12,5,1,3,1,5,1,3,1,3,1,13,2,5,1,3,7,3,1,3,5,9,2,5,1,13,1,7,1,9,2,5,1,13,1,7,1,9,2,5,1,13,1,7,1,9,2,5,1,9,24,5,1,9,1,3,1,7,1,10,1,5,1,7,7,1,7,10,1,5,1,7,1,1,1,5,1,16,7,7,1,1,1,5,1,30,1,1,1,5,1,18,7,5,1,1,11,14,1,5,1,5,1,7,1,3,1,14,1,5,1,5,5,3,1,3,1,14,1,5,1,9,1,3,1,3,1,14,1,5,1,9,1,3,1,3,1,14,1,5,1,9,1,3,1,3,1,14,1,5,11,3,5,14,1,38,1,38,1,38,11,38,1,38,1,38,1,38,1,38,1,28,11,104"
test_pathological_path = """\
A,B,B,B,A,C,B,C,A,C
R,10,L,6,L,10,R,6
4,R,6,R,6,L,10,L,4,L
6,L,10,R,6,R,12,L
n
"""


def parsed(data):
    comp = IntComputer(data)
    comp.run()
    txt = "".join([chr(x) for x in reversed(comp.output)])
    grid = ZGrid(txt)
    grid.draw()
    return grid


def calibration(grid):
    result = 0
    for z0, txt in grid.items():
        if txt == "#" and {grid.get(z) for z in grid.near(z0)} == {"#"}:
            result += int(z0.real) * int(z0.imag)
    return result


def get_path(grid, compressed=True):
    # detect initial position and orientation
    [(z0, glyph)] = [(k,v) for (k,v) in grid.items() if v in "^>v<"]
    dz0 = grid.dzs[glyph]
    [z1] = [z for z in grid.near(z0) if grid.get(z) == "#"]
    steps = []

    # orient self onto scaffold
    if z0 + dz0 != z1:
        if z0 + dz0 * grid.turn_right == z1:
            steps.append("R")
            dz0 *= grid.turn_right
        elif z0 + dz0 * grid.turn_left == z1:
            steps.append("L")
            dz0 *= grid.turn_left
        else:
            assert z0 - dz0 == z1
            steps.extend("RR")
            dz0 *= grid.turn_around

    # find an uncompressed path
    z = z0
    dz = dz0
    while True:
        n = 0
        while grid.get(z + dz) == "#":
            n += 1
            z += dz
        steps.append(str(n))
        if grid.get(z + dz * grid.turn_right) == "#":
            dz *= grid.turn_right
            steps.append("R")
        elif grid.get(z + dz * grid.turn_left) == "#":
            dz *= grid.turn_left
            steps.append("L")
        else:
            break

    # compress path to memory requirement
    path = ",".join(steps)
    if compressed:
        options = compress(path)
        path = min(options, key=len)
        path += "\nn\n"  # suppress "continuous video feed"
    return path


def chunk_choices(path):
    choices = []
    for i in range(1, 20):
        chunk = path[:i]
        if path[i:i+1] not in {"", ","}:
            continue
        score = len(chunk) * path.count(chunk)
        choices.append((score, chunk))
    choices = {chunk: score for score, chunk in sorted(choices, reverse=True)}
    return choices


def compress(path, mem=20):
    results = []
    A_choices = chunk_choices(path)
    for A in A_choices:
        compressed_pathA = ""
        pathA = path
        while pathA.startswith(A):
            compressed_pathA += "A,"
            pathA = pathA[len(A):].lstrip(",")
        B_choices = chunk_choices(pathA)
        for B in B_choices:
            compressed_pathAB = compressed_pathA
            pathAB = pathA
            while pathAB.startswith((A, B)):
                if pathAB.startswith(A):
                    pathAB = pathAB[len(A):].lstrip(",")
                    compressed_pathAB += "A,"
                if pathAB.startswith(B):
                    pathAB = pathAB[len(B):].lstrip(",")
                    compressed_pathAB += "B,"
            C_choices = chunk_choices(pathAB)
            for C in C_choices:
                compressed_pathABC = compressed_pathAB
                pathABC = pathAB
                while pathABC.startswith((A, B, C)):
                    if pathABC.startswith(A):
                        pathABC = pathABC[len(A):].lstrip(",")
                        compressed_pathABC += "A,"
                    if pathABC.startswith(B):
                        pathABC = pathABC[len(B):].lstrip(",")
                        compressed_pathABC += "B,"
                    if pathABC.startswith(C):
                        pathABC = pathABC[len(C):].lstrip(",")
                        compressed_pathABC += "C,"
                if not pathABC:
                    result = compressed_pathABC.rstrip(",")
                    if len(result) <= mem:
                        results.append("\n".join([result, A, B, C]))
    return results


assert calibration(ZGrid(test_calibration)) == 76
uncompressed_test_path = get_path(ZGrid(test_path), compressed=False)
assert uncompressed_test_path == "R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2"
assert """\
A,B,C,B,A,C
R,8,R,8
R,4,R,4,R,8
L,6,L,2""" in compress(uncompressed_test_path)


grid = parsed(data)
print("part a", calibration(grid))
comp = IntComputer(data)
comp.reg[0] = 2
path = get_path(grid)
comp.input_text(path)
comp.run()
print("part b", comp.output[0])
