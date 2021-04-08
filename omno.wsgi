import sys
sys.path.insert(0, '/home/ubuntu/capstone')

python_home = '/home/ubuntu/capstone'
toActivate = python_home + '/venv/bin/activate_this.py'
exec(open(toActivate).read())

from omno import app as application
