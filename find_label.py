import os
import argparse
import glob
import xml.etree.ElementTree as ET

def finder(path, label):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            if member[0].text == label:
                print(root.find('filename').text)

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description = "XML to CSV")
    ap.add_argument("-d", "--data", required = True,
        help="path to data")
    ap.add_argument("-l", "--label", required = True,
        help="label name")
    args = vars(ap.parse_args())
    image_path = os.path.join(args["data"])
    for folder in ['train','eval']:
        print(image_path + folder)
        xml_df = finder(image_path + folder, args["label"])
