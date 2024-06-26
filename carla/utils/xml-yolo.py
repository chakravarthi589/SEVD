import os
import xml.etree.ElementTree as ET
import shutil


def convert_voc_to_yolo(xml_path, names_dict):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find('size')
    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)

    yolo_lines = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        class_id = names_dict.get(name)
        if class_id is not None:
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text) / img_width
            ymin = float(bndbox.find('ymin').text) / img_height
            xmax = float(bndbox.find('xmax').text) / img_width
            ymax = float(bndbox.find('ymax').text) / img_height

            width = xmax - xmin
            height = ymax - ymin

            center_x = (xmin + xmax) / 2
            center_y = (ymin + ymax) / 2

            yolo_line = f"{class_id} {center_x} {center_y} {width} {height}"
            yolo_lines.append(yolo_line)

    return yolo_lines


def convert_folder(input_folder, output_folder, names_dict):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_path = os.path.join(input_folder, filename)
            yolo_lines = convert_voc_to_yolo(xml_path, names_dict)

            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(output_folder, txt_filename)
            with open(txt_path, 'w') as txt_file:
                for line in yolo_lines:
                    txt_file.write(line + '\n')


if __name__ == '__main__':
    input_folders = [
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/rgb/rgb_camera-back",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/rgb/rgb_camera-back-left",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/rgb/rgb_camera-back-right",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/rgb/rgb_camera-front",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/rgb/rgb_camera-front-left",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/rgb/rgb_camera-front-right",

    "/home/apg/manideep/carla/out/ego-d5/ego0/images/dvs/dvs_camera-back",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/dvs/dvs_camera-back-left",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/dvs/dvs_camera-back-right",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/dvs/dvs_camera-front",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/dvs/dvs_camera-front-left",
    "/home/apg/manideep/carla/out/ego-d5/ego0/images/dvs/dvs_camera-front-right",
    ]

    names_dict = {'car': 0, 'truck': 1, 'van': 2,
                  'pedestrian': 3, 'motorcycle': 4, 'bicycle': 5}

    for input_folder in input_folders:
        if "images" in input_folder:
            output_folder = input_folder.replace("images", "labels")
            convert_folder(input_folder, output_folder, names_dict)
            print("Done yolo conversion @ ", input_folder)
            xml_folder = input_folder.replace("images", "annotations")
            print(xml_folder)
            os.makedirs(xml_folder, exist_ok=True)
            xml_files = [f for f in os.listdir(
                input_folder) if not f.endswith('.png')]
            for xml_file in xml_files:
                xml_path = os.path.join(input_folder, xml_file)
                shutil.move(xml_path, os.path.join(xml_folder, xml_file))
            print("Done moved annotations @ ", input_folder)
        else:
            print("error")
