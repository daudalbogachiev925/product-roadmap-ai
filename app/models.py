from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="backlog", index=True)
    reach = Column(Integer, default=0)
    impact = Column(Float, default=0.0)
    confidence = Column(Float, default=0.8)
    effort = Column(Float, default=1.0)
    business_value = Column(Float, default=0.0)
    time_criticality = Column(Float, default=0.0)
    risk_reduction = Column(Float, default=0.0)
    job_size = Column(Float, default=1.0)
    kano_category = Column(String, default="performance")
    epic = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())

    estimates = relationship("Estimate", back_populates="feature")

class Estimate(Base):
    __tablename__ = "estimates"

    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey("features.id"))
    optimistic = Column(Float, nullable=False)
    likely = Column(Float, nullable=False)
    pessimistic = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    feature = relationship("Feature", back_populates="estimates")
