#!/usr/bin/env python3
import urllib.request, json, subprocess

def check():
    p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate('protocol=https\nhost=github.com\n\n')
    creds = dict(line.split('=', 1) for line in out.splitlines() if '=' in line)
    pat = creds.get('password')
    headers = {'Authorization': f'Bearer {pat}', 'User-Agent': 'Python'}
    
    req = urllib.request.Request('https://api.github.com/repos/sajuptpm/spring-boot/actions/runs/41329135678/jobs', headers=headers)
    res = json.loads(urllib.request.urlopen(req).read().decode())
    jobs = res.get('jobs', [])
    print(f"{'JOB NAME':<25} | {'STATUS':<12} | {'CONCLUSION':<12}")
    print("-" * 55)
    for j in jobs:
        print(f"{j['name']:<25} | {j['status']:<12} | {str(j['conclusion']):<12}")

if __name__ == '__main__':
    check()
