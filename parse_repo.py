#!/usr/bin/env python3
import argparse

from github_parser.api import GitHubAPI
from github_parser.parser import PullRequestParser


def main():
    parser = argparse.ArgumentParser(description="Parse GitHub PR review comments")
    parser.add_argument("owner", help="Repository owner")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("pull", type=int, help="Pull request number")
    args = parser.parse_args()

    api = GitHubAPI()
    pr_parser = PullRequestParser(api)
    comments = pr_parser.parse_review_comments(args.owner, args.repo, args.pull)
    print(PullRequestParser.to_json(comments))


if __name__ == "__main__":
    main()
