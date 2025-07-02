# GitHub Code Review Parser

This repository provides a simple parser for GitHub pull request review comments.
It fetches each review comment, its diff hunk, and the full diff between the PR
base commit and the commit to which the comment was attached.

## Requirements

- Python 3.8+
- `requests` library

Install dependencies with:

```bash
pip install -r requirements.txt
```

Create a file `requirements.txt` containing `requests`.

## Usage

Set the `GITHUB_API_KEY` environment variable with a GitHub personal access
token to increase rate limits (default unauthenticated limit is 60 requests per
hour).

Run the parser for a repository and pull request number:

```bash
./parse_repo.py <owner> <repo> <pull_number>
```

The script outputs the collected review comments in JSON format.
