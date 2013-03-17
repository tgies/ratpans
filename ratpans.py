import yaml
import time
from subprocess import call

f = file('jobs.yml', 'r')

for job in yaml.load_all(f):
    cmdln = ['tarsnap', '--keyfile', '/root/tarsnap/tarsnap-write.key',
        '-cf', job['name'] + '-' + time.strftime('%Y%m%d')] + job['files']
    call(cmdln)
