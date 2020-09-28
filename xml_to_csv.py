import os
import argparse
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description = "XML to CSV")
    ap.add_argument("-d", "--data", required = True,
        help="path to data")
    args = vars(ap.parse_args())
    image_path = os.path.join(args["data"])
    for folder in ['train','eval']:
        print(folder)
        print(image_path + folder)
        xml_df = xml_to_csv(image_path + folder)
        xml_df.to_csv((folder + '_labels.csv'), index=None)
        print('Successfully converted ' + folder + ' xml to csv.')