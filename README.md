# GitHub Code Review Parser

This repository provides a simple parser for GitHub pull request review comments.
It fetches each review comment, its diff hunk, and the full diff between the PR
base commit and the commit to which the comment was attached.

## Requirements

- Python 3.8+
- `requests`
- `tqdm`

Install dependencies with:

```bash
pip install -r requirements.txt
```

Create a file `requirements.txt` containing the packages above.

## Usage

Set the `GITHUB_API_KEY` environment variable with a GitHub personal access
token to increase rate limits (default unauthenticated limit is 60 requests per
hour).

Run the parser for a repository and pull request number:

```bash
./parse_repo.py <owner> <repo> <pull_number> [--workers N]
```

The script outputs the collected review comments in JSON format.

To process all repositories listed in `repos_stats_all.json` and write the
results into `output.csv`, run:

```bash
./parse_all.py --input repos_stats_all.json --output output.csv [--workers N]
```
The bulk parser shows progress with `tqdm` and skips pull requests that have no
review comments to reduce API calls. Diff retrieval is parallelized with a
thread pool (`--workers` option) to improve performance without exceeding rate
limits.
