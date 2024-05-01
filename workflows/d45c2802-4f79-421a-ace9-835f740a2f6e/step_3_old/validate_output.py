import json
from run_gitleaks import CodeRawControlFinding

with open('./local_tmp/jit_output.json', 'r') as f:
    jit_output = json.load(f)

for finding in jit_output:
    parsed_finding = CodeRawControlFinding(**finding)
    print(parsed_finding)
