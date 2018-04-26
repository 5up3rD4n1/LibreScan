from os import listdir
from shutil import copyfile
import random

from librescan.config import config, LS_DEV_PICS_PATH
from librescan.services import queue_service, ImageService, ProjectService
from librescan.utils import logger


class DevScannerService:
    def __init__(self):
        self.dev_pics = sorted(listdir(LS_DEV_PICS_PATH))
        self.image_service = ImageService()
        self.project_service = ProjectService()
        self.camera_config = None

    def take_pictures(self, p_index, p_image_ids=None):
        #try:
        dev_pics_index = []
        save_path = config.raw_folder() + '/'

        if not p_image_ids:
            p_image_ids = []
            pic_number = self.project_service.last_pic_number()
            dev_pics_index.append(pic_number % len(self.dev_pics))
            pic_number += 1
            p_image_ids.append("lsp" + str(pic_number).zfill(5))
            dev_pics_index.append(pic_number % len(self.dev_pics))
            pic_number += 1
            p_image_ids.append("lsp" + str(pic_number).zfill(5))
            self.image_service.insert_pics(p_index, p_image_ids)
            self.project_service.update_last_picture_id(pic_number)
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

        #except Exception as err:
         #   logger.error("Exception while taking pictures." + str(err))
          #  return []
        try:
            self.image_service.rotate_photos(p_image_ids[0], p_image_ids[1])
        except Exception as err:
            logger.error("Exception while rotating pictures." + str(err))
            return []
        queue_service.push(p_image_ids)
        return p_image_ids
