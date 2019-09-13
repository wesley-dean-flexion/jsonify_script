# jsonify\_script

This is a tool to package a script into a JSON file.

## How (do I use it)?

Call the script with the name of the file to include (JSONify) like so:

```
$ ./jsonify_script.py "/path/to/awesomeness.groovy"
```

Currently, it takes exactly one argument -- the filename to include.

## What (happens)?

When the script runs, it reads (slurps) the contents of the file
provided into memory and exports it to a hash in a JSON object
named "content".

The filename (basename -- no path or extension) is exported in
the "name" field.

The file's extension is exported in the "type" field.


```
$ cat ./disable_anonymous_access.groovy
#!groovy

// the following disables anonymous repo access:
security.setAnonymousAccess (false)

$ ./jsonify_script.py ./disable_anonymous_access.groovy
{"content": "#!groovy\n\n// the following disables anonymous repo access:\nsecurity.setAnonymousAccess (false)\n", "type": "groovy", "name": "disable_anonymous_access"}

```

### What (do I need to use this)?

This script only uses the Python Standard Library, so it ought to run
anywhere where Python is installed.  Moreover, it uses os-independent
functions to access and manipulate paths and filenames to give this
the best chance of operating properly regardless of execution
environment.

## Why (did you write this)?

This tool exists because it's a nightmare to package Groovy scripts for use
with Nexus Repository Manager 3 into JSON objects, particularly non-trivial
scripts that span multiple lines, have quotation marks, etc..  This tool
gets around that by handling the JSONification for you, including setting
parameters in the JSON object as needed for import into Nexus.

The trick is to let the fine folks who maintain the Python 'json' module
handle the ugly business..

## Who (contributed to this)?

The folks who maintain Python and the Standard Python Library deserve
all of the credit.  All I did was to bikeshed a script around some
simple function calls.

