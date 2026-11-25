"""Collect public GitHub profile stats, then render the two profile cards."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo

from render import render


OWNER = "omersukruvarol"
SNAPSHOT = Path(__file__).with_name("stats.json")


def github(endpoint, *args):
    result = subprocess.run(
        ["gh", "api", endpoint, *args], check=True,
        stdout=subprocess.PIPE, text=True, timeout=120,
    )
    return json.loads(result.stdout)


def authored_count(kind):
    result = github(
        "search/issues", "--method", "GET", "-f",
        f"q=author:{OWNER} is:public is:{kind}", "-F", "per_page=1",
    )
    if result["incomplete_results"]:
        raise RuntimeError(f"GitHub returned an incomplete {kind} count")
    return result["total_count"]


def refresh():
    pages = github(f"users/{OWNER}/repos?type=owner&per_page=100",
                   "--paginate", "--slurp")
    repos = {r["id"]: r for page in pages for r in page if not r["private"]}
    if len(repos) != github(f"users/{OWNER}")["public_repos"]:
        raise RuntimeError("Public repository listing is incomplete")

    languages = Counter()
    for repo in repos.values():
        if not repo["fork"] and repo["name"].lower() != OWNER:
            languages.update(github(f"repos/{repo['full_name']}/languages"))

    snapshot = {
        "as_of": datetime.now(ZoneInfo("Europe/Istanbul")).date().isoformat(),
        "public_repositories": len(repos),
        "public_pull_requests_authored": authored_count("pr"),
        "public_issues_authored": authored_count("issue"),
        "language_bytes": dict(sorted(languages.items(), key=lambda kv: (-kv[1], kv[0]))),
    }
    pending = SNAPSHOT.with_suffix(".json.tmp")
    pending.write_text(json.dumps(snapshot, indent=2) + "\n")
    pending.replace(SNAPSHOT)
    render()


if __name__ == "__main__":
    refresh()
