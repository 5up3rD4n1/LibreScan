from jpegtran import JPEGImage
from os import listdir
from os import remove
from shutil import copyfile
import time
import random
import yaml

from librescan.models import CameraConfig
from librescan.config import config, LS_DEV_PICS_PATH
from librescan.services import queue_service
from librescan.utils import logger


class DevScannerService:
    def __init__(self):
        self.dev_pics = sorted(listdir(LS_DEV_PICS_PATH))
        self.camera_config = None

    def set_camera_config(self):
        self.camera_config = self.get_configuration()

    @staticmethod
    def get_configuration():
        f = open(config.projects_file_path())
        data_map = yaml.safe_load(f)["camera"]
        f.close()
        return CameraConfig(data_map["zoom"], data_map["iso"])

    def take_pictures(self, p_index, p_image_ids=None):
        try:
            dev_pics_index = []
            save_path = config.raw_folder() + '/'

            if not p_image_ids:
                p_image_ids = []
                pic_number = self.get_last_pic_number()
                dev_pics_index.append(pic_number % len(self.dev_pics))
                pic_number += 1
                p_image_ids.append("lsp" + str(pic_number).zfill(5))
                dev_pics_index.append(pic_number % len(self.dev_pics))
                pic_number += 1
                p_image_ids.append("lsp" + str(pic_number).zfill(5))
                self.insert_pics_to_file(p_index, p_image_ids)
                self.update_last_pic_number(pic_number)
            else:  # In case of retake, take any picture from the dev pics
                dev_pics_index.append(random.choice(range(len(self.dev_pics))))
                dev_pics_index.append(random.choice(range(len(self.dev_pics))))

            # Copy development pics (/resources/devModePics) in the raw dir.
            dev_pic = LS_DEV_PICS_PATH + '/' + self.dev_pics[dev_pics_index[0]]
            dest_path = save_path + p_image_ids[0] + ".jpg"
            copyfile(dev_pic, dest_path)
            dev_pic = LS_DEV_PICS_PATH + '/' + self.dev_pics[dev_pics_index[1]]
            dest_path = save_path + p_image_ids[1] + ".jpg"
            copyfile(dev_pic, dest_path)

        except Exception as err:
            logger.error("Exception while taking pictures." + str(err))
            return -1
        try:
            self.rotate_photos(p_image_ids[0], p_image_ids[1])
        except Exception as err:
            logger.error("Exception while rotating pictures." + str(err))
            return -1
        queue_service.push(p_image_ids)
        return p_image_ids

    @staticmethod
    def prepare_cams():
        logger.info("Preparing cameras...")

    @staticmethod
    def rotate_photos(p_left_photo, p_right_photo):
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
                logger.info('Pictures not found yet')
                time.sleep(0.5)
                if tries > 20:
                    raise Exception
            tries += 1

    @staticmethod
    def delete_photos(p_photo_list):
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

    @staticmethod
    def insert_pics_to_file(p_index, pic_list):
        pics_file = config.pics_file_path()
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()

        if p_index == -1:
            p_index = len(contents)

        for pic in pic_list:
            contents.insert(p_index, pic + '\n')
            p_index += 1

        f = open(pics_file, "w")
        f.writelines(contents)
        f.close()

    @staticmethod
    def get_last_photo_names():
        pics_file = config.pics_file_path()
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()

        last_pics = []
        if len(contents) > 1:
            last_pics = contents[-2:]
        return last_pics

    @staticmethod
    def recalibrate():
        logger.info("Recalibrating cameras....")
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
