#!/usr/bin/env python3
from pycocotools.coco import COCO
import sys
import os
import cv2
from os.path import join
import numpy as np
from util import start, end, status, options, convert2relative

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

start("Extracting images")
total = 0
selected = 0
for img_id, img_fname, width, height, meta in get_meta(train_coco):
    if img_id > 100:
        continue
    total += 1
    if options.verbosity > 0 and total % 1000 == 0:
        print("(%d, %.1fs)" % (total,time.time()-started), end='')
        sys.stdout.flush()
    takeit = False
    for m in meta:
        if not m['iscrowd'] and m['area'] >= 2000:
            takeit = True
    if not takeit:
        continue
    selected += 1
    os.system("cp {} {}".format(join('data/train2017',img_fname),join('data/selected',img_fname)))
    f = open(join('data/selected'," ".join(img_fname.split(".")[:-1])+".annotated.txt"),"wt")
    for m in meta:
        if m['iscrowd'] or m['area'] < 2000:
            continue
        bbox = " ".join("{:.6f}".format(x) for x in convert2relative(width, height, m['bbox']))
        for pts in m['segmentation']:
            outline = " ".join("{:.6f}".format(x) for x in convert2relative(width, height, pts))
            f.write("0 {} 100.000000 {}".format(bbox,outline))
    f.close()
end('')
status(selected,"out of",total)
