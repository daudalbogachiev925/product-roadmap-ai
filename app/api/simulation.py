from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Feature, Estimate
from app.schemas import SimulationRequest, SimulationResult, EstimateCreate
from app.core.monte_carlo import simulate

router = APIRouter()

@router.post("/estimate/{feature_id}")
def add_estimate(feature_id: int, payload: EstimateCreate,
                 db: Session = Depends(get_db)):
    f = db.query(Feature).get(feature_id)
    if not f:
        raise HTTPException(404)
    if not (payload.optimistic <= payload.likely <= payload.pessimistic):
        raise HTTPException(400, "optimistic <= likely <= pessimistic required")
    e = Estimate(feature_id=feature_id, **payload.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    return {"id": e.id, "feature_id": e.feature_id}

@router.post("/run", response_model=SimulationResult)
def run_simulation(req: SimulationRequest, db: Session = Depends(get_db)):
    estimates = db.query(Estimate).all()
    if not estimates:
        raise HTTPException(400, "No estimates available")
    result = simulate(estimates, req.velocity_mean, req.velocity_std,
                      req.n_simulations)
    return result
