# Maze Generator

A command-line maze generator and solver supporting multiple algorithms. This project was entirely
vibe-coded with Claude - not a single line is human-written.

## Usage

```bash
python main.py [-g|--generator {kruskal|prim|rbt}] [-s|--solve]
```

## Options

- `-g, --generator`: Choose algorithm (default: `rbt`)
  - `rbt`: Recursive Backtracking - long winding paths
  - `kruskal`: Kruskal's Algorithm - branched structure  
  - `prim`: Prim's Algorithm - tree-like growth
- `-s, --solve`: Show solution path with Unicode line graphics

## Examples

```bash
# Generate basic maze with recursive backtracking
python main.py

# Generate and solve with Kruskal's algorithm
python main.py -g kruskal -s

# Generate unsolved maze with Prim's algorithm
python main.py --generator prim
```