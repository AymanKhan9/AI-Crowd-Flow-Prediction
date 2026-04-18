import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes import router as api_router
from api.websockets import router as ws_router

# Ensure necessary environment variables are set for GCP
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/key.json"

app = FastAPI(title="Production AI Crowd Flow Prediction")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(api_router)
app.include_router(ws_router)

@app.on_event("startup")
async def startup_event():
    print("Starting up GCP services...")
    # Initialize Vertex AI client here in production
    # Initialize Pub/Sub listeners here in production

@app.get("/")
def health_check():
    return {"status": "ok", "service": "crowd-flow-api"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
