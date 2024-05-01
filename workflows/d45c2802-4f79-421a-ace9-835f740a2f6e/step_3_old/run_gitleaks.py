import subprocess
import json
from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

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
    command = ["/usr/bin/gitleaks", "detect", "--verbose", "--report-format=json", "--report-path=/tmp/gitleaks-report.json", "--source=/code", "--no-git"]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Gitleaks exited with code {e.returncode}")

    with open("/tmp/gitleaks-report.json", "r") as f:
        gitleaks_output = json.load(f)

    jit_findings = []
    for gitleaks_finding in gitleaks_output:
        jit_finding = CodeRawControlFinding(
            test_name=gitleaks_finding["RuleID"],
            fingerprint=gitleaks_finding["Description"],
            test_id=gitleaks_finding["RuleID"],
            issue_text=f"Gitleaks rule {gitleaks_finding['RuleID']} identified a secret",
            issue_severity=Severity.HIGH,
            filename=gitleaks_finding["File"],
            line_range=f"{gitleaks_finding['StartLine']}-{gitleaks_finding['EndLine']}",
            code_snippet=gitleaks_finding["Secret"]
        )
        jit_findings.append(jit_finding)

    with open("/tmp/jit_output.json", "w") as f:
        f.write(json.dumps([finding.dict() for finding in jit_findings]))

if __name__ == "__main__":
    run_gitleaks()
