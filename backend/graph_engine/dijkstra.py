import heapq
from typing import Dict, List, Tuple, Optional

PENALTY_FACTOR = 10.0 # Multiplier for density to heavily penalize crowded areas
PREDICTION_AHEAD_TIME = 5.0 # Minutes into the future to predict

def calculate_dynamic_weight(base_distance: float, predicted_density: float) -> float:
    """
    Calculate dynamic edge weight based on the destination node's predicted crowd density.
    density: value between 0.0 and 1.0.
    """
    # Predictive Analytics: use the provided predicted density directly
    clamped_density = max(0.0, min(1.0, predicted_density))
    return base_distance * (1 + (clamped_density * PENALTY_FACTOR))

def dijkstra_shortest_path(
    graph: Dict[str, Dict[str, float]], 
    start: str, 
    end: str, 
    predicted_densities: Dict[str, float], 
    is_emergency: bool = False,
    exits: Optional[List[str]] = None
) -> Tuple[Optional[List[str]], float]:
    """
    Find the shortest path considering predicted node densities and emergency mode.
    """
    if start not in graph:
        return None, float('inf')
        
    if not is_emergency and end not in graph:
        return None, float('inf')

    # If emergency, we find the shortest path to ANY of the EXITS
    target_nodes = exits if is_emergency and exits else [end]

    pq = [(0.0, start, [start])]
    visited = set()
    dist = {node: float('inf') for node in graph}
    dist[start] = 0.0

    while pq:
        curr_dist, node, path = heapq.heappop(pq)
        
        if node in target_nodes:
            return path, curr_dist
            
        if node in visited:
            continue
            
        visited.add(node)

        for neighbor, base_weight in graph[node].items():
            if neighbor in visited:
                continue
                
            predicted_density = predicted_densities.get(neighbor, 0.0)
            
            # In emergency mode, ignore minor density penalties, just GTFO fast
            # But still avoid completely blocked areas (density > 0.95)
            if is_emergency:
                if predicted_density > 0.95:
                    dynamic_weight = float('inf') # Blocked path
                else:
                    dynamic_weight = base_weight # Raw distance is prioritized
            else:
                dynamic_weight = calculate_dynamic_weight(base_weight, predicted_density)
            
            new_dist = curr_dist + dynamic_weight
            
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))

    return None, float('inf')
