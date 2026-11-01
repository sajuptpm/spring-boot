#!/usr/bin/env python3
"""
Trigger a GitHub Actions workflow in sajuptpm/spring-boot using Git Credential Manager or a GitHub Token.

Usage:
    python workflow-fixes/trigger-workflow.py <workflow-filename> [branch] [inputs_json]
    python workflow-fixes/trigger-workflow.py build-pull-request.yml main
    python workflow-fixes/trigger-workflow.py publicize-release.yml main '{"milestone": "4.2.0", "latest": "true"}'
"""

import sys
import json
import urllib.request
import subprocess

REPO = "sajuptpm/spring-boot"

def get_token():
    # 1. Try Git Credential Manager first
    try:
        p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, _ = p.communicate('protocol=https\nhost=github.com\n\n')
        creds = dict(line.split('=', 1) for line in out.splitlines() if '=' in line)
        if creds.get('password'):
            return creds['password']
    except Exception:
        pass

    # 2. Try environment variable
    import os
    if os.getenv('GITHUB_TOKEN'):
        return os.environ['GITHUB_TOKEN']
    if os.getenv('GH_TOKEN'):
        return os.environ['GH_TOKEN']

    return None

def trigger_workflow(workflow_file, branch="main", inputs=None):
    token = get_token()
    if not token:
        print("ERROR: Could not retrieve a GitHub token from Git Credential Manager or GITHUB_TOKEN environment variable.")
        print("Please set GITHUB_TOKEN or ensure git credentials are saved.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{workflow_file}/dispatches"
    body = {"ref": branch}
    if inputs:
        if isinstance(inputs, str):
            try:
                body["inputs"] = json.loads(inputs)
            except Exception as e:
                print(f"Warning: Failed to parse inputs as JSON: {e}")
                body["inputs"] = {}
        elif isinstance(inputs, dict):
            body["inputs"] = inputs

    payload = json.dumps(body).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Antigravity-Workflow-Trigger"
    })

    print(f"Triggering workflow '{workflow_file}' on branch '{branch}' with inputs {body.get('inputs', {})} in {REPO}...")
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 204:
                print(f"SUCCESS: Workflow '{workflow_file}' triggered successfully! (HTTP 204)")
                print(f"View runs at: https://github.com/{REPO}/actions/workflows/{workflow_file}")
            else:
                print(f"Response status: {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python trigger-workflow.py <workflow-filename> [branch] [inputs_json]")
        print("Example: python trigger-workflow.py publicize-release.yml main '{\"milestone\": \"4.2.0\"}'")
        sys.exit(1)

    wf = sys.argv[1]
    br = sys.argv[2] if len(sys.argv) > 2 else "main"
    inp = sys.argv[3] if len(sys.argv) > 3 else None
    trigger_workflow(wf, br, inp)
