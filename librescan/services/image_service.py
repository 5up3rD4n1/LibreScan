from jpegtran import JPEGImage
import os
from os import remove
from time import sleep

from PIL import Image

from librescan.config import config
from librescan.models import ProjectPhoto
from librescan.utils import (
    dict_from_yaml,
    write_dict,
    logger
)


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

    @staticmethod
    def get_all(cls, p_project_id):
        config.change_project(p_project_id)
        contents = cls.__file_content()
        return [ProjectPhoto(image_id.rstrip(), p_project_id) for image_id in contents]
    
    @staticmethod
    def rotate_photos(p_left_photo, p_right_photo):
        pictures_found = False
        tries = 0
        # NOTE: This can be replaced to use a file watch dog over the file system
        # then use the web socket to notify
        # a watch dog over the files will imply another thread running
        while not pictures_found:
            try:
                save_path = config.raw_folder() + '/'

                left = JPEGImage(save_path + p_left_photo + ".jpg")
                right = JPEGImage(save_path + p_right_photo + ".jpg")

                left.rotate(270).save(save_path + p_left_photo + ".jpg")
                right.rotate(90).save(save_path + p_right_photo + ".jpg")
                pictures_found = True
            except Exception as err:
                logger.error('Pictures not found yet' + str(err))
                sleep(0.5)
                if tries > 20:
                    raise Exception
            tries += 1

    @staticmethod
    # NOTE: There are many of this functions all over the project
    # TODO: extract this to a file service or something similar
    def __file_content():
        pics_file = config.pics_file_path()
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()
        return contents

    @staticmethod
    def append_image_to_yaml(cls, p_project_photo, p_config=None):
        yaml_path = config.pics_yaml_path()

        data_map = dict_from_yaml(yaml_path)

        data_map[p_project_photo.id] = p_project_photo.to_dict()

        if p_config and isinstance(p_config, dict):
            data_map[p_project_photo.id]['config'] = config

        write_dict(yaml_path, data_map)

    @staticmethod
    def mark_image_as_deleted(cls, p_image_id):
        yaml_path = config.pics_yaml_path()
        data_map = dict_from_yaml(yaml_path)
        data_map[p_image_id]['deleted'] = True
        write_dict(yaml_path, data_map)

    @staticmethod
    def delete_photos(cls, p_photo_list):
        pics_file = config.pics_file_path()
        with open(pics_file, "r") as file:
            contents = file.readlines()

        for photo in p_photo_list:
            remove(config.raw_folder() + "/" + photo + ".jpg")
            contents.remove(photo + '\n')

        with open(pics_file, "w") as file:
            file.writelines(contents)

        [cls.mark_image_as_deleted(_id) for _id in p_photo_list]

    @staticmethod
    def update_last_picture_id(cls, p_pic_number):
        config_path = config.project_config_file_path()
        data_map = dict_from_yaml(config_path)

        data_map['camera']['last-pic-number'] = p_pic_number

        write_dict(config_path, data_map)

    @staticmethod
    def insert_pics(cls, p_index, pic_list):
        pics_file = config.pics_file_path()
        with open(pics_file, "r") as file:
            contents = file.readlines()

            if p_index == -1:
                p_index = len(contents)

        for pic in pic_list:
            contents.insert(p_index, pic + '\n')
            p_index += 1

        with open(pics_file, "w") as file:
            file.writelines(contents)

        [cls.append_image_to_yaml(ProjectPhoto(_id, config.project_id)) for _id in pic_list]

    @staticmethod
    def get_last_photos_ids():
        pics_file = config.pics_file_path()
        with open(pics_file, "r") as file:
            contents = file.readlines()

            last_pics = []
            if len(contents) > 1:
                # TODO: take in count project layout(1 or 2 pages)
                last_pics = contents[-2:]
            return last_pics