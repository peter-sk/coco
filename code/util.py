from argparse import Namespace
import time

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
