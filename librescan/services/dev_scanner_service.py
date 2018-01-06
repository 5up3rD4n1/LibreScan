from jpegtran import JPEGImage
from os import listdir
from os import remove
from shutil import copyfile
import time
import yaml

from librescan.models import CameraConfig
from librescan.config import config
from librescan.services import queue_service


class DevScannerService:
    def __init__(self):
        self.dev_pics_dir = 'resources/devModePics/'
        self.dev_pics = sorted(listdir(self.dev_pics_dir))
        self.dev_pics_index = [0, 1]
        self.camera_config = None

    def set_camera_config(self):
        self.camera_config = self.get_configuration()

    def get_configuration(self):
        f = open(config.projects_file_path())
        data_map = yaml.safe_load(f)["camera"]
        f.close()
        return CameraConfig(data_map["zoom"], data_map["iso"])

    def take_pictures(self):
        try:
            pic_names = []
            save_path = config.raw_folder() + '/'
            pic_number = self.get_last_pic_number()

            pic_number += 1
            pic_names.append("lsp" + str(pic_number).zfill(5))
            pic_number += 1
            pic_names.append("lsp" + str(pic_number).zfill(5))

            # Copy development pics (/resources/devModePics) in the raw dir.
            dev_pic = self.dev_pics_dir + self.dev_pics[self.dev_pics_index[0]]
            dest_path = save_path + pic_names[0] + ".jpg"
            copyfile(dev_pic, dest_path)
            dev_pic = self.dev_pics_dir + self.dev_pics[self.dev_pics_index[1]]
            dest_path = save_path + pic_names[1] + ".jpg"
            copyfile(dev_pic, dest_path)

            # Increase the dev pictures index (in a circular way).
            self.dev_pics_index[0] = ((self.dev_pics_index[0] + 2)
                                      % len(self.dev_pics))
            self.dev_pics_index[1] = ((self.dev_pics_index[1] + 2)
                                      % len(self.dev_pics))

            self.insert_pics_to_file(-1, pic_names)
            self.update_last_pic_number(pic_number)
        except:
            print("Exception while taking pictures.")
            return -1
        try:
            self.rotate_photos(pic_names[0], pic_names[1])
        except:
            print("Exception while rotating pictures.")
            return -1
        queue_service.push(pic_names)
        return pic_names

    def prepare_cams(self):
        print("Preparing cameras...")

    def rotate_photos(self, p_left_photo, p_right_photo):
        pictures_found = False
        tries = 0
        while not pictures_found:
            try:
                save_path = config.raw_folder()

                left = JPEGImage(f'{save_path}/{p_left_photo}.jpg')
                right = JPEGImage(f'{save_path}/{p_right_photo}.jpg')

                left.rotate(270).save(f'{save_path}/{p_left_photo}.jpg')
                right.rotate(90).save(f'{save_path}/{p_right_photo}.jpg')
                pictures_found = True
            except:
                print('Pictures not found yet')
                time.sleep(0.5)
                if tries > 20:
                    raise Exception
            tries += 1

    def delete_photos(self, p_photo_list):
        pics_file = config.pics_file_path()
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()

        for photo in p_photo_list:
            remove(config.raw_folder() + photo + ".jpg")
            contents.remove(photo + '\n')

        f = open(pics_file, "w")
        f.writelines(contents)
        f.close()

    def update_last_pic_number(self, p_pic_number):
        config_path = config.project_config_file_path()
        data_map = self.get_file_data(config_path)
        data_map['camera']['last-pic-number'] = p_pic_number
        f = open(config_path, 'w')
        f.write(yaml.dump(data_map, default_flow_style=False,
                allow_unicode=True))
        f.close()

    def insert_pics_to_file(self, p_index, pic_list):
        pics_file = config.pics_file_path()
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()

        if p_index == -1:
            p_index = len(contents) - 1

        for pic in pic_list:
            contents.insert(p_index + 1, pic + '\n')
            p_index += 1

        f = open(pics_file, "w")
        f.writelines(contents)
        f.close()

    def get_last_photo_names(self):
        pics_file = config.pics_file_path()
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()

        last_pics = []
        if len(contents) > 1:
            last_pics = contents[-2:]
        return last_pics

    def recalibrate(self):
        print("Recalibrating cameras....")
        return 1

    @staticmethod
    def get_file_data(p_path):
        f = open(p_path)
        data_map = yaml.safe_load(f)
        f.close()
        return data_map

    @classmethod
    def get_last_pic_number(cls):
        config_path = config.project_config_file_path()
        data_map = cls.get_file_data(config_path)
        return int(data_map['camera']['last-pic-number'])
