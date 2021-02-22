from pycocotools.coco import COCO
import sys
import os
import cv2
from os.path import join
import numpy as np
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

def convert2relative(width, height, coords):
    coords = list(coords)
    coords[::2], coords[1::2] = (float(x)/width for x in coords[::2]), (float(x)/height for x in coords[::2])
    return coords

train_coco = COCO('annotations/person_keypoints_train2017.json')

def get_meta(coco):
    ids = list(coco.imgs.keys())
    for i, img_id in enumerate(ids):
        img_meta = coco.imgs[img_id]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        # basic parameters of an image
        img_file_name = img_meta['file_name']
        w = img_meta['width']
        h = img_meta['height']
        # retrieve metadata for all persons in the current image
        anns = coco.loadAnns(ann_ids)
        yield [img_id, img_file_name, w, h, anns]

start("Selecting images")
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
#    img = cv2.imread(join('train2017',img_fname))
#    img = cv2.imwrite(join('selected',img_fname),img)
    os.system("cp {} {}".format(join('train2017',img_fname),join('selected',img_fname)))
    f = open(join('selected'," ".join(img_fname.split(".")[:-1])+".annotated.txt"),"wt")
    for m in meta:
        if m['iscrowd'] or m['area'] < 2000:
            continue
        bbox = " ".join("{:.6f}".format(x) for x in convert2relative(width, height, m['bbox']))
#        x,y,w,h = coords
#        ul = int(x),int(y)
#        dr = int(x+w),int(y+h)
#        bbox = cv2.rectangle(img,ul,dr,(255,255,0),3)
        for pts in m['segmentation']:
            outline = " ".join("{:.6f}".format(x) for x in convert2relative(width, height, pts))
            print("0 {} 100.000000 {}".format(bbox,outline),file=f)
#            pts = np.array(pts,dtype=np.int32).reshape((-1,1,2))
#            outline = cv2.polylines(img,[pts],True,(255,0,255),2)
    f.close()
#    cv2.imwrite(join('selected',img_fname.split(".jpg")[0]+'.annotated.jpg'),img)
    #cv2.imshow('image',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
end('')
status(selected,"out of",total)