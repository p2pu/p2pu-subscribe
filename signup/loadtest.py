import subprocess
import json

f = open('signup/data.json')
data = json.load(f)

for s in data:
    subprocess.Popen(['python', 'signup/postsignup.py', json.dumps(s)])

print('Done')
