#!/usr/bin/env python3
"""
Trigger a GitHub Actions workflow in sajuptpm/spring-boot using Git Credential Manager or a GitHub Token.

Usage:
    python workflow-fixes/trigger-workflow.py <workflow-filename> [branch] [inputs]
    python workflow-fixes/trigger-workflow.py build-pull-request.yml main
    python workflow-fixes/trigger-workflow.py publicize-release.yml main milestone=4.2.0,latest=true
    python workflow-fixes/trigger-workflow.py publicize-release.yml main '{"milestone": "4.2.0", "latest": "true"}'
"""

import sys
import json
import re
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

def parse_inputs(raw):
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    
    # Format 1: Direct JSON
    try:
        return json.loads(raw)
    except Exception:
        pass

    # Format 2: key=val,key2=val2
    if "=" in raw:
        data = {}
        for part in raw.split(","):
            if "=" in part:
                k, v = part.split("=", 1)
                data[k.strip().strip("'\"")] = v.strip().strip("'\"")
        return data

    # Format 3: PowerShell stripped quotes: {key: val, key2: val2}
    try:
        s = raw.strip("{}")
        data = {}
        for part in s.split(","):
            if ":" in part:
                k, v = part.split(":", 1)
                data[k.strip().strip("'\"")] = v.strip().strip("'\"")
        return data
    except Exception:
        pass

    return {}

def trigger_workflow(workflow_file, branch="main", inputs=None):
    token = get_token()
    if not token:
        print("ERROR: Could not retrieve a GitHub token from Git Credential Manager or GITHUB_TOKEN environment variable.")
        print("Please set GITHUB_TOKEN or ensure git credentials are saved.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{workflow_file}/dispatches"
    body = {"ref": branch}
    
    parsed_inputs = parse_inputs(inputs)
    if parsed_inputs:
        body["inputs"] = parsed_inputs

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
        print("Usage: python trigger-workflow.py <workflow-filename> [branch] [inputs]")
        print("Example: python trigger-workflow.py publicize-release.yml main milestone=4.2.0,latest=true")
        sys.exit(1)

    wf = sys.argv[1]
    br = sys.argv[2] if len(sys.argv) > 2 else "main"
    inp = sys.argv[3] if len(sys.argv) > 3 else None
    trigger_workflow(wf, br, inp)
