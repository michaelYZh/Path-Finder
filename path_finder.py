import  pygame
from algorithms import ALGO_DICT
from a_star import a_star

SCREEN_DIM = 900
ROWS = 90
BG_COLOR = (255, 255, 255)
MENU_BG_COLOR = (0, 0, 0)
SYSTEM_FONT = "comicsans"
FONT_SIZE = 60
FONT_COLOR = (255, 255, 255)
MENU_Y = 200
MENU_OPT_GAP = 100

INIT_BOX_COLOR = (255, 255, 255)
CLOSED_COLOR = (0, 255, 255)
OPEN_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (0, 0, 0)
START_COLOR = (160,32,240)
END_COLOR = (0, 255, 0)
PATH_COLOR = (255, 255, 0)
GRID_LINE_COLOR = (134, 136, 138)

class Box:
    def __init__(self, row, col, dim):
        self.row = row
        self.col = col
        self.x = row * dim
        self.y = col * dim
        self.color = INIT_BOX_COLOR
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
        self.color = INIT_BOX_COLOR
    
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

    def update_neighbors_diag(self, grid):
        if self.row > 0:
            if self.col > 0:
                if not grid[self.row - 1][self.col - 1].is_obstacle() and \
                   not (grid[self.row][self.col - 1].is_obstacle() and 
                        grid[self.row - 1][self.col].is_obstacle()):
                    self.neighbors.append(grid[self.row - 1][self.col - 1])
            if self.col < ROWS - 1:
                if not grid[self.row - 1][self.col + 1].is_obstacle() and \
                   not (grid[self.row][self.col + 1].is_obstacle() and 
                        grid[self.row - 1][self.col].is_obstacle()):
                    self.neighbors.append(grid[self.row - 1][self.col + 1])

        if self.row < ROWS - 1:
            if self.col > 0:
                if not grid[self.row + 1][self.col - 1].is_obstacle() and \
                   not (grid[self.row][self.col - 1].is_obstacle() and 
                        grid[self.row + 1][self.col].is_obstacle()):
                    self.neighbors.append(grid[self.row + 1][self.col - 1])
            if self.col < ROWS - 1:
                if not grid[self.row + 1][self.col + 1].is_obstacle() and \
                   not (grid[self.row][self.col + 1].is_obstacle() and 
                        grid[self.row + 1][self.col].is_obstacle()):
                    self.neighbors.append(grid[self.row + 1][self.col + 1])  
        
    def update_neighbors(self, grid, diag=True):
        self.neighbors = []
        if self.row < ROWS - 1 and \
            not grid[self.row + 1][self.col].is_obstacle():
                self.neighbors.append(grid[self.row + 1][self.col])
                
        if self.row > 0 and \
            not grid[self.row - 1][self.col].is_obstacle():
                self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < ROWS - 1 and \
            not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])

        if diag:
            self.update_neighbors_diag(grid)

class Grid:
    def __init__(self, rows, dim):
        self.rows = rows
        self.dim = dim
        self.gap = dim // rows
        self.boxes = [[Box(i, j, self.gap) for j in range(rows)] 
                        for i in range(rows)]
        self.start = None
        self.end = None

    def get_clicked_pos(self, pos):
        y, x = pos
        row = y // self.gap
        col = x // self.gap
        return (row, col)

    def draw(self, win):
        win.fill(BG_COLOR)

        for row in self.boxes:
            for box in row:
                box.draw(win)

        for i in range(self.rows + 1):
            pygame.draw.line(win, GRID_LINE_COLOR, (0, i * self.gap), 
                            (self.dim, i * self.gap))
            pygame.draw.line(win, GRID_LINE_COLOR, (i * self.gap, 0), 
                            (i * self.gap, self.dim))

        pygame.display.update()

    def construct_path(self, win, came_from):
        cur = self.end
        while cur in came_from:
            cur = came_from[cur]
            if cur != self.start and cur != self.end:
                cur.set_path()
            self.draw(win)

    def clear_path(self):
        for row in self.boxes:
            for box in row:
                if (box.color == CLOSED_COLOR or box.color == OPEN_COLOR or 
                    box.color == PATH_COLOR):
                    box.reset()
        


def path_finder(win, algo):
    grid = Grid(ROWS, SCREEN_DIM)

    path_drawn = False
    run = True
    while run:
        grid.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if pygame.mouse.get_pressed()[0]:
                if path_drawn:
                    grid.clear_path()

                mouse_pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(mouse_pos)
                box = grid.boxes[row][col]

                if not grid.start and box != grid.end:
                    grid.start = box
                    grid.start.set_start()
                elif not grid.end and box != grid.start:
                    grid.end = box
                    grid.end.set_end()
                elif box != grid.start and box != grid.end:
                    box.set_obstacle()

            elif pygame.mouse.get_pressed()[2]:
                if path_drawn:
                    grid.clear_path()

                mouse_pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(mouse_pos)
                box = grid.boxes[row][col]
                box.reset()

                if box == grid.start:
                    grid.start = None
                elif box == grid.end:
                    grid.end = None

            if event.type == pygame.KEYDOWN:
                if path_drawn:
                    grid.clear_path()

                if event.key == pygame.K_SPACE and grid.start and grid.end:
                    for row in grid.boxes:
                        for box in row:
                            box.update_neighbors(grid.boxes)
                    
                    if algo == ALGO_DICT["A* (pythagorean)"]:
                        a_star(win, grid)
                    path_drawn = True

                elif event.key == pygame.K_RETURN:
                    run = False

                elif event.key == pygame.K_c:
                    grid = Grid(ROWS, SCREEN_DIM)
                    path_drawn = False

def draw_menu(win):
    win.fill(MENU_BG_COLOR)
    font = pygame.font.SysFont(SYSTEM_FONT, FONT_SIZE)

    counter = 0
    for key, value in ALGO_DICT.items():
        instr = "Press '" + value + "' for " + key
        text = font.render(instr, 1, FONT_COLOR)
        win.blit(text, (SCREEN_DIM / 2 - text.get_width() / 2,
                        MENU_Y + counter * MENU_OPT_GAP))
        counter += 1

    pygame.display.update()

def menu():
    pygame.init()
    win = pygame.display.set_mode((SCREEN_DIM, SCREEN_DIM))
    pygame.display.set_caption("Path Finder")

    run = True
    while run:
        draw_menu(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    path_finder(win, ALGO_DICT["A* (pythagorean)"])
                #elif event.key == pygame.K_m:
                #   path_finder(win, ALGO_DICT["A* (manhattan)"])

    pygame.quit()

if __name__ == '__main__':
    menu()