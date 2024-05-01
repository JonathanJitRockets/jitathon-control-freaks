import subprocess

def run_gitleaks():
    command = [
        'gitleaks',
        'detect',
        '--verbose',
        '--no-git',
        '--report-format=json',
        '--report-path=/tmp/gitleaks-report.json',
        '--source=/app'
    ]
    subprocess.run(command, check=True)

if __name__ == '__main__':
    run_gitleaks()