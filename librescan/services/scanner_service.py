from librescan.utils.camera.impl.chdkptpPT import ChdkptpPT
from librescan.services import ImageService, ProjectService
from librescan.services import queue_service
from librescan.config import config
from librescan.utils import logger


class ScannerService:

    def __init__(self):
        self.camera_config = None
        self.cam_driver = ChdkptpPT()
        self.image_service = ImageService()
        self.project_service = ProjectService()

    def take_pictures(self, p_index, p_image_ids=None):
        try:
            pic_number = self.project_service.last_pic_number()
            save_path = config.raw_folder() + '/'

            if not p_image_ids:
                p_image_ids = []
                pic_number += 1
                p_image_ids.append("lsp" + str(pic_number).zfill(5))
                pic_number += 1
                p_image_ids.append("lsp" + str(pic_number).zfill(5))
                self.cam_driver.shoot(save_path, p_image_ids)
                self.image_service.insert_pics(p_index, p_image_ids)
                self.project_service.update_last_picture_id(pic_number)
            else:
                self.cam_driver.shoot(save_path, p_image_ids)
        except Exception as err:
            logger.error("Exception while taking pictures." + str(err))
            return []
        try:
            self.image_service.rotate_photos(p_image_ids[0], p_image_ids[1])
        except Exception as err:
            logger.error("Exception while rotating pictures." + str(err))
            return []
        queue_service.push(p_image_ids)
        return p_image_ids
