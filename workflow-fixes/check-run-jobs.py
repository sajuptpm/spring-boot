#!/usr/bin/env python3
import sys, urllib.request, json, subprocess

def check(run_id):
    p = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate('protocol=https\nhost=github.com\n\n')
    creds = dict(line.split('=', 1) for line in out.splitlines() if '=' in line)
    pat = creds.get('password')
    headers = {'Authorization': f'Bearer {pat}', 'User-Agent': 'Python'}
    
    req = urllib.request.Request(f'https://api.github.com/repos/sajuptpm/spring-boot/actions/runs/{run_id}', headers=headers)
    res = json.loads(urllib.request.urlopen(req).read().decode())
    print(f"Run {run_id} ({res.get('name')}) - Status: {res.get('status')} | Conclusion: {res.get('conclusion')}")
    
    req_jobs = urllib.request.Request(f'https://api.github.com/repos/sajuptpm/spring-boot/actions/runs/{run_id}/jobs', headers=headers)
    jobs_res = json.loads(urllib.request.urlopen(req_jobs).read().decode())
    for j in jobs_res.get('jobs', []):
        print(f"  {j['name']:<28} | {j['status']:<12} | {str(j['conclusion']):<10}")

if __name__ == '__main__':
    r_id = sys.argv[1] if len(sys.argv) > 1 else '41335144421'
    check(r_id)
