import pygame
from queue import  PriorityQueue

DIS_ACCURACY = 100

def dis(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dis = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return int(dis * DIS_ACCURACY)

def a_star(win, grid):
    time_stamp = 0
    open_queue = PriorityQueue()
    open_queue.put((0, time_stamp, grid.start))
    came_from = {}
    g_cost = {box: float("inf") for row in grid.boxes for box in row}
    g_cost[grid.start] = 0
    f_cost = {box: float("inf") for row in grid.boxes for box in row}
    f_cost[grid.start] = dis(grid.start.get_pos(), grid.end.get_pos())
    open_set = {grid.start}

    while not open_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_queue.get()[2]
        open_set.discard(current)

        if current == grid.end:
            grid.end.set_end()
            grid.construct_path(win, came_from)
            return True

        for neighbor in current.neighbors:
            temp_g_cost = g_cost[current] + dis(neighbor.get_pos(),
                                                current.get_pos())

            if temp_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + dis(neighbor.get_pos(), 
                                                     grid.end.get_pos())

                if neighbor not in open_set:
                    time_stamp += 1
                    open_queue.put((f_cost[neighbor], time_stamp, neighbor))
                    open_set.add(neighbor)
                    neighbor.set_open()
        
        grid.draw(win)

        if current != grid.start:
            current.set_closed()

    return False