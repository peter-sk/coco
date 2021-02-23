#!/usr/bin/env python3
import sys
import os
import cv2
import time
from os.path import join
import numpy as np
from util import start, end, options, convert2absolute, load_files, get_started

def main():
    for i in range(10):
        start("Rendering images in data/selected/",i)
        txts = load_files("data/selected/"+str(i),ext="annotated.txt")
        txts.extend(load_files("data/selected/"+str(i),ext="detected.txt"))
        txts = txts[::2]+txts[1::2]
        total = 0
        for txt_fname in txts:
            total += 1
            if options.verbosity > 0 and total % 1000 == 0:
                print("(%d, %.1fs)" % (total,time.time()-get_started()), end='')
                sys.stdout.flush()
            img_fname = ".".join(txt_fname.split(".")[:-2])+".jpg"
            ext = txt_fname.split(".")[-2]
            img = cv2.imread(join(img_fname))
            height, width, _ = img.shape
            #print(txt_fname,width,height)
            f = open(txt_fname,"rt")
            for line in f.readlines():
                coords = line.split()
                #print(coords[1:5])
                x,y,w,h = convert2absolute(width,height,coords[1:5])
                #print(x,y,w,h)
                ul = int(x-w/2),int(y-h/2)
                dr = int(x+w/2),int(y+h/2)
                #print(ul,dr)
                bbox = cv2.rectangle(img,ul,dr,(255,255,0),3)
                pts = convert2absolute(width,height,coords[6:])
                pts = np.array(pts,dtype=np.int32).reshape((-1,1,2))
                outline = cv2.polylines(img,[pts],True,(255,0,255),2)
            f.close()
            cv2.imwrite(join(img_fname.split(".jpg")[0]+"."+ext+".jpg"),img)
        end()

if __name__ == "__main__":
    main()
