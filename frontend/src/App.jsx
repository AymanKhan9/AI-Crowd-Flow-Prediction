import { useState, useEffect } from 'react'
import { Map, Navigation, Activity, ChevronRight, Accessibility, AlertTriangle, Users } from 'lucide-react'
import './index.css'

const STADIUM_NODES = {
  Gate_A: { x: 150, y: 150, label: "Gate A" },
  Gate_B: { x: 650, y: 150, label: "Gate B" },
  Food_Court: { x: 400, y: 250, label: "Food Court" },
  Section_1: { x: 200, y: 350, label: "Section 1" },
  Section_2: { x: 600, y: 350, label: "Section 2" },
  Washroom: { x: 400, y: 400, label: "Washroom" },
  Exit: { x: 400, y: 550, label: "Exit" }
};

const STADIUM_EDGES = [
  ["Gate_A", "Section_1"], ["Gate_A", "Food_Court"],
  ["Gate_B", "Section_2"], ["Gate_B", "Food_Court"],
  ["Section_1", "Washroom"], ["Section_1", "Section_2"], ["Section_1", "Exit"],
  ["Section_2", "Washroom"], ["Section_2", "Exit"],
  ["Food_Court", "Washroom"]
];

function App() {
  const [densities, setDensities] = useState({});
  const [velocities, setVelocities] = useState({});
  const [zones, setZones] = useState([]);
  const [incentives, setIncentives] = useState([]);
  
  const [startZone, setStartZone] = useState('Gate_A');
  const [endZone, setEndZone] = useState('Exit');
  const [routeData, setRouteData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // New Toggles
  const [isAccessible, setIsAccessible] = useState(false);
  const [isEmergency, setIsEmergency] = useState(false);

  // Queue State
  const [queueStatus, setQueueStatus] = useState(null);
  const [joinedQueue, setJoinedQueue] = useState(false);
  const [userId] = useState("user_" + Math.floor(Math.random() * 1000));

  useEffect(() => {
    fetch('http://localhost:8000/zones')
      .then(res => res.json())
      .then(data => setZones(data.zones))
      .catch(err => console.error(err));
      
    fetch('http://localhost:8000/heatmap')
      .then(res => res.json())
      .then(data => {
        setDensities(data.densities || {});
        setVelocities(data.velocities || {});
        setIncentives(data.incentives || []);
      })
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/live');
    ws.onmessage = (event) => {
      try {
        const updates = JSON.parse(event.data);
        const newDensities = { ...densities };
        const newVelocities = { ...velocities };
        
        Object.keys(updates).forEach(z => {
          newDensities[z] = updates[z].density;
          newVelocities[z] = updates[z].velocity;
        });
        
        setDensities(newDensities);
        setVelocities(newVelocities);
        
        // Check for incentives continuously in frontend or wait for periodic polling
        // To be safe, we can just poll heatmap every 5s for incentives
      } catch (e) {
        console.error("WS Parse error", e);
      }
    };
    return () => ws.close();
  }, [densities, velocities]);

  // Poll for incentives & queue
  useEffect(() => {
    const interval = setInterval(() => {
      fetch('http://localhost:8000/heatmap')
        .then(res => res.json())
        .then(data => {
          setIncentives(data.incentives || []);
        });

      if (joinedQueue) {
        fetch(`http://localhost:8000/queue/status?zone=Food_Court`)
          .then(res => res.json())
          .then(data => setQueueStatus(data));
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [joinedQueue]);

  useEffect(() => {
    // Automatically recalculate route when toggles change if route exists
    if (routeData || isEmergency) {
      handleRouteRequest();
    }
  }, [isAccessible, isEmergency, startZone, endZone]);

  const handleRouteRequest = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`http://localhost:8000/best-route?start=${startZone}&end=${endZone}&accessibility=${isAccessible}&emergency=${isEmergency}`);
      const data = await res.json();
      if (data.error) setError(data.error);
      else setRouteData(data);
    } catch (err) {
      setError("Failed to connect to server.");
    } finally {
      setLoading(false);
    }
  };

  const handleJoinQueue = async () => {
    const res = await fetch('http://localhost:8000/queue/join', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ zone: "Food_Court", user_id: userId })
    });
    const data = await res.json();
    setJoinedQueue(true);
    setQueueStatus(data);
  };

  const getNodeColor = (density) => {
    if (density === undefined || density === null) return 'rgba(255, 255, 255, 0.2)';
    if (density < 0.3) return 'var(--free-color)';
    if (density < 0.7) return 'var(--medium-color)';
    return 'var(--crowded-color)';
  };

  const isEdgeInRoute = (n1, n2) => {
    if (!routeData || !routeData.path) return false;
    const p = routeData.path;
    for (let i = 0; i < p.length - 1; i++) {
      if ((p[i] === n1 && p[i+1] === n2) || (p[i] === n2 && p[i+1] === n1)) {
        return true;
      }
    }
    return false;
  };

  return (
    <div className={`dashboard-container ${isEmergency ? 'emergency-mode' : ''}`}>
      <header className="header" style={{ position: 'relative' }}>
        <h1 style={isEmergency ? { color: '#ff4444', background: 'none', WebkitTextFillColor: '#ff4444' } : {}}>
          {isEmergency ? 'EMERGENCY EVACUATION ACTIVE' : 'AI Crowd Flow Routing'}
        </h1>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button 
            className={`btn-toggle ${isAccessible ? 'active' : ''}`}
            onClick={() => setIsAccessible(!isAccessible)}
          >
            <Accessibility size={16} /> Accessible Route
          </button>
          <button 
            className={`btn-toggle danger ${isEmergency ? 'active' : ''}`}
            onClick={() => setIsEmergency(!isEmergency)}
          >
            <AlertTriangle size={16} /> EVACUATE
          </button>
        </div>
      </header>

      {/* Incentives Overlay */}
      {incentives.length > 0 && !isEmergency && (
        <div className="incentive-banner">
          🎉 {incentives[0].message}
        </div>
      )}

      {/* Main Map Area */}
      <div className="glass-panel map-container">
        <div className="panel-title">
          <Map size={20} /> Live Stadium Heatmap
        </div>
        
        <div className="stadium-map" style={isEmergency ? { background: 'rgba(255,0,0,0.1)' } : {}}>
          <svg className="map-svg" viewBox="0 0 800 700">
            {STADIUM_EDGES.map((edge, i) => {
              const [n1, n2] = edge;
              
              // If accessible mode is ON, hide the stairs (Gate_A -> Sec_1, Gate_B -> Sec_2)
              if (isAccessible && ((n1==="Gate_A" && n2==="Section_1") || (n1==="Gate_B" && n2==="Section_2") || (n2==="Gate_A" && n1==="Section_1") || (n2==="Gate_B" && n1==="Section_2"))) {
                return null;
              }

              const p1 = STADIUM_NODES[n1];
              const p2 = STADIUM_NODES[n2];
              const isRoute = isEdgeInRoute(n1, n2);
              
              return (
                <line 
                  key={i}
                  x1={p1.x} y1={p1.y} 
                  x2={p2.x} y2={p2.y}
                  className={`map-edge ${isRoute ? 'highlighted' : ''} ${isEmergency && isRoute ? 'emergency' : ''}`}
                />
              );
            })}

            {Object.entries(STADIUM_NODES).map(([nodeKey, pos]) => {
              const density = densities[nodeKey] || 0;
              const velocity = velocities[nodeKey] || 0;
              
              // Predicted color based on future
              const predictedDensity = Math.min(1.0, Math.max(0.0, density + (velocity * 5)));
              const color = isEmergency ? (["Exit", "Gate_A", "Gate_B"].includes(nodeKey) ? '#10b981' : '#444') : getNodeColor(predictedDensity);
              
              const isRouteNode = routeData?.path?.includes(nodeKey);
              
              return (
                <g key={nodeKey} className="map-node">
                  {predictedDensity > 0.7 && !isEmergency && (
                     <circle cx={pos.x} cy={pos.y} r={45} fill={color} opacity="0.2" style={{ animation: 'pulse 2s infinite' }} />
                  )}
                  {/* Arrow indicating trend */}
                  {!isEmergency && velocity > 0.05 && (
                    <text x={pos.x + 35} y={pos.y - 35} fontSize="20" fill="red">↑</text>
                  )}
                  {!isEmergency && velocity < -0.05 && (
                    <text x={pos.x + 35} y={pos.y - 35} fontSize="20" fill="green">↓</text>
                  )}

                  <circle 
                    cx={pos.x} cy={pos.y} 
                    r={30} 
                    fill={color}
                    stroke={isRouteNode ? 'white' : 'transparent'}
                    strokeWidth={isRouteNode ? 4 : 0}
                  />
                  <text x={pos.x} y={pos.y}>{pos.label}</text>
                </g>
              );
            })}
          </svg>
        </div>
      </div>

      {/* Sidebar */}
      <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        
        {/* Routing */}
        <div>
          <div className="panel-title"><Navigation size={20} /> Route Planner</div>
          <div className="form-group">
            <label>You are here:</label>
            <select className="form-control" value={startZone} onChange={e => setStartZone(e.target.value)}>
              {zones.map(z => <option key={z} value={z}>{STADIUM_NODES[z]?.label || z}</option>)}
            </select>
          </div>
          {!isEmergency && (
            <div className="form-group">
              <label>Destination:</label>
              <select className="form-control" value={endZone} onChange={e => setEndZone(e.target.value)}>
                {zones.map(z => <option key={z} value={z}>{STADIUM_NODES[z]?.label || z}</option>)}
              </select>
            </div>
          )}
        </div>

        {routeData && (
          <div className={`route-result ${isEmergency ? 'emergency-bg' : ''}`}>
            <div className="route-title">{isEmergency ? 'EVACUATION ROUTE' : 'Optimal Path (Predictive)'}</div>
            <div className="route-path" style={isEmergency ? {color: '#ff4444'} : {}}>
              {routeData.path.map((node, i) => (
                <span key={i}>
                  {STADIUM_NODES[node]?.label || node}
                  {i < routeData.path.length - 1 && <ChevronRight size={16} style={{ margin: '0 4px', verticalAlign: 'middle', display: 'inline' }} />}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Virtual Queue */}
        {!isEmergency && (
          <div style={{ marginTop: 'auto', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1.5rem' }}>
            <div className="panel-title"><Users size={20} /> Virtual Queue</div>
            {!joinedQueue ? (
              <button className="btn outline" onClick={handleJoinQueue}>Join Food Court Queue</button>
            ) : (
              <div className="queue-status">
                <div className="q-time">{queueStatus?.estimated_wait_minutes || 0} min</div>
                <div className="q-label">Estimated Wait Time ({queueStatus?.people_in_line} ahead of you)</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--accent)', marginTop: '0.5rem' }}>Stay seated. We'll notify you when it's your turn!</div>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  )
}

export default App
