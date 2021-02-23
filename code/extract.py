#!/usr/bin/env python3
from pycocotools.coco import COCO
import sys
import time
import os
from os.path import join
import numpy as np
from util import start, end, status, options, convert2relative, get_started

train_coco = COCO('data/person_keypoints_train2017.json')

def get_meta(coco):
    ids = list(coco.imgs.keys())
    for i, img_id in enumerate(ids):
        img_meta = coco.imgs[img_id]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        img_file_name = img_meta['file_name']
        w = img_meta['width']
        h = img_meta['height']
        anns = coco.loadAnns(ann_ids)
        yield [img_id, img_file_name, w, h, anns]

def main():
    start("Extracting images")
    total = 0
    selected = 0
    for img_id, img_fname, width, height, meta in get_meta(train_coco):
        total += 1
        if options.verbosity > 0 and total % 1000 == 0:
            print("(%d, %.1fs)" % (total,time.time()-get_started()), end='')
            sys.stdout.flush()
        takeit = False
        for m in meta:
            bbox = m['bbox']
            area = bbox[2]*bbox[3]/width/height
            if not m['iscrowd']:# and area >= 0.05:
                takeit = True
        if not takeit:
            continue
        #print(img_fname,width,height)
        selected += 1
        os.system("cp {} {}".format(join('data/train2017',img_fname),join('data/selected/{}'.format(img_id % 10),img_fname)))
        f = open(join('data/selected/{}'.format(img_id % 10)," ".join(img_fname.split(".")[:-1])+".annotated.txt"),"wt")
        for m in meta:
            bbox = m['bbox']
            area = bbox[2]*bbox[3]/width/height
            if m['iscrowd']:# and area < 0.05:
                continue
            bbox = m['bbox']
            #print(bbox)
            bbox = (bbox[0]+bbox[2]/2,bbox[1]+bbox[3]/2,bbox[2],bbox[3])
            #print(bbox)
            bbox = " ".join("{:.6f}".format(x) for x in convert2relative(width, height, bbox))
            #print(bbox)
            for pts in m['segmentation']:
                outline = " ".join("{:.6f}".format(x) for x in convert2relative(width, height, pts))
                f.write("0 {} 100.000000 {}\n".format(bbox,outline))
        f.close()
    end('')
    status(selected,"out of",total)

if __name__ == "__main__":
    main()
