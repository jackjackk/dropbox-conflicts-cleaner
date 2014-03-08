# -*- coding: utf-8 -*-
import os
import re
import time
import hashlib
import sys
import subprocess as sp

"""
Specify extra pairs (key, command), where {command} is run when key is pressed,
assuming that the argument to command is the list of conflicting files
"""
extrakeys = {
    'd' : ('Beyond Compare', (lambda flist: r'C:\Program Files (x86)\Beyond Compare 3\BCompare.exe %s'%' '.join(['"%s"'%f for f in flist]))),
    'e' : ('Explorer', (lambda flist: r'explorer /e,/select,"%s"' % flist[0]))
    }

def _find_getch():
    """
    Returns getch()-like function
    http://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user
    """
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


def calcHash(f):
    """
    Returns a string MD5-hash of file {f}, or the string '' if something goes wrong
    
    Parameters
    ----------
    f: file to read
    """
    try:
        fhandle = open(f,'r')
        rhex = hashlib.md5(fhandle.read()).hexdigest()
        fhandle.close()
    except:
        rhex = ''
    return rhex

def handleConflicted(title,fgroup):
    """
    Provides interactive selection of one file among those listed in {fgroup} to be kept
    The non-selected files will be removed, while the selected one will be renamed to {title}
    Extra functions can be configured through the global {extrakeys} parameter

    Parameters
    ----------
    title: common root path+name of the files to choose from
    fgroup: list of (desc, st_size, st_mtime) tuples, one for each conflicted file, where
            - desc is the conflict string
            - st_size is the size in bytes
            - st_mtime is the time of last modification
    """
    print title
    print '-'*len(title)
    finord = []
    count = 0
    firstfilesize = fgroup[0][1]
    lasthash = None
    interactive_flag = False
    for f in sorted(fgroup, key=lambda tup: -tup[-1]):
        if f[0] != '(current)':
            p,e = os.path.splitext(title)
            finord.append('%s%s%s' % (p,f[0],e))
        else:
            finord.append(title)
        count += 1
        currhash = 'n.c.'
        if firstfilesize != f[1]:
            interactive_flag = True
        else:
            if not interactive_flag:
                currhash = calcHash(finord[-1])
                if (lasthash != None) and (currhash != lasthash):
                    interactive_flag = True
                else:
                    lasthash = currhash
        print "%3d)%50s%20d%30s%30s" % (count,((f[0].strip())[1:-1]).strip(),f[1],time.ctime(f[2]),currhash)
    if interactive_flag:
        if len(finord)>9:
            get_input = raw_input
        else:
            get_input = getch
        sys.stdout.write('\nWhat to keep ("h" for help)? ')
        k = get_input()
        isvalid = False
        while (not isvalid) and (not k in ['',chr(13),chr(27)]):
            print k
            try:
                kn = int(k)
                if kn<1 or kn>len(finord):
                    isvalid = False
                else:
                    isvalid = True
            except:
                isvalid = False
                if k=='h':
                    print 'Press:'
                    print '[1-%d] for keeping corresponding file' % len(finord)
                    print '[esc] for exiting'
                    print '[ret] for continuing without taking action'                    
                    for ek,ev in extrakeys.iteritems():
                        print '[%s] for running "%s"' % (ek,ev[0])
                elif extrakeys.has_key(k):
                    sp.Popen(extrakeys[k][1](finord))
            if (not isvalid):
                sys.stdout.write('What to keep ("h" for help)? ')
                k = get_input()
    else:
        print 'Automatic mode'
        isvalid = True
        kn = 1
    if isvalid:
        print 'Keeping "%s"' %finord[kn-1]
        if finord[kn-1] != title:
            print 'Moving "%s" to "%s"' %(finord[kn-1],title)
            try:
                os.remove(title)
                pass
            except:
                print title,'already missing!'
            os.rename(finord[kn-1],title)
            finord.pop(kn-1)
            finord.remove(title)
        else:
            finord.pop(kn-1)
        for f in finord:
            print 'Removing "%s"...'%f
            try:
                os.remove(f)
                pass
            except:
                print f,'already missing!'
    else:
        if k==chr(27):
            sys.exit(1)
        else:
            print "Doing nothing"
    print ''


def main(rootdir=u'.'):
    """
    Walks across the file tree from {rootdir} looking for
    conflicted files. When these are found, handle them with
    handleConflicted() function
    """
    print 'Processing directory "%s"...' % rootdir
    lastName = None
    for root, subFolders, files in os.walk(rootdir):
        fileGroupDict = {}
        for f in files:
            m = re.search('^(.*)( \(.*[Cc][Oo][Nn][Ff].*\))([^\)]*)$', f)
            j = os.path.join(root,f)
            try:
                print j
            except:
                print 'unable to print filename'
            s = os.stat(j)
            if m != None:
                realname = m.group(1)
                realext = m.group(3)
                realf = os.path.join(root, realname+realext)
                desc = m.group(2)
            else:
                realf = j
                desc = '(current)'
            if not fileGroupDict.has_key(realf):
                fileGroupDict[realf] = []
            fileGroupDict[realf].append((desc, s.st_size, s.st_mtime))
        for realf,fileGroup in fileGroupDict.iteritems():
            if len(fileGroup) > 1:
                handleConflicted(realf,fileGroup)

getch = _find_getch()

if __name__ == '__main__':
    if len(sys.argv)==2:
        main(sys.argv[1])
    else:
        main('')
