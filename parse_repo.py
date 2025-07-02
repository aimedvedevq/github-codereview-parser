#!/usr/bin/env python3
import argparse

from github_parser.api import GitHubAPI
from github_parser.parser import PullRequestParser


def main():
    api = GitHubAPI()
    pr_parser = PullRequestParser(api)
    comments = pr_parser.parse_review_comments('embeddings-benchmark', 'mteb', 2838)
    
    # Filter out reply comments - only keep original comments
    original_comments = [c for c in comments if c.in_reply_to_id is None]
    
    print(f"Total comments: {len(comments)}")
    print(f"Original comments (non-replies): {len(original_comments)}")
    print(f"Reply comments filtered out: {len(comments) - len(original_comments)}")
    print("\nOriginal comments only:")
    print(PullRequestParser.to_json(original_comments))


if __name__ == "__main__":
    main()
