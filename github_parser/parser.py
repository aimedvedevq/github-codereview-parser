import json
from dataclasses import dataclass
from typing import Dict, List, Set
from concurrent.futures import ThreadPoolExecutor, as_completed


from .api import GitHubAPI

@dataclass
class ReviewComment:
    id: int
    commit_id: str
    path: str
    diff_hunk: str
    body: str
    full_diff: str

class PullRequestParser:
    def __init__(self, api: GitHubAPI, workers: int = 4):
        """Create parser using the given GitHubAPI instance.

        Parameters
        ----------
        api: GitHubAPI
            API wrapper used for requests.
        workers: int
            Number of threads for fetching commit diffs concurrently.
        """
        self.api = api
        self.workers = workers


    def parse_review_comments(self, owner: str, repo: str, pull_number: int) -> List[ReviewComment]:
        pr_info = self.api.get_pull(owner, repo, pull_number)
        base_sha = pr_info["base"]["sha"]
        comments = self.api.list_review_comments(owner, repo, pull_number)

        diff_cache: Dict[str, str] = {}
        results: List[ReviewComment] = []

        unique_commits: Set[str] = {c["commit_id"] for c in comments}
        if unique_commits:
            with ThreadPoolExecutor(max_workers=self.workers) as exe:
                futures = {
                    exe.submit(
                        self.api.get_compare_diff, owner, repo, base_sha, sha
                    ): sha
                    for sha in unique_commits
                }
                for fut in as_completed(futures):
                    diff_cache[futures[fut]] = fut.result()

        for c in comments:
            commit_sha = c["commit_id"]

            results.append(
                ReviewComment(
                    id=c["id"],
                    commit_id=commit_sha,
                    path=c["path"],
                    diff_hunk=c.get("diff_hunk", ""),
                    body=c.get("body", ""),
                    full_diff=diff_cache.get(commit_sha, ""),

                )
            )
        return results

    @staticmethod
    def to_json(comments: List[ReviewComment]) -> str:
        return json.dumps([c.__dict__ for c in comments], indent=2)
