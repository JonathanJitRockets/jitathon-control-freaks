import os
import subprocess

# Define the directories
output_directory = '/tmp'
scan_directory = '/code'

# Command to run checkov
command = ['checkov', '--directory', scan_directory, '-o', 'json', '--output-file-path', os.path.join(output_directory, 'checkov-report.json')]

# Execute the command and suppress additional outputs
subprocess.run(command)