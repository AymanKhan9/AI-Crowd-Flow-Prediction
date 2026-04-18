import pytest
from graph_engine.dijkstra import dijkstra_shortest_path, calculate_dynamic_weight
from graph_engine.stadium_graph import STADIUM_GRAPH, get_base_graph, apply_zone_closures

def test_calculate_dynamic_weight():
    # Base weight 10, predicted density 0.5, penalty factor 10
    # Expected: 10 * (1 + 0.5 * 10) = 10 * (1 + 5) = 60
    weight = calculate_dynamic_weight(10.0, 0.5)
    assert weight == 60.0

def test_dijkstra_normal_routing():
    predicted_densities = {"Section_1": 0.1, "Food_Court": 0.9}
    
    # Given density, going via Food_Court should be heavily penalized
    path, cost = dijkstra_shortest_path(
        graph=STADIUM_GRAPH,
        start="Gate_A",
        end="Washroom",
        predicted_densities=predicted_densities,
        is_emergency=False
    )
    
    assert path is not None
    # Path should avoid Food_Court (which is dense)
    assert "Food_Court" not in path
    assert "Section_1" in path

def test_apply_zone_closures():
    base = get_base_graph()
    closed = apply_zone_closures(base, ["Food_Court"])
    
    assert "Food_Court" not in closed
    assert "Food_Court" not in closed["Gate_A"]

def test_dijkstra_emergency_routing():
    predicted_densities = {"Exit": 0.1, "Gate_A": 0.99} # Gate A blocked
    
    # In emergency, should route to closest non-blocked exit
    path, cost = dijkstra_shortest_path(
        graph=STADIUM_GRAPH,
        start="Section_1",
        end="Food_Court", # Ignored in emergency
        predicted_densities=predicted_densities,
        is_emergency=True,
        exits=["Exit", "Gate_A", "Gate_B"]
    )
    
    assert path is not None
    assert path[-1] in ["Exit", "Gate_A", "Gate_B"]
    assert path[-1] != "Gate_A" # Avoids blocked exit
