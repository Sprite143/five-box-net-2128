# Verification of the five-box net

*October 2026.*

The net in `data/cells.txt` has 2,128 unit squares. These checks were run independently of the search that found it,
using tools written separately from that search.

## The shape

| Check | Result |
| --- | --- |
| Number of squares | 2,128 |
| Connected | yes |
| Holes | none (Euler characteristic V − E + F = 1) |
| Squares meeting only at a corner | none |
| Boundary | one closed curve of 1,204 unit edges |
| Bounding box | 389 × 191 |
| SHA-256 of the sorted list (`x,y` pairs joined by `;`, one trailing LF) | `1c42ebccb47d7236cd757325570c3fe7023b38486c9aa18ef7b78a18e86af8ef` |

## Static folds: every box of area 2,128

Area 2,128 has 28 integer boxes. Four separately written checkers agree that the net folds into exactly five of them.

| Checker | Result |
| --- | --- |
| `anyfold` (C, from the four-box project), all 28 boxes | folds 2×4×176, 4×8×86, 4×14×56, 4×16×50, 4×26×32; no others |
| The area-106 paper authors' checker, `OutputReader.ValidNetSolutionChecker.hasSolution` from [hidny/CuboidSimplePhaseNetSearch](https://github.com/hidny/CuboidSimplePhaseNetSearch), compiled from that repository's source, all 28 boxes | FOLDS for the same five; "does not fold" for the other 23 |
| An independent Python folder (rolling a frame square by square, pairing boundary edges in 3D) | folds all five |
| `verify_folds.py` in this repository (standard library only) | see the README |

**Controls.** The same checkers give the 532-square four-box net
([Sprite143/four-box-net-532](https://github.com/Sprite143/four-box-net-532)) exactly its known four boxes and reject
the other four boxes of area 532.

## How the boxes are glued

Pairing the boundary edges that meet in 3D shows how each fold closes up. In all five boxes the paper's boundary is
glued along a branched tree with 7 fold points (each at an inward corner of the outline, each becoming a box corner),
5 flat branch points, and one box corner formed where a convex corner meets a straight stretch of boundary. This is
different from the 532-square net, whose folds close up like zips (three or four fold points), and it is why the net
is not limited to two zip choices on each edge of the strip.

## Rigid folding motion

`simulate_folding.py` (the whole-panel version from the four-box repository, unchanged) folds each box as a rigid
object. The squares that land on one face and touch form a flat panel; the panels form a tree; each fold line turns
from 0° to 90° while the others are held fixed, and every position is tested for two squares passing through each
other (squares shrunk slightly about their centres so that legitimate shared edges and corners do not count).

Starting from square (57, −30), one end of the strip, and folding the fold lines nearest that square first:

| Box | Panels | Fold lines | Positions at 0.5° | Collisions |
| --- | ---: | ---: | ---: | ---: |
| 2 × 4 × 176 | 81 | 80 | 14,400 | 0 |
| 4 × 8 × 86 | 74 | 73 | 13,140 | 0 |
| 4 × 14 × 56 | 44 | 43 | 7,740 | 0 |
| 4 × 16 × 50 | 54 | 53 | 9,540 | 0 |
| 4 × 26 × 32 | 43 | 42 | 7,560 | 0 |

(0.5° steps, squares shrunk by 0.5%; the same start is also collision-free at 1° steps, in both orders.) The order
matters: starting from the middle of the strip, four of the five boxes collide, so the test does detect collisions.
The simulator reproduces the published result for the 532-square net (no collisions, 17,100 positions at 1°).

## Not checked

- The original write-up (`docs/fivebox-2128-original-writeup.md`) embeds its own verification script. The checks
  above did not use it.
- No physical paper model has been made.
