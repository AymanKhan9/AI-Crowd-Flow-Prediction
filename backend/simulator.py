import redis
import time
import random
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=REDIS_HOST, port=6379, db=0)

ZONES = ["Gate_A", "Gate_B", "Section_1", "Section_2", "Food_Court", "Washroom", "Exit"]

# Initial densities
densities = {zone: random.uniform(0.1, 0.3) for zone in ZONES}
# Rate of change
velocities = {zone: 0.0 for zone in ZONES}

def simulate():
    print("Starting Next-Level YOLO Simulation...")
    tick = 0
    while True:
        tick += 1
        
        # Force a major imbalance every 20 ticks to trigger Incentivization
        if tick % 20 == 0:
            print("SIMULATION: Forcing crowd imbalance at Gate_A!")
            densities["Gate_A"] = 0.95
            densities["Gate_B"] = 0.10
        
        updates = {}
        for zone in ZONES:
            # Simulate random velocity change
            accel = random.uniform(-0.05, 0.05)
            velocities[zone] += accel
            
            # Dampen velocity so it doesn't run away
            velocities[zone] *= 0.8
            
            # Update density based on velocity
            densities[zone] = max(0.0, min(1.0, densities[zone] + velocities[zone]))
            
            # Save to redis
            r.set(f"zone:{zone}", densities[zone])
            r.set(f"velocity:{zone}", velocities[zone])
            
            updates[zone] = {"density": densities[zone], "velocity": velocities[zone]}
            
        # Publish update payload via Pub/Sub
        r.publish("density_updates", json.dumps(updates))
        # print(f"Published updates tick {tick}")
        
        # Simulate Virtual Queue Wait Times
        food_queue = r.llen("queue:Food_Court")
        washroom_queue = r.llen("queue:Washroom")
        # Save estimated wait time based on queue length + density
        r.set("waittime:Food_Court", food_queue * 2 + int(densities["Food_Court"] * 10))
        r.set("waittime:Washroom", washroom_queue * 1.5 + int(densities["Washroom"] * 5))
        
        time.sleep(2)

if __name__ == "__main__":
    while True:
        try:
            r.ping()
            break
        except redis.ConnectionError:
            print("Waiting for redis...")
            time.sleep(1)
            
    # Clear queues on restart
    r.delete("queue:Food_Court")
    r.delete("queue:Washroom")
            
    simulate()
