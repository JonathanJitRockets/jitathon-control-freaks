import subprocess

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
    subprocess.run(command, check=True)

if __name__ == '__main__':
    run_gitleaks()