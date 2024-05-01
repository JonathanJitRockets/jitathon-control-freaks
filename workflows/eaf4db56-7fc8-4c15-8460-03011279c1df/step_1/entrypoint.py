import os
import subprocess

# Define the directories
output_directory = '/tmp'
scan_directory = '/code'

# Command to run checkov
command = ['checkov', '--directory', scan_directory, '-o', 'json', '--output-file-path', os.path.join(output_directory, 'checkov-report.json')]

# Execute the command
result = subprocess.run(command, capture_output=True)

# Print stdout and stderr for logging in container logs
print(result.stdout.decode())
print(result.stderr.decode())