from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import features, prioritization, simulation, integrations

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Roadmap AI", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(features.router, prefix="/api/features", tags=["features"])
app.include_router(prioritization.router, prefix="/api/prioritize", tags=["prioritize"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["simulation"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["integrations"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "product-roadmap-ai"}
