#!/usr/bin/env python3
import sys
import os
import cv2
import time
from os.path import join
import numpy as np
from util import start, end, options, convert2absolute, load_files, get_started

FROM = "data/selected_train2017"
TO = "data/coco_train"

def main():
    for i in range(10):
        from_path = join(FROM,str(i))
        start("Collecting images in",from_path)
        txts = load_files(from_path,ext="annotated.txt")
        total = 0
        for from_txt_fname in txts:
            total += 1
            if options.verbosity > 0 and total % 1000 == 0:
                print("(%d, %.1fs)" % (total,time.time()-get_started()), end='')
                sys.stdout.flush()
            from_img_fname = ".".join(from_txt_fname.split(".")[:-2])+".jpg"
            to_img_fname = join(TO,".".join(from_img_fname[len(from_path)+3:].split(".")[:-1])+".JPG")
            to_txt_fname = ".".join(to_img_fname.split(".")[:-1])+".txt"
            os.system("cp {} {}".format(from_img_fname,to_img_fname))
            f = open(from_txt_fname,"rt")
            g = open(to_txt_fname,"wt")
            for line in f.readlines():
                coords = line.split()
                g.write("{}\n".format(" ".join(coords[:5])))
            f.close()
            g.close()
        end()

if __name__ == "__main__":
    main()
