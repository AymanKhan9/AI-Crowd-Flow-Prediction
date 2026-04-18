import os
import json
import asyncio
from typing import Dict, AsyncGenerator
import redis.asyncio as aioredis
import redis as sync_redis

# MOCK GCP PUB/SUB IMPLEMENTATION USING REDIS FOR LOCAL TESTING
# In production, this would use google.cloud.pubsub_v1.SubscriberClient

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
r_sync = sync_redis.Redis(host=REDIS_HOST, port=6379, db=0)

def get_current_densities() -> Dict[str, float]:
    """Fetch current densities synchronously."""
    from graph_engine.stadium_graph import ZONES
    densities = {}
    for zone in ZONES:
        d_val = r_sync.get(f"zone:{zone}")
        densities[zone] = float(d_val) if d_val else 0.0
    return densities

async def subscribe_to_density_updates() -> AsyncGenerator[str, None]:
    """Async generator that yields messages from Pub/Sub (Mocked via Redis)."""
    r_async = aioredis.Redis(host=REDIS_HOST, port=6379, db=0)
    pubsub = r_async.pubsub()
    await pubsub.subscribe("density_updates")
    
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"].decode("utf-8")
                yield data
    finally:
        await pubsub.unsubscribe()
        await pubsub.close()
