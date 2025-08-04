# maze [-g|--generator kruskal|prim|rbt] [-s|--solve] [--width N] [--height N] - Generate and solve mazes using various algorithms

import random
import argparse

WALL = 0
PATH = 1
STEP = 2


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[PATH for _ in range(width)] for _ in range(height)]
        self.entrance = (1, 0)
        self.exit = (width - 2, height - 1)


class MazeGenerator:
    def generate(self, width, height):
        *_, final_maze = self.igenerate(width, height)
        return final_maze
    
    def igenerate(self, width, height):
        maze = Maze(width, height)
        self._add_fence(maze)
        yield from self.generate_inner(maze, 1, 1, maze.width - 2, maze.height - 2)
        self._ensure_entrance_exit(maze)
        yield maze
    
    def generate_inner(self, maze, min_x, min_y, max_x, max_y):
        raise NotImplementedError("Subclasses must implement generate_inner method")
    
    def _ensure_entrance_exit(self, maze):
        entrance_x, entrance_y = maze.entrance
        exit_x, exit_y = maze.exit
        maze.grid[entrance_y][entrance_x] = PATH
        maze.grid[exit_y][exit_x] = PATH
        
        self._connect_to_maze(maze, entrance_x, entrance_y)
        self._connect_to_maze(maze, exit_x, exit_y)
    
    def _connect_to_maze(self, maze, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < maze.width and 0 <= ny < maze.height and 
                maze.grid[ny][nx] == PATH):
                return
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 < nx < maze.width - 1 and 0 < ny < maze.height - 1):
                maze.grid[ny][nx] = PATH
                break
    
    def _add_fence(self, maze):
        for x in range(maze.width):
            maze.grid[0][x] = WALL
            maze.grid[maze.height - 1][x] = WALL
        
        for y in range(maze.height):
            maze.grid[y][0] = WALL
            maze.grid[y][maze.width - 1] = WALL


class RecursiveBacktrackingGenerator(MazeGenerator):
    def generate_inner(self, maze, min_x, min_y, max_x, max_y):
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                maze.grid[y][x] = WALL
        
        yield from self._carve_path(maze, min_x, min_y, min_x, min_y, max_x, max_y)
    
    def _carve_path(self, maze, x, y, min_x, min_y, max_x, max_y):
        maze.grid[y][x] = PATH
        yield maze
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (min_x <= nx <= max_x and min_y <= ny <= max_y and 
                maze.grid[ny][nx] == WALL):
                maze.grid[y + dy // 2][x + dx // 2] = PATH
                yield maze
                yield from self._carve_path(maze, nx, ny, min_x, min_y, max_x, max_y)


class KruskalGenerator(MazeGenerator):
    def generate_inner(self, maze, min_x, min_y, max_x, max_y):
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                maze.grid[y][x] = WALL
        
        cells = []
        for y in range(min_y, max_y + 1, 2):
            for x in range(min_x, max_x + 1, 2):
                cells.append((x, y))
                maze.grid[y][x] = PATH
        
        yield maze
        
        parent = {}
        for cell in cells:
            parent[cell] = cell
        
        def find(cell):
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]
        
        def union(cell1, cell2):
            root1, root2 = find(cell1), find(cell2)
            if root1 != root2:
                parent[root1] = root2
                return True
            return False
        
        walls = []
        for y in range(min_y, max_y + 1, 2):
            for x in range(min_x, max_x + 1, 2):
                if x + 2 <= max_x:
                    walls.append(((x, y), (x + 2, y)))
                if y + 2 <= max_y:
                    walls.append(((x, y), (x, y + 2)))
        
        random.shuffle(walls)
        
        for (x1, y1), (x2, y2) in walls:
            if union((x1, y1), (x2, y2)):
                wall_x, wall_y = (x1 + x2) // 2, (y1 + y2) // 2
                maze.grid[wall_y][wall_x] = PATH
                yield maze


