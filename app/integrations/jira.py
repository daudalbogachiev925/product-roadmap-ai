import httpx
from typing import List, Dict
from app.config import settings

class JiraClient:
    def __init__(self):
        self.base = settings.JIRA_BASE_URL
        self.auth = (settings.JIRA_EMAIL, settings.JIRA_TOKEN)

    def fetch_issues(self, jql: str = "project = PROD") -> List[Dict]:
        if not self.base:
            return []
        url = f"{self.base}/rest/api/3/search"
        r = httpx.get(url, params={"jql": jql, "maxResults": 100},
                      auth=self.auth, timeout=30)
        r.raise_for_status()
        data = r.json().get("issues", [])
        return [self._normalize(i) for i in data]

    def _normalize(self, issue: dict) -> Dict:
        fields = issue.get("fields", {})
        return {
            "external_id": issue.get("key"),
            "title": fields.get("summary", ""),
            "description": str(fields.get("description", ""))[:1000],
            "status": fields.get("status", {}).get("name", "backlog").lower(),
        }
