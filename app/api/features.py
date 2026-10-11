from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Feature
from app.schemas import FeatureCreate, FeatureRead

router = APIRouter()

@router.post("", response_model=FeatureRead, status_code=201)
def create(payload: FeatureCreate, db: Session = Depends(get_db)):
    if payload.external_id:
        existing = db.query(Feature).filter(
            Feature.external_id == payload.external_id).first()
        if existing:
            raise HTTPException(409, "external_id exists")
    f = Feature(**payload.model_dump())
    db.add(f)
    db.commit()
    db.refresh(f)
    return f

@router.get("", response_model=List[FeatureRead])
def list_features(status: Optional[str] = None,
                  epic: Optional[str] = None,
                  limit: int = 200,
                  db: Session = Depends(get_db)):
    q = db.query(Feature)
    if status:
        q = q.filter(Feature.status == status)
    if epic:
        q = q.filter(Feature.epic == epic)
    return q.limit(limit).all()

@router.get("/{feature_id}", response_model=FeatureRead)
def get_one(feature_id: int, db: Session = Depends(get_db)):
    f = db.query(Feature).get(feature_id)
    if not f:
        raise HTTPException(404, "Feature not found")
    return f

@router.patch("/{feature_id}", response_model=FeatureRead)
def update(feature_id: int, payload: dict, db: Session = Depends(get_db)):
    f = db.query(Feature).get(feature_id)
    if not f:
        raise HTTPException(404)
    for k, v in payload.items():
        if hasattr(f, k):
            setattr(f, k, v)
    db.commit()
    db.refresh(f)
    return f

@router.delete("/{feature_id}", status_code=204)
def delete(feature_id: int, db: Session = Depends(get_db)):
    f = db.query(Feature).get(feature_id)
    if not f:
        raise HTTPException(404)
    db.delete(f)
    db.commit()
