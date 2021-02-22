from argparse import Namespace
import time
import glob
import os

options = Namespace()
options.verbosity = 1
def set_option(k,v):
    if k is not None:
        vars(options)[k] = v
started = 0
def start(*msg):
    if options.verbosity > 0:
        global started
        if msg:
            print(" ".join(map(str,msg)).ljust(60),"... ",end='',flush=True)
        started = time.time()
def end(end='\n'):
    if options.verbosity > 0:
        global started
        print("%.3f seconds   " % (time.time()-started),end=end,flush=True)
        started = time.time()
def file_size(file_name,end='\n'):
    from os import stat
    if options.verbosity > 0:
        print("%.0fK" % (stat(file_name).st_size/1024),end=end)
def status(*msg,end='\n'):
    if options.verbosity > 0:
        print(' '.join(map(str,msg)),end=end)

def convert2relative(width, height, coords):
    coords = list(coords)
    coords[::2], coords[1::2] = (float(x)/width for x in coords[::2]), (float(x)/height for x in coords[::2])
    return coords

def load_files(files_path,ext="jpg"):
    files_path_extension = files_path.split('.')[-1]
    if files_path_extension == ext:
        return [files_path]
    if files_path_extension == "files":
        with open(files_path, "rt") as f:
            return f.read().splitlines()
    return glob.glob(os.path.join(files_path, "*."+ext))
