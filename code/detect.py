#!/usr/bin/env python3
import argparse
import os
import os.path
import glob
import random
import time
import cv2
import numpy as np
import sys
from util import start, end, status, convert2relative, load_files

old_path = sys.path
os.chdir("darknet")
sys.path.append(".")
import darknet
os.chdir("..")
sys.path = old_path

def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, default="data/selected/",
                        help="image source. It can be a single image, a"
                        "txt with paths to them, or a folder. Image valid"
                        " formats are jpg, jpeg or png."
                        "If no input is given, ")
    parser.add_argument("--batch_size", default=1, type=int,
                        help="number of images to be processed at the same time")
    parser.add_argument("--weights", default="data/yolov4.weights",
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_false', default=True,
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--save_labels", action='store_false', default=True,
                        help="save detections bbox for each image in yolo format")
    parser.add_argument("--config_file", default="darknet/cfg/yolov4.cfg",
                        help="path to config file")
    parser.add_argument("--data_file", default="darknet/cfg/coco.data",
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.1,
                        help="remove detections with lower confidence")
    return parser.parse_args()

def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
    if args.input and not os.path.exists(args.input):
        raise(ValueError("Invalid image path {}".format(os.path.abspath(args.input))))

def image_detection(image_path, network, class_names, class_colors, thresh):
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections

def save_annotations(file_name, image, detections, class_names):
    with open(file_name, "w") as f:
        for label, confidence, bbox in detections:
            height, width, _ = image.shape
            relative_bbox = " ".join("{:.6f}".format(x) for x in convert2relative(width, height, bbox))
            if label == "person":
                #print(file_name,width,height,bbox,relative_bbox)
                f.write("0 {} {:.6f}\n".format(relative_bbox, float(confidence)))

def main():
    args = parser()
    check_arguments_errors(args)
    network, class_names, class_colors = darknet.load_network(
        args.config_file,
        args.data_file,
        args.weights,
        batch_size=args.batch_size
    )
    for i in range(10):
        images = load_files(args.input+"/"+str(i))
        for image_name in images:
            file_name = ".".join(image_name.split(".")[:-1]) + ".detected.txt"
            if os.path.exists(file_name):
                start("Existing detection for", image_name)
                status("SKIP")
                continue
            start("Detecting", image_name)
            image, detections = image_detection(image_name, network, class_names, class_colors, args.thresh)
            save_annotations(file_name, image, detections, class_names)
            end()

if __name__ == "__main__":
    main()
