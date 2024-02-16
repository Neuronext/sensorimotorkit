import subprocess
import os

png_file_path = 'input.png'
node_path = 'C:\\Program Files\\nodejs\\node.exe'
result = subprocess.run([node_path, 'humanTracking.js', png_file_path], capture_output=True, text=True)

if result.stdout:
    print(result.stdout)
else:
    print("Error or no output from humanTracking.js:", result.stderr)
