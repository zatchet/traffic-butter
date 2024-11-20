from intersection import StopLight, StopSign
from pos import Pos
from direction import Direction
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any, List

@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)

class RouteFinder:
    def generate_route(self, source: Pos, dest: Pos, grid: List[List[int]]) -> list[Direction]:
        """A* pathfinding algorithm that considers intersection costs"""
        
        def heuristic(pos: Pos) -> float:
            """Manhattan distance heuristic"""
            return abs(dest.x - pos.x) + abs(dest.y - pos.y)
        
        def get_intersection_cost(pos: Pos) -> float:
            """Cost of passing through an intersection"""
            if pos.x <= 0 or pos.y <= 0 or pos.x >= len(grid[0]) or pos.y >= len(grid):
                return float('inf')
            
            intersection = grid[pos.y][pos.x]
            if intersection is None:
                return 1.0  # Base cost for moving one cell
            elif isinstance(intersection, StopLight):
                return 2.0  # Higher cost for traffic lights due to potential waiting
            elif isinstance(intersection, StopSign):
                return 1.5  # Medium cost for stop signs
            return 1.0

        def get_direction(from_pos: Pos, to_pos: Pos) -> Direction:
            """Get the direction enum from one position to another"""
            if to_pos.x > from_pos.x:
                return Direction.right
            elif to_pos.x < from_pos.x:
                return Direction.left
            elif to_pos.y > from_pos.y:
                return Direction.down
            else:
                return Direction.up

        # A* algorithm
        frontier = PriorityQueue()
        frontier.put(PrioritizedItem(0, source))
        came_from = {source: None}
        cost_so_far = {source: 0}
        
        while not frontier.empty():
            current = frontier.get().item
            
            if current == dest:
                break
                
            # Check all four directions
            for direction in Direction:
                dir_vals = direction.math_dirs()
                next_pos = Pos(current.x + dir_vals[0], current.y + dir_vals[1])
                
                # Skip if out of bounds
                if (next_pos.x <= 0 or next_pos.y <= 0 or 
                    next_pos.x >= len(grid[0]) or next_pos.y >= len(grid)):
                    continue
                
                new_cost = cost_so_far[current] + get_intersection_cost(next_pos)
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(next_pos)
                    frontier.put(PrioritizedItem(priority, next_pos))
                    came_from[next_pos] = current
        
        # Reconstruct path
        current = dest
        path = []
        while current != source:
            prev = came_from[current]
            path.append(get_direction(prev, current))
            current = prev
        path.reverse()

        return path