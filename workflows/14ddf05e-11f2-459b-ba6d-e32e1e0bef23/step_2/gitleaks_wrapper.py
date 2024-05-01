import subprocess

def run_gitleaks():
    # Command to run Gitleaks with the required parameters
    command = [
        './gitleaks', 'detect',
        '--verbose',
        '--report-format=json',
        '--report-path=/tmp/gitleaks-report.json',
        '--source=/code',
        '--no-git'
    ]

    # Execute the command
    subprocess.run(command, check=True)

if __name__ == "__main__":
    run_gitleaks()
