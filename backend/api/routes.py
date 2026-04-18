import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any

from graph_engine.stadium_graph import get_base_graph, apply_zone_closures, ZONES, EXITS
from graph_engine.dijkstra import dijkstra_shortest_path
from predictor.vertex_client import predict_density
from services.pubsub_client import get_current_densities

router = APIRouter()

class RouteRequest(BaseModel):
    start: str
    end: str
    accessibility: bool = False
    emergency: bool = False
    closed_zones: List[str] = []

@router.get("/zones")
def get_zones():
    return {"zones": ZONES}

@router.get("/heatmap")
async def get_heatmap():
    densities = get_current_densities()
    
    # Use Vertex AI predictor to get T+5 predictions
    predicted_densities = await predict_density(densities, steps_ahead=5)
    
    # INCENTIVIZATION ENGINE
    incentives = []
    if densities.get("Gate_A", 0) > 0.8 and densities.get("Gate_B", 1) < 0.3:
        incentives.append({
            "id": "imbalance_gate_b",
            "message": "Gate A is congested! Use Gate B right now and get a 10% discount on drinks!",
            "target_node": "Gate_B",
            "type": "discount"
        })
        
    return {
        "current_densities": densities,
        "predicted_densities": predicted_densities,
        "incentives": incentives
    }

@router.post("/best-route")
async def get_best_route(req: RouteRequest):
    if req.start not in ZONES:
        raise HTTPException(status_code=400, detail="Invalid start zone")
        
    if not req.emergency and req.end not in ZONES:
        raise HTTPException(status_code=400, detail="Invalid end zone")

    # 1. Get current real-time state from PubSub/Redis
    current_densities = get_current_densities()
    
    # 2. Get predictions from Vertex AI (LSTM)
    predicted_densities = await predict_density(current_densities, steps_ahead=5)
    
    # 3. Construct Graph with What-If Closures and Accessibility
    base_graph = get_base_graph(accessibility=req.accessibility)
    final_graph = apply_zone_closures(base_graph, closed_zones=req.closed_zones)
    
    # 4. Route Calculation
    path, cost = dijkstra_shortest_path(
        graph=final_graph, 
        start=req.start, 
        end=req.end, 
        predicted_densities=predicted_densities, 
        is_emergency=req.emergency,
        exits=EXITS
    )
    
    if path is None:
        raise HTTPException(status_code=404, detail="Path not found (possibly due to closures)")
        
    return {
        "path": path,
        "cost": round(cost, 2),
        "predicted_densities_used": {node: predicted_densities.get(node, 0.0) for node in path},
        "is_emergency": req.emergency,
        "is_accessible": req.accessibility,
        "closed_zones": req.closed_zones
    }
