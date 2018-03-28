from jpegtran import JPEGImage
import os

from PIL import Image

from librescan.config import config
from librescan.models import ProjectPhoto


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

    @staticmethod
    def tif(p_project_id, p_image_id, height, width):
        config.change_project(p_project_id)
        path = f'{config.processed_folder()}/{p_image_id}.tif'
        output_path = f'{config.processed_folder()}/{p_image_id}.jpg'
        im = Image.open(path)
        im.save(output_path, 'JPEG', quality=100)
        jpg_image = JPEGImage(output_path)
        jpg_image = jpg_image.downscale(height, width)
        return jpg_image.as_blob()

    @classmethod
    def get_all(cls, p_project_id):
        config.change_project(p_project_id)
        contents = cls.__file_content()
        return [ProjectPhoto(image_id.rstrip(), p_project_id) for image_id in contents]

    @staticmethod
    # NOTE: There are many of this functions all over the project
    # TODO: extract this to a file service or something similar
    def __file_content():
        pics_file = config.pics_file_path()
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()
        return contents
