#!/usr/bin/env python3
import argparse
import json
import csv

from github_parser import GitHubAPI, PullRequestParser


def main():
    argp = argparse.ArgumentParser(
        description="Parse review comments for all pull requests in repos_stats_all.json"
    )
    argp.add_argument(
        "--input",
        default="repos_stats_all.json",
        help="Path to JSON file with repository stats",
    )
    argp.add_argument(
        "--output", default="output.csv", help="CSV file to write the results"
    )
    args = argp.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        repos = json.load(f)

    api = GitHubAPI()
    parser = PullRequestParser(api)

    with open(args.output, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(
            [
                "repo",
                "pull_number",
                "comment_id",
                "commit_id",
                "path",
                "diff_hunk",
                "body",
                "full_diff",
            ]
        )
        for repo in repos:
            owner = repo.get("owner")
            name = repo.get("name")
            if not owner or not name:
                continue
            pulls = api.list_pull_requests(owner, name)
            for pr in pulls:
                number = pr["number"]
                comments = parser.parse_review_comments(owner, name, number)
                for c in comments:
                    writer.writerow(
                        [
                            f"{owner}/{name}",
                            number,
                            c.id,
                            c.commit_id,
                            c.path,
                            c.diff_hunk,
                            c.body,
                            c.full_diff,
                        ]
                    )


if __name__ == "__main__":
    main()
