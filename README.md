# IART

## Dependencies

[PyPNG](https://github.com/drj11/pypng)

## Details

### Building

- **H** rows and **W** collumns
- Coords [r, c], starting at 0
- [0, 0] is the upper left corner of the grid
- wall is **'#'**
- target is **'.'** - these cells need wireless coverage
- void is **'-'** - these cells don't need wireless coverage

### Routers

- Each router covers at most (2 \* R + 1)^2 cells around itself, where **R** is
  the router's range.
- Signals are stopped by walls
- If a router is placed at [a, b], the cell [x, y] is covered if:
  - |a - x| <= R,
  - |b - y| <= R,
  - there is no wall [w, v] where min(a, x) <= w <= max(a, x) &&
    min(b, y) <= v <= max(b, y)
  - described as: there are no walls in the smallest enclosing rectangle
    of [a, b] and [x, y]

```txt
R = 3

.#...ooo........
.#...ooo#.......
.####ooo#.......
....#ooSooo.....
....#oooooo.....
....#ooo#.......
....#ooo#.......
```

### Backbone

- Routers can only be placed in cells connected to the backbone.
- In the beginning only **1 cell** is connected to the backbone.
- Cells of any type can be connected to the backbone (one of its eight
  neighboring cells must already be connected to the backbone).

### Budget

- Placing a router costs **Pr**
- Connecting a cell to the backbone costs **Pb**
- The maximum budget is **B**

## Input

- First line
  - (1 <= **H** <= 1000) - number of rows on the grid
  - (1 <= **W** <= 1000) - number of columns on the grid
  - (1 <= **R** <= 10) - radius of a router range
- Second line
  - (1 <= **Pb** <= 5) - price of connecting one cell to the backbone
  - (5 <= **Pr** <= 100) - price of one wireless router
  - (1 <= **B** <= 10^9) - maximum budget
- Third line
  - (0 <= **br** < H) - row of the initial cell connected to the backbone
  - (0 <= **bc** < W) - column of the initial cell connected to the backbone
- Next **H** lines
  - **W** characters specifying the type of each cell (**'#'**, **'.'**, **'-'**)

## Authors

- Ana Inês Oliveira de Barros, up201806593@fe.up.pt
- João de Jesus Costa, up201806560@fe.up.pt
- João Lucas Silva Martins, up201806436@fe.up.pt
