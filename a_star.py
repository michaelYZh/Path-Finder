import  pygame
from queue import  PriorityQueue
from cost import heuristic_manhattan as h_m
from cost import g_manhattan as g_m
from cost import heuristic_pythagorean as h_p
from cost import g_pythagorean as g_p

SCREEN_DIM = 900
ROWS = 90
BG_COLOR = (255, 255, 255)

INIT_NODE_COLOR = (255, 255, 255)
CLOSED_COLOR = (0, 255, 255)
OPEN_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (0, 0, 0)
START_COLOR = (255, 116, 53)
END_COLOR = (0, 255, 0)
PATH_COLOR = (255, 255, 0)
GRID_LINE_COLOR = (134, 136, 138)

class Box:
    def __init__(self, row, col, dim):
        self.row = row
        self.col = col
        self.x = row * dim
        self.y = col * dim
        self.color = INIT_NODE_COLOR
        self.neighbors = []
        self.dim = dim
    
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == CLOSED_COLOR

    def is_open(self):
        return self.color == OPEN_COLOR
    
    def is_obstacle(self):
        return self.color == OBSTACLE_COLOR

    def is_start(self):
        return self.color == START_COLOR

    def reset(self):
        self.color = INIT_NODE_COLOR
    
    def set_closed(self):
        self.color = CLOSED_COLOR

    def set_open(self):
        self.color = OPEN_COLOR

    def set_obstacle(self):
        self.color = OBSTACLE_COLOR

    def set_start(self):
        self.color = START_COLOR

    def set_end(self):
        self.color = END_COLOR

    def set_path(self):
        self.color = PATH_COLOR

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.dim, self.dim))

    def update_neighbors(self, grid, dis_type = "m"):
        self.neighbors = []
        if self.row < ROWS - 1:
            if not grid[self.row + 1][self.col].is_obstacle():
                self.neighbors.append(grid[self.row + 1][self.col])

            if dis_type == "p":
                if self.col < ROWS - 1 and \
                    not grid[self.row + 1][self.col + 1].is_obstacle():
                    self.neighbors.append(grid[self.row + 1][self.col + 1])
                if self.col > 0 and \
                    not grid[self.row + 1][self.col - 1].is_obstacle():
                    self.neighbors.append(grid[self.row + 1][self.col - 1])
                
        if self.row > 0:
            if not grid[self.row - 1][self.col].is_obstacle():
                self.neighbors.append(grid[self.row - 1][self.col])

            if dis_type == "p":
                if self.col < ROWS - 1 and \
                    not grid[self.row - 1][self.col + 1].is_obstacle():
                    self.neighbors.append(grid[self.row - 1][self.col + 1])
                if self.col > 0 and \
                    not grid[self.row - 1][self.col - 1].is_obstacle():
                    self.neighbors.append(grid[self.row - 1][self.col - 1])

        if self.col < ROWS - 1 and \
            not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])


def make_grid(rows, dim):
    grid = []
    box_dim = dim // rows
    for i in range(rows):
        col = []
        for j in range(rows):
            box = Box(i , j, box_dim)
            col.append(box)
        grid.append(col)

    return grid

def draw_grid_lines(win, rows, dim):
    box_dim = dim // rows
    for i in range(rows + 1):
        pygame.draw.line(win, GRID_LINE_COLOR, (0, i * box_dim), 
                         (dim, i * box_dim))
        pygame.draw.line(win, GRID_LINE_COLOR, (i * box_dim, 0), 
                         (i * box_dim, dim))

def draw_grid(win, grid, rows, dim):
    win.fill(BG_COLOR)

    for row in grid:
        for box in row:
            box.draw(win)

    draw_grid_lines(win, rows, dim)
    pygame.display.update()

def get_clicked_pos(pos, rows, dim):
    box_dim = dim // rows
    y, x = pos

    row = y // box_dim
    col = x // box_dim

    return row, col

def construct_path(came_from, start, end, cur, draw_grid):
    while cur in came_from:
        cur = came_from[cur]
        if cur != start and cur != end:
            cur.set_path()
        draw_grid()

def a_star(draw_grid, grid, start, end, dis_type = "m"):
    time_stamp = 0
    open_set = PriorityQueue()
    open_set.put((0, time_stamp, start)) # (f_cost, time_added, node)
    came_from = {}
    g_cost = {box: float("inf") for row in grid for box in row}
    g_cost[start] = 0
    f_cost = {box: float("inf") for row in grid for box in row}
    if dis_type == "p":
        f_cost[start] = h_p(start.get_pos(), end.get_pos())
    else:
        f_cost[start] = h_m(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            end.set_end()
            construct_path(came_from, start, end, end, draw_grid)
            return True

        for neighbor in current.neighbors:
            temp_g_cost = g_cost[current]

            if dis_type == "p":
                temp_g_cost += g_p()
            else:
                temp_g_cost += g_m()

            if temp_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = temp_g_cost

                if dis_type == "p":
                    f_cost[neighbor] = temp_g_cost + h_p(neighbor.get_pos(), 
                                                         end.get_pos())
                else:
                    f_cost[neighbor] = temp_g_cost + h_m(neighbor.get_pos(), 
                                                         end.get_pos())

                if neighbor not in open_set_hash:
                    time_stamp += 1
                    open_set.put((f_cost[neighbor], time_stamp, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()
        
        draw_grid()

        if current != start:
            current.set_closed()

    return False


def main():
    win = pygame.display.set_mode((SCREEN_DIM, SCREEN_DIM))
    pygame.display.set_caption("Path Finder")
    grid = make_grid(ROWS, SCREEN_DIM)

    start = None
    end = None
    run = True
    while run:
        draw_grid(win, grid, ROWS, SCREEN_DIM)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(mouse_pos, ROWS, SCREEN_DIM)
                box = grid[row][col]

                if not start and box != end:
                    start = box
                    start.set_start()
                elif not end and box != start:
                    end = box
                    end.set_end()
                elif box != start and box != end:
                    box.set_obstacle()

            elif pygame.mouse.get_pressed()[2]:
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(mouse_pos, ROWS, SCREEN_DIM)
                box = grid[row][col]
                box.reset()

                if box == start:
                    start = None
                elif box == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for box in row:
                            box.update_neighbors(grid)
                    
                    a_star(lambda: draw_grid(win, grid, ROWS, SCREEN_DIM), grid,
                           start, end)

                if event.key == pygame.K_RETURN:
                    grid = make_grid(ROWS, SCREEN_DIM)
                    start = None
                    end = None
                    started = False
      
    pygame.quit()

if __name__ == '__main__':
    main()