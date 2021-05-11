def heuristic_manhattan(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def g_manhattan():
    return 1

def heuristic_pythagorean(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dis = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return int(dis * 10)

def g_pythagorean():
    return 10