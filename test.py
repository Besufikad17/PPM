import subprocess

s = subprocess.Popen('python', shell=True)
print(s.returncode)