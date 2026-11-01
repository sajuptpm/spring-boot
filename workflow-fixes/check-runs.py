#!/usr/bin/env python3
"""
Check recent GitHub Actions workflow runs and active step progress in sajuptpm/spring-boot.

Usage:
    python workflow-fixes/check-runs.py [limit]
"""

import sys
import json
import urllib.request
import urllib.error

REPO = "sajuptpm/spring-boot"

def check_runs(limit=5):
    url = f"https://api.github.com/repos/{REPO}/actions/runs?per_page={limit}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Antigravity-Workflow-Monitor"
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error querying runs: {e}")
        return

    runs = data.get("workflow_runs", [])
    if not runs:
        print("No workflow runs found.")
        return

    print(f"\n{'RUN ID':<13} {'WORKFLOW NAME':<30} {'STATUS':<14} {'CONCLUSION':<12} {'EVENT':<16}")
    print("-" * 90)
    for r in runs:
        run_id = str(r.get("id"))
        name = r.get("name", "Unknown")[:28]
        status = r.get("status", "")
        conclusion = r.get("conclusion") or "running"
        event = r.get("event", "")
        print(f"{run_id:<13} {name:<30} {status:<14} {conclusion:<12} {event:<16}")

    # Inspect the most recent running or completed job
    first_run = runs[0]
    print(f"\n--- Latest Run Details: {first_run.get('name')} (#{first_run.get('run_number')}) ---")
    print(f"URL: {first_run.get('html_url')}")
    
    jobs_url = first_run.get("jobs_url")
    if jobs_url:
        try:
            req_jobs = urllib.request.Request(jobs_url, headers={"User-Agent": "Antigravity-Workflow-Monitor"})
            with urllib.request.urlopen(req_jobs) as j_resp:
                j_data = json.loads(j_resp.read().decode("utf-8"))
                for job in j_data.get("jobs", []):
                    print(f"\nJob: {job.get('name')} | Status: {job.get('status')} | Conclusion: {job.get('conclusion')}")
                    print(f"Job URL: {job.get('html_url')}")
                    print(f"{'STEP':<4} {'STATUS':<14} {'CONCLUSION':<12} {'NAME'}")
                    print("-" * 60)
                    for step in job.get("steps", []):
                        s_num = str(step.get("number"))
                        s_status = step.get("status", "")
                        s_concl = step.get("conclusion") or ""
                        s_name = step.get("name", "")
                        print(f"{s_num:<4} {s_status:<14} {s_concl:<12} {s_name}")
        except Exception as e:
            print(f"Could not load job steps: {e}")

if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    check_runs(lim)
