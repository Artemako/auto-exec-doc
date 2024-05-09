import subprocess

command = ['unoconv', '-f', 'png', 'examples/example.docx']
subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)