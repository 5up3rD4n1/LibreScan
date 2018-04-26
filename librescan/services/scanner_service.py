from librescan.utils.camera.impl.chdkptpPT import ChdkptpPT
from librescan.services import ImageService

from librescan.config import config
from librescan.utils import logger


class ScannerService:

    def __init__(self, p_pic_number=0):
        self.camera_config = None
        self.pic_number = p_pic_number
        self.cam_driver = ChdkptpPT()
        self.images_service = ImageService()

    def take_pictures(self, p_index, p_image_ids=None):
        try:
            save_path = config.raw_folder() + '/'

            if not p_image_ids:
                p_image_ids = []
                self.pic_number += 1
                p_image_ids.append("lsp" + str(self.pic_number).zfill(5))
                self.pic_number += 1
                p_image_ids.append("lsp" + str(self.pic_number).zfill(5))
                self.cam_driver.shoot(save_path, p_image_ids)
                self.images_service.insert_pics(p_index, p_image_ids)
                self.images_service.update_last_picture_id(self.pic_number)
            else:
                self.cam_driver.shoot(save_path, p_image_ids)
        except Exception as err:
            logger.error("Exception while taking pictures." + str(err))
            return -1
        try:
            self.images_service.rotate_photos(p_image_ids[0], p_image_ids[1])
        except Exception as err:
            logger.error("Exception while rotating pictures." + str(err))
            return -1
        return p_image_ids
