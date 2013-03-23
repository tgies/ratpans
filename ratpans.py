#!/usr/bin/env python

import time
from subprocess import call
import logging
import yaml

STARTTIME = time.localtime()

LOGTIMEFORMAT = "%Y%m%d %H:%M:%S"
CONSOLEFORMAT = '%(name)s: %(message)s'
LOGFILEFORMAT = '%(asctime)s %(name)s: [%(levelname)s] %(message)s'

TARSNAP = 'tarsnap'

# set up logger
log = logging.getLogger('ratpans')
log.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
consoleformatter = logging.Formatter(CONSOLEFORMAT, datefmt=LOGTIMEFORMAT)
console.setFormatter(consoleformatter)
log.addHandler(console)

log.info('aight')

with open('ratpans-config.yml', 'r') as c:
    sc = c.read()

config = yaml.load(sc)
# TODO: validate config

if config['logfile'] and config['logfile'] != 'off':
    try:
        logfile = logging.FileHandler(config['logfile'])
        logfile.setLevel(logging.ERROR)
        logfileformatter = logging.Formatter(LOGFILEFORMAT, datefmt=LOGTIMEFORMAT)
        logfile.setFormatter(logfileformatter)
        log.addHandler(logfile)
    except IOError as e:
        log.error('error: cannot open logfile "{0}": {1} [errno {2}]'
                  .format(config['logfile'], e.strerror, e.errno))
    else:
        log.critical('started logging to "{0}" (started at {1})'
                     .format(config['logfile'], time.strftime(LOGTIMEFORMAT, STARTTIME)))

j = open('ratpans-jobs.yml', 'r')
jobs = yaml.load_all(j)

# TODO: yaml.load_all seemingly streams from file or has bizarro
# threadsafety issues or something, because I could not manage to close the
# file seemingly at any time without it stacking the hell out. this is
# annoying and I will figure it out later.

for job in jobs:
    if 'keyfile' in job:
        keyfile_option = ['--keyfile', job['keyfile']]
    elif 'keyfile' in config:
        keyfile_option = ['--keyfile', config['keyfile']]
    else:
        keyfile_option = []

    log.critical('Job ' + job['name'] + ' starting')

    # TODO: builder class for tarsnap cmdln or class that just abstracts
    # away calling tarsnap probably. REALLY need to be validating things
    # before just chucking them on a command line and expecting anything
    # sensible to happen.

    cmdln = [TARSNAP] + keyfile_option + ['-cf', job['name'] + '-' + 
                                          time.strftime('%Y%m%d')] + job['files']

    log.debug(cmdln)
    ret = call(cmdln)
    if ret == 0:
        log.critical('Job ' + job['name'] + ' completed successfully')
    else:
        log.error('Job ' + job['name'] + \
                        ' failed with code ' + str(ret))

log.critical('done')
j.close()