class PrimGenerator(MazeGenerator):
    def generate_inner(self, maze, min_x, min_y, max_x, max_y):
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                maze.grid[y][x] = WALL
        
        start_x, start_y = min_x, min_y
        maze.grid[start_y][start_x] = PATH
        yield maze
        
        frontier = []
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            nx, ny = start_x + dx, start_y + dy
            if min_x <= nx <= max_x and min_y <= ny <= max_y:
                frontier.append((nx, ny, start_x, start_y))
        
        while frontier:
            fx, fy, px, py = random.choice(frontier)
            frontier.remove((fx, fy, px, py))
            
            if maze.grid[fy][fx] == WALL:
                maze.grid[fy][fx] = PATH
                maze.grid[(fy + py) // 2][(fx + px) // 2] = PATH
                yield maze
                
                for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                    nx, ny = fx + dx, fy + dy
                    if (min_x <= nx <= max_x and min_y <= ny <= max_y and
                        maze.grid[ny][nx] == WALL):
                        frontier.append((nx, ny, fx, fy))


class MazeRenderer:
    def render(self, maze):
        raise NotImplementedError("Subclasses must implement render method")


class TextMazeRenderer(MazeRenderer):
    def __init__(self, wall='#', path=' ', step='●'):
        self.wall = wall
        self.path = path
        self.step = step
    
    def render(self, maze):
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == WALL:
                    print(self.wall * 2, end='')
                elif maze.grid[y][x] == STEP:
                    print(self._get_step_char(maze, x, y), end='')
                else:
                    print(self.path * 2, end='')
            print()
    
    def _get_step_char(self, maze, x, y):
        left = x > 0 and maze.grid[y][x-1] == STEP
        right = x < maze.width-1 and maze.grid[y][x+1] == STEP  
        up = y > 0 and maze.grid[y-1][x] == STEP
        down = y < maze.height-1 and maze.grid[y+1][x] == STEP
        
        if (left or right) and not (up or down):
            return '──'
        elif (up or down) and not (left or right):
            return '│ '
        elif up and right:
            return '└─'
        elif up and left:
            return '┘ '
        elif down and right:
            return '┌─'
        elif down and left:
            return '┐ '
        else:
            return self.step + ' '


class MazeSolver:
    def solve(self, maze):
        import copy
        solved_maze = copy.deepcopy(maze)
        
        start_x, start_y = maze.entrance
        end_x, end_y = maze.exit
        
        path = self._find_path(maze, start_x, start_y, end_x, end_y)
        
        if path:
            for x, y in path:
                solved_maze.grid[y][x] = STEP
        
        return solved_maze
    
    def _find_path(self, maze, start_x, start_y, end_x, end_y):
        visited = set()
        stack = [(start_x, start_y, [(start_x, start_y)])]
        
        while stack:
            x, y, path = stack.pop()
            
            if (x, y) in visited:
                continue
            
            visited.add((x, y))
            
            if x == end_x and y == end_y:
                return path
            
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < maze.width and 0 <= ny < maze.height and
                    (nx, ny) not in visited and
                    maze.grid[ny][nx] != WALL):
                    stack.append((nx, ny, path + [(nx, ny)]))
        
        return None


def main():
    parser = argparse.ArgumentParser(description='Generate and optionally solve mazes')
    parser.add_argument('-g', '--generator', 
                       choices=['kruskal', 'prim', 'rbt'], 
                       default='rbt',
                       help='Maze generation algorithm (default: rbt)')
    parser.add_argument('-s', '--solve', 
                       action='store_true',
                       help='Show solution path')
    parser.add_argument('--width',
                       type=int,
                       default=20,
                       help='Maze width (min: 3, default: 20)')
    parser.add_argument('--height',
                       type=int,
                       default=20,
                       help='Maze height (min: 3, default: 20)')
    
    args = parser.parse_args()
    
    if args.width < 3:
        parser.error('Width must be at least 3')
    if args.height < 3:
        parser.error('Height must be at least 3')
    
    renderer = TextMazeRenderer(wall='█')
    
    if args.generator == 'kruskal':
        generator = KruskalGenerator()
    elif args.generator == 'prim':
        generator = PrimGenerator()
    else:  # rbt
        generator = RecursiveBacktrackingGenerator()
    
    maze = generator.generate(args.width, args.height)
    
    if args.solve:
        solver = MazeSolver()
        solved_maze = solver.solve(maze)
        renderer.render(solved_maze)
    else:
        renderer.render(maze)


if __name__ == "__main__":
    main()
