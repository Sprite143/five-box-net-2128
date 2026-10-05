# A verified common net of five rectangular boxes

**Verified on 4 October 2026.**

A single connected, hole-free polyomino of **2,128 unit squares** is a common net of the following five pairwise noncongruent, positive-volume rectangular boxes:

| Box dimensions | Surface area | Volume |
| --- | ---: | ---: |
| 2 × 4 × 176 | 2,128 | 1,408 |
| 4 × 8 × 86 | 2,128 | 2,752 |
| 4 × 14 × 56 | 2,128 | 3,136 |
| 4 × 16 × 50 | 2,128 | 3,200 |
| 4 × 26 × 32 | 2,128 | 3,328 |

For each box, every unit surface square is covered exactly once and every adjacency in the paper maps to the same physical edge from both sides. Their distinct positive volumes certify that the boxes are noncongruent.

**This Markdown file is self-contained:** the certificate below contains the entire net, five folding frames, and a verifier requiring only Python's standard library. No accompanying files or machine-specific paths are needed.

## How it was found

A search first produced a connected, hole-free **530-square partial shape** that fitted portions of all five target surfaces. That exact retained shape had no common one-square extension.

Doubling the geometry replaced each square by a 2 × 2 block, giving a **2,120-square partial shape** for boxes with doubled dimensions. A search was then allowed to change the boundary on this finer relative grid. The successful repair retained **1,840** of those squares, removed **280**, and added **288**, producing the complete **2,128-square net**. The change was a boundary repair, rather than simply adding eight squares to the retained core.

The final search reached the certificate after 2,349,481 proposals. Exact coordinates and physical verification, rather than the search heuristic, establish the result.

## Verification

The recorded checks include:

- Two separate physical 3D geometry implementations verified all five foldings without relying on the search's transition tables.
- An independent exhaustive check tested **17,024 starting frames per box**, finding **eight successful frames** for each.
- Each box passed **68,096 directed physical transition checks** and all **7,308 directed paper joins**.
- The paper is connected, has Euler characteristic **1**, has no diagonal point pinches, and has one boundary component containing **1,204 unit edges**.
- A separate `anyfold` scan found exactly these five among positive-integer cuboids of surface area 2,128 in the grid-edge folding model.

The compact verifier below needs only one successful root frame for each box. It reconstructs all other frames and checks complete surface coverage, absence of overlaps, every induced paper adjacency, and the paper's disk topology using exact integer arithmetic.

## Scale and scope

Scaling this net by **1/2** gives a polygon of area **532** folding into:

**1 × 2 × 88; 2 × 4 × 43; 2 × 7 × 28; 2 × 8 × 25; 2 × 13 × 16.**

At that scale, its boundary uses **half-unit coordinates**. It is not a 532-unit-square polyomino; the finer boundary detail is essential to this example.

The result establishes five static, nonoverlapping surface developments of one simple paper polygon. It does not establish a minimum-area result, a repeatable construction for arbitrary numbers of boxes, or a continuous collision-free folding motion. No priority or first-discovery claim is made here.

## Exact certificate and reproduction

Copy the following code block into `verify_fivebox.py`, then run `python verify_fivebox.py` with Python 3. It prints five `PASS` lines and a final `VERIFIED` message. It also writes the exact coordinate file `fivebox-2128-canonical.cells` and the diagram `fivebox-2128.svg` beside the script.

Each coordinate `(x, y)` denotes the lower-left corner of the square `[x, x+1] × [y, y+1]`, with Cartesian y increasing upward. The row intervals in the code include both endpoints. Physical centers in the folding frames are stored at twice their actual coordinates, so all calculations remain integral.

The canonical coordinate serialization sorts cells lexicographically, joins `x,y` pairs with semicolons, and ends with a single LF newline. Its SHA-256 is:

```text
1c42ebccb47d7236cd757325570c3fe7023b38486c9aa18ef7b78a18e86af8ef
```

The original search output has a different cell order and file hash, but the same set of squares. Its SHA-256 is:

```text
3e0425f23ef55028499bc98edbc1a6faf28334d0b269af1fd76d63dcb1317697
```

