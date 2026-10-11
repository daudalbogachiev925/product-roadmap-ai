from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Feature
from app.integrations.jira import JiraClient
from app.integrations.linear import LinearClient

router = APIRouter()

@router.post("/sync/{provider}")
def sync(provider: str, db: Session = Depends(get_db)):
    if provider == "jira":
        client = JiraClient()
    elif provider == "linear":
        client = LinearClient()
    else:
        raise HTTPException(400, "Unknown provider")

    items = client.fetch_issues()
    inserted = 0
    for item in items:
        existing = db.query(Feature).filter(
            Feature.external_id == item["external_id"]).first()
        if existing:
            for k, v in item.items():
                setattr(existing, k, v)
        else:
            db.add(Feature(**item))
            inserted += 1
    db.commit()
    return {"provider": provider, "total": len(items), "inserted": inserted}
