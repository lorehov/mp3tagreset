'''
Created on Mar 16, 2011

@author: lev.orekhov@gmail.com
'''
import os
import sys
import copy

helptext = """
Tool for resetting mp3 tags.
Purpose: 
Some mp3 players (many of them), sort music by tag:Title (or other), so, if you're 
want to listen an audio book, you've got a problem.

Usage:
Tool is automaticly scans directories from given recursively, and resets mp3 tag to declared.

mp3tagreset [OPTION...] [DIR...]
as DIR param mp3tagreset can receive multiple directories with space separator

Examples:
    mp3tagreset -v /home/username/mp3/Hyperion
    
Options:
    -v                       verbose mode
    -a                       resets all tag
    -i                       print object info (name and tags)
    --tag=TAGNAME            resets specified tag (Title, Artist, Album)
    --value=VALUE            resets tag(s) to given value (FILENAME, INCREMENT, BLANK or custom value in quotes

Other options:
  -?, --help                 give this help list
      --usage                give a short usage message
      --version              print program version
      """

version = """
Version 0.1
Author: Lev Orekhov
        lev.orekhov@gmail.com
"""

 

try:
    import eyeD3
except:
    print "python-eyeD3 package not found, please install it first"
    sys.exit()
    
is_verbose = False
    
def printOutput(message):
    if is_verbose:
        print message

def processDir(dir):
    def changeTag():
        tag = eyeD3.Tag()
        try:
            if not tag.link(fullpath):
                print "something wrong with file " + fullpath
                return
        except:
            print fullpath + ": error, may be tags corrupted"
            return
        newTitle = entry.partition('.')[0]
        tag.setTitle(newTitle)
        tag.update()
        printOutput("%s: updated, new title is %s" % (fullpath, newTitle))

    for entry in os.listdir(dir):
        fullpath = os.path.join(dir, entry)
        if (os.path.isfile(fullpath) 
            and eyeD3.isMp3File(fullpath)):
            changeTag()
        elif os.path.isdir(fullpath):
            processDir(fullpath)
        else:
            printOutput(fullpath + ": skipped")

def run():
    root_dirs = []
    argv = copy.copy(sys.argv)
    argv.__delitem__(0)
    for arg in argv:
        if (arg == '--usage' or
            arg == '--help' or
            arg == '--version'):
            print helptext
            print version
            sys.exit()
        elif arg == '-v':
            globals()['is_verbose'] = True
        elif arg == '--version':
            print version
        elif os.path.isdir(arg):
            root_dirs.append(arg)
        else:
            print "Invalid argument '",str(arg),"' It's not a directory.\n Try ",sys.argv[0], " --usage"
            sys.exit()
    if root_dirs == []:
        root_dirs.append(os.getcwd())
    for dir in root_dirs:
        processDir(dir)
    
if __name__ == '__main__':
    run()