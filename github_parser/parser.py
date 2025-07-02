import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional

from .api import GitHubAPI

@dataclass
class ReviewComment:
    id: int
    commit_id: str
    path: str
    diff_hunk: str
    body: str
    full_diff: str
    in_reply_to_id: Optional[int]

class PullRequestParser:
    def __init__(self, api: GitHubAPI):
        self.api = api

    def parse_review_comments(self, owner: str, repo: str, pull_number: int) -> List[ReviewComment]:
        pr_info = self.api.get_pull(owner, repo, pull_number)
        base_sha = pr_info["base"]["sha"]
        comments = self.api.list_review_comments(owner, repo, pull_number)

        diff_cache: Dict[str, str] = {}
        results: List[ReviewComment] = []

        for c in comments:
            commit_sha = c["commit_id"]
            if commit_sha not in diff_cache:
                diff_cache[commit_sha] = self.api.get_compare_diff(owner, repo, base_sha, commit_sha)
            results.append(
                ReviewComment(
                    id=c["id"],
                    commit_id=commit_sha,
                    path=c["path"],
                    diff_hunk=c.get("diff_hunk", ""),
                    body=c.get("body", ""),
                    full_diff=diff_cache[commit_sha],
                    in_reply_to_id=c.get("in_reply_to_id"),
                )
            )
        return results

    @staticmethod
    def to_json(comments: List[ReviewComment]) -> str:
        return json.dumps([c.__dict__ for c in comments], indent=2)