```python
# Python 3, standard library only. Run without the -O option.
# Row format: y followed by inclusive x_start:x_end intervals.
from pathlib import Path
from itertools import product
from hashlib import sha256

ROWS = """
-218 438:441 444:445
-217 438:445
-216 438:445
-215 436:445
-214 431:438
-213 429:436
-212 427:434
-211 426:433
-210 422:429
-209 421:428
-208 419:426
-207 414:421
-206 414:421
-205 412:419
-204 410:417
-203 407:414
-202 407:414
-201 405:412
-200 403:410
-199 403:410
-198 403:410
-197 398:400 402:405 409:409
-196 395:402
-195 393:400
-194 393:400
-193 390:397
-192 388:395
-191 386:393
-190 386:393
-189 381:388
-188 379:386
-187 378:385
-186 374:381
-185 373:380
-184 371:378
-183 369:376
-182 364:369
-181 362:369
-180 362:369
-179 356:357 362:369
-178 351:366
-177 349:364
-176 347:362
-175 346:361
-174 342:357
-173 341:356
-172 339:354
-171 334:349
-170 334:349
-169 332:347
-168 330:345
-167 327:342
-166 327:342
-165 325:340
-164 318:318 322:333 335:337
-163 317:332
-162 317:332
-161 317:332
-160 315:330
-159 313:328
-158 313:328
-157 310:325
-156 308:323
-155 306:321
-154 306:321
-153 303:316
-152 303:314
-151 303:313
-150 302:309
-149 297:297 299:299 302:308
-148 297:306
-147 294:304
-146 294:297
-145 292:297
-144 290:297
-143 287:297
-142 287:294
-141 285:292
-140 283:290
-139 283:289
-138 283:285
-137 278:280 282:284
-136 275:282
-135 273:277
-134 273:277
-133 270:275
-132 268:273
-131 266:270
-130 266:270
-129 261:268
-128 259:266
-127 258:266
-126 254:266
-125 253:261 265:265
-124 251:258
-123 249:256
-122 238:241 244:256
-121 238:253
-120 238:251
-119 236:249
-118 231:249
-117 229:244
-116 227:242
-115 226:241
-114 222:237
-113 221:236
-112 219:234
-111 214:232
-110 214:229
-109 212:229
-108 210:229
-107 207:229
-106 207:222
-105 205:220
-104 198:198 202:218
-103 197:217
-102 197:213
-101 197:212
-100 195:210
-99 193:205
-98 193:205
-97 190:203
-96 188:201
-95 186:198
-94 186:198
-93 183:196
-92 183:189 191:193
-91 183:188
-90 182:188
-89 177:177 179:179 182:188
-88 177:186
-87 174:184
-86 174:184
-85 172:181
-84 170:179
-83 167:177
-82 167:177
-81 165:172
-80 163:170
-79 163:169
-78 163:165
-77 158:160 162:164
-76 155:162
-75 153:160
-74 153:153
-73 150:153
-72 148:153
-71 146:153
-70 146:150
-69 141:148
-68 139:146
-67 138:145
-66 134:141
-65 133:140
-64 131:138
-63 129:133
-62 124:133
-61 122:131
-60 122:129
-59 116:117 122:126
-58 111:126
-57 109:124
-56 107:117 119:121
-55 106:116
-54 102:116
-53 101:116
-52 99:114
-51 94:112
-50 94:112
-49 92:109
-48 90:107
-47 87:105
-46 87:105
-45 85:100
-44 78:78 82:98
-43 77:97
-42 77:93
-41 77:92
-40 75:90
-39 73:88
-38 73:77 82:83
-37 70:77
-36 68:77
-35 66:75
-34 66:70
-33 63:68
-32 58:59 61:61 63:66
-31 58:65
-30 57:61
-29 57:60
-28 57:58
"""

# Each certificate supplies dimensions and the frame of paper cell ROOT.
# Frame = (doubled physical center, paper-right unit vector, paper-up unit vector).
ROOT = (57, -30)
CASES = [((2, 4, 176), ((0, 3, 121), (0, 0, -1), (0, -1, 0))), ((4, 8, 86), ((0, 1, 55), (0, -1, 0), (0, 0, -1))), ((4, 14, 56), ((0, 9, 1), (0, 0, -1), (0, 1, 0))), ((4, 16, 50), ((0, 1, 9), (0, -1, 0), (0, 0, 1))), ((4, 26, 32), ((3, 0, 15), (0, 0, 1), (-1, 0, 0)))]
CANONICAL_SHA256 = "1c42ebccb47d7236cd757325570c3fe7023b38486c9aa18ef7b78a18e86af8ef"
DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def add(*vectors):
    return tuple(sum(v[k] for v in vectors) for k in range(3))

def mul(s, v):
    return tuple(s * a for a in v)

cells = set()
for line in ROWS.strip().splitlines():
    fields = line.split()
    y = int(fields[0])
    for interval in fields[1:]:
        lo, hi = map(int, interval.split(':'))
        require(lo <= hi, 'Reversed interval')
        for x in range(lo, hi + 1):
            require((x, y) not in cells, 'Duplicate square')
            cells.add((x, y))
require(len(cells) == 2128 and ROOT in cells, 'Wrong paper area or root')
canonical = ';'.join(f'{x},{y}' for x, y in sorted(cells)) + '\n'
require(sha256(canonical.encode('ascii')).hexdigest() == CANONICAL_SHA256,
        'Coordinate certificate has changed')

# Verify that the paper is a simple topological disk.
seen = {ROOT}
order = [ROOT]
for x, y in order:
    for dx, dy in DIRECTIONS:
        q = x + dx, y + dy
        if q in cells and q not in seen:
            seen.add(q)
            order.append(q)
require(seen == cells, 'Disconnected paper')
vertices, edges = set(), set()
for x, y in cells:
    corners = ((x, y), (x+1, y), (x+1, y+1), (x, y+1))
    vertices.update(corners)
    for a, b in zip(corners, corners[1:] + corners[:1]):
        edges.add(tuple(sorted((a, b))))
require(len(vertices) - len(edges) + len(cells) == 1, 'Paper has a hole')
for x, y in vertices:
    occupied = [p in cells for p in ((x-1,y-1), (x,y-1), (x,y), (x-1,y))]
    require(occupied not in ([True,False,True,False], [False,True,False,True]),
            'Paper has a point pinch')

unit_axes = {tuple(sign if k == j else 0 for k in range(3))
             for j in range(3) for sign in (-1, 1)}
require(len({tuple(sorted(d)) for d, frame in CASES}) == 5,
        'Five distinct boxes required')

for dims, root_frame in CASES:
    require(all(isinstance(a, int) and a > 0 for a in dims), 'Invalid dimensions')
    extent = tuple(2*a for a in dims)
    surface = set()
    for normal_axis in range(3):
        tangents = [j for j in range(3) if j != normal_axis]
        for side, a, b in product((0, extent[normal_axis]),
                range(1, extent[tangents[0]], 2),
                range(1, extent[tangents[1]], 2)):
            q = [0, 0, 0]
            q[normal_axis], q[tangents[0]], q[tangents[1]] = side, a, b
            surface.add(tuple(q))
    require(len(surface) == 2128, 'Wrong surface area')

    def valid_frame(frame):
        q, r, u = frame
        require(q in surface and r in unit_axes and u in unit_axes,
                'Invalid physical square or tangent vector')
        require(sum(a*b for a, b in zip(r, u)) == 0, 'Nonorthogonal frame')
        normal_axis = next(i for i in range(3) if q[i] in (0, extent[i]))
        require(r[normal_axis] == u[normal_axis] == 0, 'Nontangent frame')

    def step(frame, dx, dy):
        q, r, u = frame
        movement = add(mul(dx, r), mul(dy, u))
        flat = add(q, mul(2, movement))
        if flat in surface:
            result = flat, r, u
        else:
            axis = next(i for i in range(3) if q[i] in (0, extent[i]))
            normal = tuple((-1 if q[i] == 0 else 1) if i == axis else 0
                           for i in range(3))
            q2 = add(q, movement, mul(-1, normal))
            result = (q2, mul(-dx, normal), u) if dx else (q2, r, mul(-dy, normal))
        valid_frame(result)
        return result

    valid_frame(root_frame)
    assigned = {ROOT: root_frame}
    covered = {root_frame[0]: ROOT}
    joins = 0
    for p in order:
        q, r, u = assigned[p]
        for dx, dy in DIRECTIONS:
            neighbor = p[0] + dx, p[1] + dy
            if neighbor not in cells:
                continue
            frame = step(assigned[p], dx, dy)
            if neighbor in assigned:
                require(assigned[neighbor] == frame, 'Inconsistent paper cycle')
            else:
                require(frame[0] not in covered, 'Two paper squares overlap')
                assigned[neighbor] = frame
                covered[frame[0]] = neighbor
            q2, r2, u2 = assigned[neighbor]
            mid = add(q, mul(dx, r), mul(dy, u))
            mid2 = add(q2, mul(-dx, r2), mul(-dy, u2))
            along, along2 = (u, u2) if dx else (r, r2)
            # Check ordered endpoints, hence pointwise continuity of each join.
            for sign in (-1, 1):
                require(add(mid, mul(sign, along)) == add(mid2, mul(sign, along2)),
                        'Shared paper edge does not match physically')
            joins += 1
    require(len(assigned) == 2128 and set(covered) == surface,
            'Incomplete surface coverage')
    require(joins == 7308, 'Unexpected paper adjacency count')
    print('PASS', 'x'.join(map(str, dims)), ': 2128 surface squares;',
          joins, 'directed paper joins')

# Export the exact net as sorted coordinates and a simple scalable diagram.
out = Path(__file__).resolve().parent
(out / 'fivebox-2128-canonical.cells').write_bytes(canonical.encode('ascii'))
x0, x1 = min(x for x,y in cells), max(x for x,y in cells) + 1
y0, y1 = min(y for x,y in cells), max(y for x,y in cells) + 1
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" '
         f'viewBox="-2 -2 {x1-x0+4} {y1-y0+4}">',
         '<rect x="-2" y="-2" width="100%" height="100%" fill="white"/>']
for x,y in sorted(cells):
    parts.append(f'<rect x="{x-x0}" y="{y1-y-1}" width="1" height="1" '
                 'fill="#e9f1f8" stroke="#506070" stroke-width="0.12"/>')
parts.append('</svg>')
(out / 'fivebox-2128.svg').write_text('\n'.join(parts), encoding='utf-8')
print('VERIFIED: one simple 2128-square net, five distinct positive-volume boxes.')
print('Wrote fivebox-2128-canonical.cells and fivebox-2128.svg')
```
