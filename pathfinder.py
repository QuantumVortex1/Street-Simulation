"""
This file contains the algorithm for finding paths from a to b.
The algorithm was tested on the bad_mergendheim map and needed ca. 0.13 sec for 8 calculations.
Therefore it should be considered as fast enough until we got serious performance issues.
"""
from map_handler import map
from collections import deque

def find(start, goal):
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]

    # define a set for the visited fields
    visited = set()
    visited.add(start)
    # the queue for the current position and the used path
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path + [current]

        x, y = current
        for i in range(4):
            new_x = x + dx[i]
            new_y = y + dy[i]
            new_pos = (new_x, new_y)
            if (x, y) in map.street_positions and new_pos not in visited:
                visited.add(new_pos)
                queue.append((new_pos, path + [current]))

    # if no path is found, return none
    return None
