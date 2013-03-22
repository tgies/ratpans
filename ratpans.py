import sys
import yaml
import time
from subprocess import call

TARSNAP='tarsnap'

print 'ratpans: aight'

with file('ratpans-config.yml', 'r') as c:
    sc = c.read()

config = yaml.load(sc)
# TODO: validate config

with file('jobs.yml', 'r') as j:
    jobs = yaml.load_all(j)

    for job in jobs:
        if 'keyfile' in job:
            keyfile_option = ['--keyfile', job['keyfile']]
        elif 'keyfile' in config:
            keyfile_option = ['--keyfile', config['keyfile']]
        else:
            keyfile_option = []
        print 'ratpans: Job ' + job['name'] + ' starting'
        # TODO: builder class for tarsnap cmdln or class that just abstracts away calling tarsnap probably
        cmdln = [TARSNAP] + keyfile_option + ['-cf', job['name'] + '-' + time.strftime('%Y%m%d')] + job['files']
        print cmdln
        ret = call(cmdln)
        if ret == 0:
            print 'ratpans: Job ' + job['name'] + ' completed successfully'
        else:
            print >> sys.stderr, 'ratpans: error: Job ' + job['name'] + ' failed with code ' + str(ret)
