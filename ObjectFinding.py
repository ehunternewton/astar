import heapq
from random import randint


class Cell:
    def __init__(self, x, y, reachable):
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


class AStar:
    def __init__(self, grid_size=10, number_of_walls=5):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_size = grid_size
        self.number_of_walls = number_of_walls
        self.grid_height = self.grid_size
        self.grid_width = self.grid_size
        self.start = Cell(0, 0, True)
        self.end = Cell(self.grid_size-1, self.grid_size-1, True)
        self.finalPos = []

    def init_grid(self, startX, startY, targetX, targetY):
        walls = []

        for i in range(self.number_of_walls):
            wallsCoordinate = []
            wallsCoordinate.append(randint(0, self.grid_size-1))
            wallsCoordinate.append(randint(0, self.grid_size - 1))
            walls.append(wallsCoordinate)


        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if [x, y] in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))

        self.start = self.get_cell(startX, startY)
        self.end = self.get_cell(targetX,targetY)


    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.

        @param cell
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.

        @param cell get adjacent cells for this cell
        @returns adjacent cells list
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        # grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        #         [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        #         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]

        path = []
        grid = []
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                if self.cells[self.grid_size * x + y].reachable:
                    row.append('-')
                else:
                    row.append('X')
            grid.append(row)

        cell = self.end
        grid[cell.y][cell.x] = 'T'
        while cell.parent is not self.start:
            cell = cell.parent
            grid[cell.y][cell.x] = 'o'
            print('path: cell: %d,%d' % (cell.x, cell.y))
            path.append([cell.x, cell.y])
        cell = self.start
        grid[cell.y][cell.x] = 'S'
        for row in grid:
            print(row)
        print(" '-': empty cell\n"
              " 'X': unreachable cell: e.g. chair\n"
              " 'T': ending cell\n"
              " 'o': path\n"
              " 'S': start position\n")
        if len(path) > 0:
            self.finalPos = path[0]

    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


size = int(input("Enter map size: "))
obstacles = int(input("Enter number of obstacles: "))
startX = int(input("Enter Starting X Coordinate from 0 to " + str(size-1) + ': '))
startY = int(input("Enter Starting Y Coordinate from 0 to " + str(size-1) + ': '))


for i in range(2):
    n = AStar(grid_size=size, number_of_walls=obstacles)
    targetX = randint(0, size-1)
    targetY = randint(0, size-1)
    n.init_grid(startX=startX, startY=startY,
                targetX=targetX, targetY=targetY)
    n.process()
    print(n.finalPos)
