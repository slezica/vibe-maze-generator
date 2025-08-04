# Maze Generator

A command-line maze generator and solver supporting multiple algorithms. This project was entirely
vibe-coded with Claude - not a single line is human-written.

## Usage

```bash
python main.py [-g|--generator {kruskal|prim|rbt}] [-s|--solve] [--animate] [--width N] [--height N]
```

## Options

- `-g, --generator`: Choose algorithm (default: `rbt`)
  - `rbt`: Recursive Backtracking - long winding paths
  - `kruskal`: Kruskal's Algorithm - branched structure  
  - `prim`: Prim's Algorithm - tree-like growth
- `-s, --solve`: Show solution path with Unicode line graphics
- `--animate`: Watch maze generation in real-time
- `--width`: Maze width (min: 3, default: 15)
- `--height`: Maze height (min: 3, default: 15)

## Examples

```bash
# Generate basic 15x15 maze with recursive backtracking
python main.py

# Generate and solve with Kruskal's algorithm
python main.py -g kruskal -s

# Watch Prim's algorithm generate a custom-sized maze
python main.py --generator prim --animate --width 25 --height 20

# Generate large animated maze with solution
python main.py --animate -s --width 30 --height 15
```