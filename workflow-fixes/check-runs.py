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
import subprocess

REPO = "sajuptpm/spring-boot"

def get_token():
    try:
        p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, _ = p.communicate('protocol=https\nhost=github.com\n\n')
        creds = dict(line.split('=', 1) for line in out.splitlines() if '=' in line)
        if creds.get('password'):
            return creds['password']
    except Exception:
        pass

    import os
    if os.getenv('GITHUB_TOKEN'):
        return os.environ['GITHUB_TOKEN']
    if os.getenv('GH_TOKEN'):
        return os.environ['GH_TOKEN']

    return None

def check_runs(limit=5):
    token = get_token()
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Antigravity-Workflow-Monitor"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"https://api.github.com/repos/{REPO}/actions/runs?per_page={limit}"
    req = urllib.request.Request(url, headers=headers)

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

    first_run = runs[0]
    print(f"\n--- Latest Run Details: {first_run.get('name')} (#{first_run.get('run_number')}) ---")
    print(f"URL: {first_run.get('html_url')}")
    
    jobs_url = first_run.get("jobs_url")
    if jobs_url:
        try:
            req_jobs = urllib.request.Request(jobs_url, headers=headers)
            with urllib.request.urlopen(req_jobs) as resp:
                jobs_data = json.loads(resp.read().decode("utf-8"))
                for j in jobs_data.get("jobs", []):
                    j_name = j.get("name")
                    j_status = j.get("status")
                    j_concl = j.get("conclusion")
                    print(f"\nJob: {j_name} | Status: {j_status} | Conclusion: {j_concl}")
                    print(f"Job URL: {j.get('html_url')}")
                    steps = j.get("steps", [])
                    if steps:
                        print(f"{'STEP':<4} {'STATUS':<14} {'CONCLUSION':<12} {'NAME'}")
                        print("-" * 60)
                        for s in steps:
                            s_num = str(s.get("number"))
                            s_status = s.get("status")
                            s_concl = str(s.get("conclusion") or "")
                            s_name = s.get("name")
                            print(f"{s_num:<4} {s_status:<14} {s_concl:<12} {s_name}")
        except Exception as e:
            print(f"Could not load jobs details: {e}")

if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    check_runs(lim)
