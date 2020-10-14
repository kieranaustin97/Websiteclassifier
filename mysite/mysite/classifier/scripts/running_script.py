import subprocess
from subprocess import PIPE

test_output = subprocess.run('python mysite/mysite/classifier/scripts/test_script.py', stdout=PIPE, encoding='utf-8')

print(test_output.stdout)