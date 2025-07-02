import os
import time
from typing import Dict, List, Optional

import requests

class GitHubAPI:
    def __init__(self, token: Optional[str] = None, base_url: str = "https://api.github.com"):
        self.token = token or os.getenv("GITHUB_API_KEY")
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        self.session.headers.update({"Accept": "application/vnd.github+json"})

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        while True:
            resp = self.session.request(method, url, **kwargs)
            remaining = int(resp.headers.get("X-RateLimit-Remaining", 1))
            reset = int(resp.headers.get("X-RateLimit-Reset", 0))
            if resp.status_code == 403 and remaining == 0:
                sleep_for = max(reset - int(time.time()), 1)
                time.sleep(sleep_for)
                continue
            resp.raise_for_status()
            return resp

    def get_pull(self, owner: str, repo: str, pull_number: int) -> Dict:
        resp = self._request("GET", f"/repos/{owner}/{repo}/pulls/{pull_number}")
        return resp.json()

    def list_review_comments(self, owner: str, repo: str, pull_number: int, per_page: int = 100) -> List[Dict]:
        comments = []
        page = 1
        while True:
            resp = self._request(
                "GET",
                f"/repos/{owner}/{repo}/pulls/{pull_number}/comments",
                params={"per_page": per_page, "page": page},
            )
            chunk = resp.json()
            if not chunk:
                break
            comments.extend(chunk)
            page += 1
        return comments

    def get_compare_diff(self, owner: str, repo: str, base: str, head: str) -> str:
        resp = self._request(
            "GET",
            f"/repos/{owner}/{repo}/compare/{base}...{head}",
            headers={"Accept": "application/vnd.github.v3.diff"},
        )
        return resp.text
