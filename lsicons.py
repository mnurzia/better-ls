#-*- coding: utf-8 -*-
from os import path
import subprocess, re, glob

#File extension descriptions.
#Format: "EXTENSION": ["ICON","COLOR CODE"]
extensions = {":FILE":	["","216"],
    ":DIRECTORY":	["","159"],
    "7z":			["","229"],
    "ai":			["","252"],
    "bat":			["","85"],
    "bmp":			["","252"],
    "bz":			["","229"],
    "bz2":			["","229"],
    "c":			["","85"],
    "c++":			["","85"],
    "cc":			["","85"],
    "clj":			["","85"],
    "cljc":			["","85"],
    "cljs":			["","85"],
    "coffee":		["","85"],
    "conf":			["","85"],
    "cp":			["","85"],
    "cpp":			["","85"],
    "css":			["","85"],
    "cxx":			["","85"],
    "d":			["","85"],
    "dart":			["","85"],
    "db":			["","85"],
    "diff":			["","85"],
    "dump":			["","105"],
    "edn":			["","85"],
    "ejs":			["","85"],
    "erl":			["","85"],
    "f#":			["","85"],
    "fish":			["","85"],
    "fs":			["","85"],
    "fsi":			["","85"],
    "fsscript":		["","85"],
    "fsx":			["","85"],
    "gif":			["","252"],
    "go":			["","85"],
    "gz":			["","229"],
    "hbs":			["","85"],
    "hrl":			["","85"],
    "hs":			["","85"],
    "htm":			["","85"],
    "html":			["","85"],
    "ico":			["","252"],
    "ini":			["","85"],
    "java":			["","85"],
    "jl":			["","85"],
    "jpeg":			["","252"],
    "jpg":			["","252"],
    "js":			["","85"],
    "json":			["","85"],
    "jsx":			["","85"],
    "less":			["","85"],
    "lhs":			["","85"],
    "lua":			["","85"],
    "markdown":		["","105"],
    "md":			["","105"],
    "ml":			["λ","85"],
    "mli":			["λ","85"],
    "mustache":		["","85"],
    "php":			["","85"],
    "pl":			["","85"],
    "pm":			["","85"],
    "png":			["","252"],
    "psb":			["","252"],
    "psd":			["","252"],
    "py":			["","85"],
    "pyc":			["","85"],
    "pyd":			["","85"],
    "pyo":			["","85"],
    "rb":			["","85"],
    "rlib":			["","85"],
    "rs":			["","85"],
    "rss":			["","105"],
    "scala":		["","85"],
    "scss":			["","85"],
    "sh":			["","85"],
    "slim":			["","85"],
    "sln":			["","85"],
    "sql":			["","85"],
    "styl":			["","85"],
    "suo":			["","85"],
    "t":			["","105"],
    "tar":			["","229"],
    "ts":			["","252"],
    "twig":			["","85"],
    "txt":			["","105"],
    "vim":			["","85"],
    "xul":			["","85"],
    "xz":			["","229"],
    "yml":			["","85"],
    "zip":			["","229"],
}

#Formats colors. Makes printing a bit easier.

def colorfmt(c):
    return "\x1b[38;5;%sm" % c

files = glob.glob("*")
formattedfiles = []

for f in sorted(files,key=lambda v: v.upper(),):
    if path.isfile(f):
        (name,ext) = path.splitext(f)
        ext = ext.replace(".","")
        if ext in extensions:
            formattedfiles.append(("%s %s" % (extensions[ext][0],f),colorfmt(extensions[ext][1])))
        if ext not in extensions:
            formattedfiles.append(("%s %s" % (extensions[":FILE"][0],f),colorfmt(extensions[":FILE"][1])))
    if not path.isfile(f):
        formattedfiles.append(("%s %s" % (extensions[":DIRECTORY"][0],f),colorfmt(extensions[":DIRECTORY"][1])))

fstr = ''
for f in formattedfiles:
    fstr += f[0]+"\n"

#Temporary file because I can't pipe the string to column yet - limitation (hdd speed)
tmpfile = open("lsfile","w")
tmpfile.write(fstr)
tmpfile.close()
output = subprocess.check_output("cat lsfile | column -c $(tput cols); rm -rf lsfile",shell=True).decode('utf-8') # Yes, I know I'm using shell=True. One reason why you SHOULD NOT give this program full permissions.

for f in formattedfiles:
    try:
        # Python 2
        f = [x.decode('utf8') for x in f]
    except AttributeError:
        # Python 3
        pass
    output = output.replace(f[0],f[1]+f[0])

print(output.strip('\n'))
