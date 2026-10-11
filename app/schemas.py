from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class FeatureBase(BaseModel):
    external_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str = "backlog"
    reach: int = 0
    impact: float = 0.0
    confidence: float = Field(0.8, ge=0, le=1)
    effort: float = Field(1.0, gt=0)
    business_value: float = 0.0
    time_criticality: float = 0.0
    risk_reduction: float = 0.0
    job_size: float = Field(1.0, gt=0)
    kano_category: str = "performance"
    epic: Optional[str] = None

class FeatureCreate(FeatureBase):
    pass

class FeatureRead(FeatureBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class RiceResult(BaseModel):
    feature_id: int
    title: str
    rice_score: float
    reach: int
    impact: float
    confidence: float
    effort: float

class WsjfResult(BaseModel):
    feature_id: int
    title: str
    wsjf_score: float
    business_value: float
    time_criticality: float
    risk_reduction: float
    job_size: float

class KanoResult(BaseModel):
    feature_id: int
    title: str
    category: str
    priority: int

class EstimateCreate(BaseModel):
    optimistic: float = Field(gt=0)
    likely: float = Field(gt=0)
    pessimistic: float = Field(gt=0)

class SimulationRequest(BaseModel):
    velocity_mean: float = 40.0
    velocity_std: float = 8.0
    n_simulations: int = Field(10000, ge=100, le=100000)

class SimulationResult(BaseModel):
    p50_days: float
    p85_days: float
    p95_days: float
    mean_days: float
    histogram: dict
