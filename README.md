ratpans
========
*as in the expression, "to have [one's] rats in a pan"*

Copyright © 2013 Tony Gies
March 23, 2013

synopsis
--------

ratpans is a tool that allows you to automate backups using the Tarsnap backup service.

ratpans is still in an early stage of development and should not be relied upon for any purpose, ever.

requirements
------------

ratpans requires [Tarsnap](https://www.tarsnap.com/) <= 1.0.28, an active and funded Tarsnap account, Python <= 2.6 and PyYAML.

usage
-----

Just invoke ratpans directly.

ratpans needs two configuration files to work; one specifying global configuration and one specifying backup jobs to carry out. Currently, ratpans just looks for `ratpans-config.yml` and `ratpans-jobs.yml` in the current directory.

Presently, no runtime options are implemented; ratpans looks for these specific files and tries to carry out all the jobs found in them.

configuration
-------------

`ratpans-config.yml` ought to look something like this:
```yaml
tarsnap: /usr/local/bin/tarsnap
keyfile: /root/tarsnap/tarsnap-write.key
logfile: ratpans.log
timestamp: "%Y%m%d"
```

`tarsnap:` *(optional)* path to tarsnap (we'll just hope it's in the PATH if not provided)
`keyfile:` *(optional)* path to a non-passphrase-protected tarsnap keyfile having write permissions to use. Can be overridden on the job level. If not provided, tarsnap uses its default key.
`logfile:` *(optional)* a file to log critical events (job starts, ends) and errors to.
`timestamp:` *(optional)* the strftime() format to be used for timestamping tarsnap archives. Currently ignored and fixed to "%Y%m%d".

WARNING: Notice how all the configuration directives are optional? Well, right now, you need to have a ratpans-config.yml even if it's empty. I'm sorry.

jobs
----

As mentioned above, ratpans looks for a `ratpans-jobs.yml` describing backup jobs to carry out through tarsnap.

`ratpans-jobs.yml` ough to look something like this:
```yaml
---
name: home-tgies
files:
 - /home/tgies
keyfile: /root/tarsnap/tarsnap-tgies-write.key
---
name: home-deployer
files:
 - /home/deployer
---
name: nginx-config
files:
 - /etc/nginx/nginx.conf
 - /etc/nginx/sites-available
```

As illustrated, backup job records must start with a line containing only --- (this is a YAML thing).
`name:` The name of the backup job. The archive name used by Tarsnap will be derived from this name and a timestamp.
`files:` A list of paths to be included in the backup, formatted as a YAML list (see example).
`keyfile:` *(optional)* A keyfile to use for this particular job, overriding the keyfile set in `ratpans-config.yml` and/or the default keyfile configured in tarsnap.

errata
------

Once again, ratpans is in a very early stage of development. It is not to be expected to work or to be fit for any purpose.

ratpans has extremely limited error checking and currently has no idea what to do with any error result returned by tarsnap. This is partly tarsnap's fault for returning 1 on any error.

contributing
------------

At this early a stage in development, I'd prefer to establish my own program architecture before I 
