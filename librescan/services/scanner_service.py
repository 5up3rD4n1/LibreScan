import time
from os import getenv
from os import remove
import yaml

from models.cameraConfig import CameraConfig
from utils.camera.impl.chdkptpPT import ChdkptpPT
from jpegtran import JPEGImage
from librescan.utils import logger


# TODO: Change all the paths with Config class
class ScannerService:
    def __init__(self, p_pic_number=0):
        self.working_dir = getenv("LS_PROJECT_PATH")
        self.camera_config = None
        self.pic_number = p_pic_number
        self.cam_driver = ChdkptpPT()

    def set_camera_config(self):
        self.camera_config = self.get_configuration()

    def get_configuration(self):
        config_path = self.working_dir + "/.projectConfig.yaml"
        f = open(config_path)
        data_map = yaml.safe_load(f)["camera"]
        f.close()
        return CameraConfig(data_map["zoom"], data_map["iso"])

    def take_pictures(self, p_index, p_image_ids=None):
        try:
            save_path = self.working_dir + '/raw/'

            if not p_image_ids:
                p_image_ids = []
                self.pic_number += 1
                p_image_ids.append("lsp" + str(self.pic_number).zfill(5))
                self.pic_number += 1
                p_image_ids.append("lsp" + str(self.pic_number).zfill(5))
                self.cam_driver.shoot(save_path, p_image_ids)
                self.insert_pics_to_file(p_index, p_image_ids)
                self.update_last_pic_number(self.pic_number)
            else:
                self.cam_driver.shoot(save_path, p_image_ids)
        except Exception as err:
            logger.error("Exception while taking pictures." + str(err))
            return -1
        try:
            self.rotate_photos(p_image_ids[0], p_image_ids[1])
        except Exception as err:
            logger.error("Exception while rotating pictures." + str(err))
            return -1
        return p_image_ids

    def prepare_cams(self):
        self.cam_driver.detect()
        self.cam_driver.prepare(self.camera_config)

    def rotate_photos(self, p_left_photo, p_right_photo):
        pictures_found = False
        tries = 0
        # NOTE: This can be replaced to use a file watch dog over the file system
        # then use the web socket to notify
        while not pictures_found:
            try:
                save_path = self.working_dir + '/raw/'

                left = JPEGImage(save_path + p_left_photo + ".jpg")
                right = JPEGImage(save_path + p_right_photo + ".jpg")

                left.rotate(270).save(save_path + p_left_photo + ".jpg")
                right.rotate(90).save(save_path + p_right_photo + ".jpg")
                pictures_found = True
            except Exception as err:
                logger.error('Pictures not found yet' + str(err))
                time.sleep(0.5)
                if tries > 20:
                    raise Exception
            tries += 1

    def delete_photos(self, p_photo_list):
        pics_file = self.working_dir + '/.pics.ls'
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()

        for photo in p_photo_list:
            remove(self.working_dir + "/raw/" + photo + ".jpg")
            contents.remove(photo + '\n')

        f = open(pics_file, "w")
        f.writelines(contents)
        f.close()

    def update_last_pic_number(self, p_pic_number):
        config_path = self.working_dir + "/.projectConfig.yaml"
        f = open(config_path)
        data_map = yaml.safe_load(f)
        f.close()
        data_map['camera']['last-pic-number'] = p_pic_number
        f = open(config_path, 'w')
        f.write(yaml.dump(data_map, default_flow_style=False, allow_unicode=True))
        f.close()

    def insert_pics_to_file(self, p_index, pic_list):
        pics_file = self.working_dir + '/.pics.ls'
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

    def get_last_photo_names(self):
        self.working_dir = getenv("LS_PROJECT_PATH")
        pics_file = self.working_dir + '/.pics.ls'
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()

        last_pics = []
        if len(contents) > 1:
            last_pics = contents[-2:]
        return last_pics

    def recalibrate(self):
        return self.cam_driver.calibrate()
