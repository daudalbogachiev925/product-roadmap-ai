import httpx
from typing import List, Dict
from app.config import settings

class LinearClient:
    def __init__(self):
        self.api_key = settings.LINEAR_API_KEY
        self.url = "https://api.linear.app/graphql"

    def fetch_issues(self) -> List[Dict]:
        if not self.api_key:
            return []
        query = """
        query { issues(first: 100) { nodes {
            id identifier title description
            state { name }
        } } }
        """
        r = httpx.post(self.url, json={"query": query},
                       headers={"Authorization": self.api_key}, timeout=30)
        r.raise_for_status()
        nodes = r.json().get("data", {}).get("issues", {}).get("nodes", [])
        return [{
            "external_id": n["identifier"],
            "title": n["title"],
            "description": (n.get("description") or "")[:1000],
            "status": n["state"]["name"].lower(),
        } for n in nodes]
