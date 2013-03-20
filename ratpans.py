import sys
import yaml
import time
from subprocess import call

print 'ratpans: aight'
with file('jobs.yml', 'r') as f:
    jobs = yaml.load_all(f)

    for job in jobs:
        print 'ratpans: Job ' + job['name'] + ' starting'
        cmdln = ['tarsnap', '--keyfile', '/root/tarsnap/tarsnap-write.key',
            '-cf', job['name'] + '-' + time.strftime('%Y%m%d')] + job['files']
        ret = call(cmdln)
        if ret == 0:
            print 'ratpans: Job ' + job['name'] + ' completed successfully'
        else:
            print >> sys.stderr, 'ratpans: error: Job ' + job['name'] + ' failed with code ' + str(ret)
