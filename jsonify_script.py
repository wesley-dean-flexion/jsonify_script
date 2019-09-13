#!/usr/bin/env python

import os
import json
import re
import sys


## @file jsonify_script.py
#  @brief script to build a JSON object from file
#  @author Wes Dean <wdean@flexion.us>
#  @details
#  In order to pass (and, presumably, execute) a script in Nexus3, we
#  have to upload a JSON file containing three fields: name, type, and
#  content.  This script will accept the script to process, determine
#  the name and type from the filename it's passed, and include the
#  contents of the file.
#
#  Complicating the manual drafting of these JSON documents are:
#  1. quotation marks likely need to be escaped carefully so as to not
#  foster collisions between the JSON syntax and the script's syntax.
#  2. the file contents must reside on a single line, so newlines need
#  to be escaped to '\n' sequences (that is, the backslash character
#  followed by the n character; not the newline character)
#
#  So, this tool determines the name of the script by examining the
#  filename and stripping the path and file extension.  Therefore,
#  '/path/to/awesome_script.groovy' has the name "awesome_script".
#
#  Similarly, the tool determines the type of script by examining the
#  extension of the filename.  That is, '/path/to/awesome_script.groovy'
#  has the type "groovy".
#
#  For our purposes, only the last '.' in the filename is considered
#  when separating the filename from its extension.  So, if the filename
#  is '/path/to/awesome.script.groovy' then the name is 'awesome.script'
#  and the extension is 'groovy'.


## @fn fully_qualified_filename ()
#  @brief returns the absolute, fully-qualified, expanded filename given
#  @details
#  We want to accept whatever gets passed our way, including things like
#  ~/path/filename or ${HOME}/path/filename and return the absolute
#  /path/to/filename without any symlinks or anything like that.  This
#  does that work for us.
#  @param String filename the filename to examine
#  @return String the absolute filename
#  @par Example
#  @code
#  filename = "~/src/foo/bar.txt"
#  print filename + " lives at " + fully_qualified_filename (filename)
#  @endcode
def fully_qualified_filename(filename):
    expanded_filename = os.path.expanduser(os.path.expandvars(filename))
    return os.path.abspath(expanded_filename)


## @fn slurp_file ()
#  @brief given a filename, return the contents of the file in a string
#  @details
#  This function opens the filename passed to it, reads all of the
#  content and returns it as a single string.  Lines are separated by
#  newline (or carriage return) characters, per how the file was
#  encoded.
#  @param String filename the file to open
#  @return String the file's contents
#  @par Example
#  @code
#  file_contents = slurp_file (filename)
#  @endcode
def slurp_file(filename):
    file_handle = open(filename)
    content = file_handle.read()
    file_handle.close()
    return content


## @fn script_name ()
#  @brief given a path/filename, return the filename without extension
#  @details
#  This function uses OS-safe methods to extract just the filename from
#  the filename passed along to it but without the path or filename
#  extension.  For our case, the extension is everthing after the last
#  '.' in the filename with the exception of filenames that start with
#  a '.' in which case, it's just the filename (e.g., '.bashrc' returns
#  '.bashrc')
#  @param String full_filename the filename to examine
#  @return String the filename without the path or extension
#  @par Example
#  @code
#  print "The script's name is " + script_name (filename)
#  @endcode
def script_name(full_filename):
    filename = os.path.split(full_filename)[1]
    return os.path.splitext(filename)[0]


## @fn script_Type ()
#  @brief given a path/filename, return the extension without filename
#  @details
#  This function uses OS-safe methods to extract just the extension
#  from the filename passed to the function, but without the path or
#  the base part of the filename.  Here, we use the last '.' in the
#  filename to separate the base part of the filename from the
#  extension.  If a filename is passed that starts with a '.', then
#  this will return an empty string (e.g., '.bashrc' returns '')
#  @param String full_filename the filename to examine
#  @return String the file's extension without a path or base name
#  @par Example
#  @code
#  print "The script's type is " + script_type (filename)
#  @endcode
def script_type(full_filename):
    filename = os.path.split(full_filename)[1]
    return re.sub('^.', '', os.path.splitext(filename)[1])


def main():
    # make sure we get exactly one argument (argv[0] is the program name)
    if (len(sys.argv) != 2):
        print "Usage: " + sys.argv[0] + " /path/to/filename.ext"
        sys.exit(1)

    # the first (non-program name) argument is the file to process
    filename = fully_qualified_filename(sys.argv[1])

    # build the Dict that we'll output as JSON
    data_object = {
        'name':     script_name(filename),
        'type':     script_type(filename),
        'content':  slurp_file(filename)
    }

    # finally, write out the resultant JSON object
    print json.dumps(data_object)

if __name__ == '__main__':
    main()
