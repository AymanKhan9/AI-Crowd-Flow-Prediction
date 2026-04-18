from typing import Dict, List, Set, Optional

# Standard Stadium layout graph definition
STADIUM_GRAPH: Dict[str, Dict[str, float]] = {
    "Gate_A": {"Section_1": 5, "Food_Court": 8},
    "Gate_B": {"Section_2": 5, "Food_Court": 7},
    "Section_1": {"Gate_A": 5, "Washroom": 4, "Section_2": 6, "Exit": 12},
    "Section_2": {"Gate_B": 5, "Section_1": 6, "Washroom": 5, "Exit": 10},
    "Food_Court": {"Gate_A": 8, "Gate_B": 7, "Washroom": 3},
    "Washroom": {"Food_Court": 3, "Section_1": 4, "Section_2": 5},
    "Exit": {"Section_1": 12, "Section_2": 10}
}

# Accessibility Graph (e.g., stairs removed between Gate_A and Section_1, forced to go around)
ACCESSIBLE_GRAPH: Dict[str, Dict[str, float]] = {
    "Gate_A": {"Food_Court": 8}, # Removed Section_1 direct stair access
    "Gate_B": {"Food_Court": 7}, # Removed Section_2 direct stair access
    "Section_1": {"Washroom": 4, "Section_2": 6, "Exit": 12},
    "Section_2": {"Section_1": 6, "Washroom": 5, "Exit": 10},
    "Food_Court": {"Gate_A": 8, "Gate_B": 7, "Washroom": 3},
    "Washroom": {"Food_Court": 3, "Section_1": 4, "Section_2": 5},
    "Exit": {"Section_1": 12, "Section_2": 10}
}

ZONES: List[str] = list(STADIUM_GRAPH.keys())
EXITS: List[str] = ["Exit", "Gate_A", "Gate_B"] # In emergency, gates become exits too

def get_base_graph(accessibility: bool = False) -> Dict[str, Dict[str, float]]:
    """Returns a deep copy of the base graph depending on accessibility mode."""
    graph_to_use = ACCESSIBLE_GRAPH if accessibility else STADIUM_GRAPH
    return {node: edges.copy() for node, edges in graph_to_use.items()}

def apply_zone_closures(graph: Dict[str, Dict[str, float]], closed_zones: List[str]) -> Dict[str, Dict[str, float]]:
    """
    Applies 'What-If' closures by removing closed zones and their edges from the graph.
    """
    if not closed_zones:
        return graph
        
    modified_graph = {}
    for node, edges in graph.items():
        if node in closed_zones:
            continue
        modified_graph[node] = {neighbor: weight for neighbor, weight in edges.items() if neighbor not in closed_zones}
        
    return modified_graph
