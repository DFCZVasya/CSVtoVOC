
import os
import xml.etree.cElementTree as ET
from PIL import Image
import csv

#ANNOTATIONS_DIR_PREFIX = "D:/dataset/rtsd-public/fullframes/razmetka/Лев/18_разметка/razmetka/"

DESTINATION_DIR = "D:/dataset/train_annot/"



def create_root(file_prefix, width, height):
    root = ET.Element("annotations")
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
    ET.SubElement(root, "folder").text = "images"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix))


def read_file():
    #image_file_name = "{}.jpg".format(file_prefix)
    #img = Image.open("{}/{}".format("images", image_file_name))
    w = 640
    h = 480
    lastfilename = ''
    with open('full-gt.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        voc_labels = []
        for line in reader:
            voc = []
            voc.append("sign")
            voc.append(int(int(line["x_from"]) / 2))
            voc.append(int(int(line["y_from"]) / 1.5))
            voc.append(int((int(line["x_from"]) + int(line["width"])) / 2))
            voc.append(int((int(line["y_from"]) + int(line["height"])) / 1.5))
            if lastfilename == line["filename"]:
                voc_labels.append(voc)
            else:
                voc_labels = []
                voc_labels.append(voc)
            fname = line["filename"]
            lastfilename = line["filename"]
            create_file(fname[:-4], w, h, voc_labels)
            print("Processing complete for file " + fname)


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    read_file()


if __name__ == "__main__":
    start()
