from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Feature
from app.schemas import RiceResult, WsjfResult, KanoResult
from app.core.rice import rank_by_rice
from app.core.wsjf import rank_by_wsjf
from app.core.kano import rank_by_kano, kano_matrix

router = APIRouter()

@router.get("/rice", response_model=List[RiceResult])
def rice(db: Session = Depends(get_db)):
    features = db.query(Feature).filter(Feature.status != "done").all()
    return rank_by_rice(features)

@router.get("/wsjf", response_model=List[WsjfResult])
def wsjf(db: Session = Depends(get_db)):
    features = db.query(Feature).filter(Feature.status != "done").all()
    return rank_by_wsjf(features)

@router.get("/kano", response_model=List[KanoResult])
def kano(db: Session = Depends(get_db)):
    features = db.query(Feature).all()
    return rank_by_kano(features)

@router.get("/kano/matrix")
def kano_mat(db: Session = Depends(get_db)):
    features = db.query(Feature).all()
    return kano_matrix(features)

@router.get("/combined")
def combined(db: Session = Depends(get_db)):
    features = db.query(Feature).filter(Feature.status != "done").all()
    rice_ranked = {r["feature_id"]: i for i, r in enumerate(rank_by_rice(features))}
    wsjf_ranked = {r["feature_id"]: i for i, r in enumerate(rank_by_wsjf(features))}
    kano_ranked = {r["feature_id"]: i for i, r in enumerate(rank_by_kano(features))}
    result = []
    for f in features:
        avg_rank = (rice_ranked.get(f.id, 999) * 0.4
                    + wsjf_ranked.get(f.id, 999) * 0.4
                    + kano_ranked.get(f.id, 999) * 0.2)
        result.append({"feature_id": f.id, "title": f.title,
                       "combined_rank": round(avg_rank, 2)})
    result.sort(key=lambda x: x["combined_rank"])
    return result
