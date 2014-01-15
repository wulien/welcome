import subprocess

r = subprocess.check_call('ls -lstsjkf', shell=True)
# print r