from jpegtran import JPEGImage
import os

from librescan.config import config


class ImageService:

    @staticmethod
    def convert_image(image):
        temp = image.split('.')
        new_image = temp[0]
        new_image = new_image + ".jpg"        
        os.system("convert "+image+" "+new_image)   

    # TODO: probably needs to configure a project img format
    @staticmethod
    def image_path(p_project_id, p_image_id):
        config.change_project(p_project_id)
        return f'{config.raw_folder()}/{p_image_id}.jpg'

    @staticmethod
    def thumbnail(p_project_id, p_image_id, height, width):
        config.change_project(p_project_id)
        path = f'{config.raw_folder()}/{p_image_id}.jpg'
        image = JPEGImage(path)
        image = image.downscale(height, width)
        return image.as_blob()
