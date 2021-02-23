#!/usr/bin/env python3
import sys
import os
import cv2
import time
from os.path import join
import numpy as np
from util import start, end, status, options, convert2absolute, load_files, get_started

def main():
    for i in range(10):
        start("Detecting outlier candidates in data/selected/",i)
        txts = load_files("data/selected/"+str(i),ext="detected.txt")
        total = 0
        selected = 0
        for txt_fname in txts:
            total += 1
            if options.verbosity > 0 and total % 1000 == 0:
                print("(%d, %.1fs)" % (total,time.time()-get_started()), end='')
                sys.stdout.flush()
            img_fname = ".".join(txt_fname.split(".")[:-2])+".jpg"
            img = cv2.imread(join(img_fname))
            height, width, _ = img.shape
            #print(txt_fname,width,height)
            f = open(txt_fname,"rt")
            g = None
            takeIt = False
            for line in f.readlines():
                coords = line.split()
                #print(coords[1:5])
                x,y,w,h = convert2absolute(width,height,coords[1:5])
                confidence = float(coords[5])
                if w*h/width/height < 0.05 or confidence >= 30:
                    continue
                takeIt = True
                if g is None:
                    g = open(".".join(txt_fname.split(".")[:-2])+".outlier.txt","wt")
                g.write(line)
                #print(x,y,w,h)
                ul = int(x-w/2),int(y-h/2)
                dr = int(x+w/2),int(y+h/2)
                #print(ul,dr)
                bbox = cv2.rectangle(img,ul,dr,(255,255,0),3)
            f.close()
            if g is not None:
                g.close()
            if takeIt:
                selected += 1
                cv2.imwrite(join(img_fname.split(".jpg")[0]+".outlier.jpg"),img)
        end('')
        status(selected,"out of",total)

if __name__ == "__main__":
    main()
