# Graph Report - /home/aymankhan/Desktop/projects/AI-Crowd-Flow-Prediction  (2026-04-18)

## Corpus Check
- 7 files · ~6,249 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 29 nodes · 27 edges · 11 communities detected
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]

## God Nodes (most connected - your core abstractions)
1. `ConnectionManager` - 5 edges
2. `websocket_endpoint()` - 4 edges
3. `dijkstra_shortest_path()` - 4 edges
4. `get_current_state()` - 3 edges
5. `get_best_route()` - 3 edges
6. `calculate_dynamic_weight()` - 3 edges
7. `get_heatmap()` - 2 edges
8. `JoinQueueRequest` - 2 edges
9. `Calculate dynamic edge weight based on the destination node's crowd density and` - 1 edges
10. `Find the shortest path considering real-time node densities and emergency mode.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `get_best_route()` --calls--> `dijkstra_shortest_path()`  [INFERRED]
  /home/aymankhan/Desktop/projects/AI-Crowd-Flow-Prediction/backend/main.py → /home/aymankhan/Desktop/projects/AI-Crowd-Flow-Prediction/backend/graph_engine.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.38
Nodes (3): get_best_route(), get_current_state(), get_heatmap()

### Community 1 - "Community 1"
Cohesion: 0.47
Nodes (2): ConnectionManager, websocket_endpoint()

### Community 2 - "Community 2"
Cohesion: 0.5
Nodes (4): calculate_dynamic_weight(), dijkstra_shortest_path(), Calculate dynamic edge weight based on the destination node's crowd density and, Find the shortest path considering real-time node densities and emergency mode.

### Community 3 - "Community 3"
Cohesion: 1.0
Nodes (2): BaseModel, JoinQueueRequest

### Community 4 - "Community 4"
Cohesion: 1.0
Nodes (0): 

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (0): 

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (0): 

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (0): 

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (0): 

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): Calculate dynamic edge weight based on the destination node's crowd density.

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Find the shortest path from start to end considering real-time node densities.

## Knowledge Gaps
- **4 isolated node(s):** `Calculate dynamic edge weight based on the destination node's crowd density and`, `Find the shortest path considering real-time node densities and emergency mode.`, `Calculate dynamic edge weight based on the destination node's crowd density.`, `Find the shortest path from start to end considering real-time node densities.`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 3`** (2 nodes): `BaseModel`, `JoinQueueRequest`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 4`** (2 nodes): `simulator.py`, `simulate()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (2 nodes): `App()`, `App.jsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 6`** (1 nodes): `vite.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (1 nodes): `eslint.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (1 nodes): `main.jsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (1 nodes): `Calculate dynamic edge weight based on the destination node's crowd density.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `Find the shortest path from start to end considering real-time node densities.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_best_route()` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.185) - this node is a cross-community bridge._
- **Why does `dijkstra_shortest_path()` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Why does `ConnectionManager` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **What connects `Calculate dynamic edge weight based on the destination node's crowd density and`, `Find the shortest path considering real-time node densities and emergency mode.`, `Calculate dynamic edge weight based on the destination node's crowd density.` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._