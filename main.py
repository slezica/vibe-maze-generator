import random

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
    def generate(self, maze):
        self._add_fence(maze)
        self.generate_inner(maze, 1, 1, maze.width - 2, maze.height - 2)
        self._ensure_entrance_exit(maze)
    
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
        
        self._carve_path(maze, min_x, min_y, min_x, min_y, max_x, max_y)
    
    def _carve_path(self, maze, x, y, min_x, min_y, max_x, max_y):
        maze.grid[y][x] = PATH
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (min_x <= nx <= max_x and min_y <= ny <= max_y and 
                maze.grid[ny][nx] == WALL):
                maze.grid[y + dy // 2][x + dx // 2] = PATH
                self._carve_path(maze, nx, ny, min_x, min_y, max_x, max_y)


class MazeRenderer:
    def render(self, maze):
        raise NotImplementedError("Subclasses must implement render method")


class TextMazeRenderer(MazeRenderer):
    def __init__(self, wall='#', path=' ', step='.'):
        self.wall = wall
        self.path = path
        self.step = step
    
    def render(self, maze):
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == WALL:
                    print(self.wall, end='')
                elif maze.grid[y][x] == STEP:
                    print(self.step, end='')
                else:
                    print(self.path, end='')
            print()


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
    maze = Maze(21, 21)
    generator = RecursiveBacktrackingGenerator()
    renderer = TextMazeRenderer(wall='█')
    solver = MazeSolver()
    
    generator.generate(maze)
    solved_maze = solver.solve(maze)
    renderer.render(solved_maze)
    print()


if __name__ == "__main__":
    main()
