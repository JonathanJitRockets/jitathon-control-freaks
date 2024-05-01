import subprocess
import json
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class Severity(str, Enum):
    CRITICAL = 'CRITICAL'
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

class CodeRawControlFinding(BaseModel):
    test_name: str
    fingerprint: str 
    test_id: str
    issue_text: Optional[str]
    issue_confidence: str = 'UNDEFINED'
    issue_severity: Severity
    references: Optional[List[Dict[Optional[str], Optional[str]]]] = []
    location: Optional[str] = None
    location_text: Optional[str] = None
    filename: Optional[str]
    line_range: Optional[str]
    code_snippet: Optional[str]

def run_gitleaks():
    command = [
        '/usr/bin/gitleaks',
        'detect',
        '--verbose',
        '--report-format=json',
        '--report-path=/tmp/gitleaks-report.json',
        '--source=/code',
        '--no-git'
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Gitleaks exited with status {e.returncode}. Processing the output.\n')
    with open('/tmp/gitleaks-report.json', 'r') as file:
        data = json.load(file)
    findings = []
    for item in data:
        finding = CodeRawControlFinding(
            test_name=item.get('RuleID', 'Unknown'),
            fingerprint=item.get('Fingerprint', ''),
            test_id=item.get('RuleID', 'Unknown'),
            issue_text=item.get('Description', ''),
            issue_severity=Severity.HIGH,
            location=item.get('File', ''),
            location_text='Gitleaks detected a potential secret',
            filename=item.get('File', ''),
            line_range=f"{item.get('StartLine', '')}-{item.get('EndLine', '')}",
            code_snippet=item.get('Secret', '')
        )
        findings.append(finding.dict())
    with open('/tmp/jit_output.json', 'w') as file:
        json.dump(findings, file, indent=4)

if __name__ == '__main__':
    run_gitleaks()
