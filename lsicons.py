#!/usr/bin/env python
#-*- coding: utf-8 -*-
from os import path
import os
import subprocess
import glob
import stat
from pwd import getpwuid
from optparse import OptionParser


# File extension descriptions.
# Format: "EXTENSION": [u"ICON","COLOR CODE"]
EXTENSIONS = {":FILE":	[u"", "216"],
              ":DIRECTORY":	[u"", "159"],
              "7z":			[u"", "229"],
              "ai":			[u"", "252"],
              "bat":		[u"", "85"],
              "bmp":		[u"", "252"],
              "bz":			[u"", "229"],
              "bz2":		[u"", "229"],
              "c":			[u"", "85"],
              "c++":		[u"", "85"],
              "cc":			[u"", "85"],
              "clj":		[u"", "85"],
              "cljc":		[u"", "85"],
              "cljs":		[u"", "85"],
              "coffee":		[u"", "85"],
              "conf":		[u"", "85"],
              "cp":			[u"", "85"],
              "cpp":		[u"", "85"],
              "css":		[u"", "85"],
              "cxx":		[u"", "85"],
              "d":			[u"", "85"],
              "dart":		[u"", "85"],
              "db":			[u"", "85"],
              "diff":		[u"", "85"],
              "dump":		[u"", "105"],
              "edn":		[u"", "85"],
              "ejs":		[u"", "85"],
              "erl":		[u"", "85"],
              "f#":			[u"", "85"],
              "fish":		[u"", "85"],
              "fs":			[u"", "85"],
              "fsi":		[u"", "85"],
              "fsscript":	[u"", "85"],
              "fsx":		[u"", "85"],
              "gif":		[u"", "252"],
              "go":			[u"", "85"],
              "gz":			[u"", "229"],
              "hbs":		[u"", "85"],
              "hrl":		[u"", "85"],
              "hs":			[u"", "85"],
              "htm":		[u"", "85"],
              "html":		[u"", "85"],
              "ico":		[u"", "252"],
              "ini":		[u"", "85"],
              "java":		[u"", "85"],
              "jl":			[u"", "85"],
              "jpeg":		[u"", "252"],
              "jpg":		[u"", "252"],
              "js":			[u"", "85"],
              "json":		[u"", "85"],
              "jsx":		[u"", "85"],
              "less":		[u"", "85"],
              "lhs":		[u"", "85"],
              "lua":		[u"", "85"],
              "markdown":	[u"", "105"],
              "md":			[u"", "105"],
              "ml":			[u"λ", "85"],
              "mli":		[u"λ", "85"],
              "mustache":	[u"", "85"],
              "php":		[u"", "85"],
              "pl":			[u"", "85"],
              "pm":			[u"", "85"],
              "png":		[u"", "252"],
              "psb":		[u"", "252"],
              "psd":		[u"", "252"],
              "py":			[u"", "85"],
              "pyc":		[u"", "85"],
              "pyd":		[u"", "85"],
              "pyo":		[u"", "85"],
              "rb":			[u"", "85"],
              "rlib":		[u"", "85"],
              "rs":			[u"", "85"],
              "rss":		[u"", "105"],
              "scala":		[u"", "85"],
              "scss":		[u"", "85"],
              "sh":			[u"", "85"],
              "slim":		[u"", "85"],
              "sln":		[u"", "85"],
              "sql":		[u"", "85"],
              "styl":		[u"", "85"],
              "suo":		[u"", "85"],
              "t":			[u"", "105"],
              "tar":		[u"", "229"],
              "ts":			[u"", "252"],
              "twig":		[u"", "85"],
              "txt":		[u"", "105"],
              "vim":		[u"", "85"],
              "xul":		[u"", "85"],
              "xz":			[u"", "229"],
              "yml":		[u"", "85"],
              "zip":		[u"", "229"],
              }

# Formats colors. Makes printing a bit easier.
def colorfmt(c):
    return "\x1b[38;5;%sm" % c

def permissions_to_unix_name(st):
    is_dir = 'd' if stat.S_ISDIR(st.st_mode) else '-'
    dic = {'7': 'rwx', '6': 'rw-', '5': 'r-x', '4': 'r--', '0': '---'}
    perm = str(oct(st.st_mode)[-3:])
    return is_dir + ''.join(dic.get(x, x) for x in perm)

def get_user_name(file_stat):
    try:
        return getpwuid(file_stat.st_uid).pw_name
    except KeyError:
        return ""

def get_file_size(file_stat):
    size = file_stat.st_size
    if size <= 1024:
        return "%d B" % size
    size /= 1024

    if size <= 1024:
        return "%d KB" % size
    size /= 1024

    if size <= 1024:
        return "%d MB" % size
    size /= 1024

    return "%d GB" % size

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option(
        "-l",
        "--list",
        action="store_true",
        default=False,
     dest="is_list")
    parser.add_option("-d", "--dir", dest="dir", default='')
    (options, args) = parser.parse_args()

    files = glob.glob(options.dir + '.*') + glob.glob(options.dir + '*')
    formattedfiles = []

    for f in sorted(files, key=lambda v: v.upper(),):
        file_line = ''
        file_color = ''
        if path.isfile(f):
            (name, ext) = path.splitext(f)
            ext = ext.replace(".", "")
            if ext in EXTENSIONS:
                file_line = ("%s %s" % (EXTENSIONS[ext][0], f))
                file_color = colorfmt(EXTENSIONS[ext][1])
            if ext not in EXTENSIONS:
                file_line = ("%s %s" % (EXTENSIONS[u":FILE"][0], f))
                file_color = colorfmt(EXTENSIONS[u":FILE"][1])
        else:
            file_line = ("%s %s" % (EXTENSIONS[u":DIRECTORY"][0], f))
            file_color = colorfmt(EXTENSIONS[u":DIRECTORY"][1])
        if options.is_list:
            try:
                file_stat = os.stat(f)
                file_line = u"{:<15}{:<10}{:<10}{}".format(
                                    permissions_to_unix_name(file_stat),
                                    get_user_name(file_stat),
                                    get_file_size(file_stat), file_line)
            except OSError:
                file_line = f
        formattedfiles.append((file_line, file_color))
    fstr = ''
    for f in formattedfiles:
        fstr += f[0]+"\n"

    if not options.is_list:
        # Temporary file because I can't pipe the string to column yet -
        # limitation (hdd speed)
        tmpfile = open("lsfile", "w")
        try:
            # Python 3
            tmpfile.write(fstr)
        except UnicodeEncodeError:
            # Python 2
            tmpfile.write(str(fstr.encode('utf-8')))
        tmpfile.close()
        # Yes, I know I'm using shell=True. One reason why you SHOULD NOT give
        # this program full permissions.
        output = subprocess.check_output(
            "cat lsfile | column -c $(tput cols); rm -rf lsfile",
            shell=True).decode('utf-8')
    else:
        output = fstr

    for f in formattedfiles:
        output = output.replace(f[0], f[1]+f[0])

    print(output.strip('\n'))
