from worker import celery
from app.database import SessionLocal
from app.models import Feature
from app.integrations.jira import JiraClient

@celery.task(name="sync_jira")
def sync_jira_task():
    db = SessionLocal()
    try:
        items = JiraClient().fetch_issues()
        inserted = 0
        for item in items:
            existing = db.query(Feature).filter(
                Feature.external_id == item["external_id"]).first()
            if not existing:
                db.add(Feature(**item))
                inserted += 1
        db.commit()
        return {"inserted": inserted}
    finally:
        db.close()
