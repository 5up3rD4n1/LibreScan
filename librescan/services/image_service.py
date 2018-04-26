from jpegtran import JPEGImage
import os
from os import remove
from time import sleep

from PIL import Image

from librescan.config import config
from librescan.models import ProjectPhoto
from librescan.utils import (
    file_lines,
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

    @classmethod
    def get_all(cls, p_project_id):
        config.change_project(p_project_id)
        pics_file_path = config.pics_file_path()
        contents = file_lines(pics_file_path)
        return [cls.get_project_photo(p_project_id, image_id.rstrip()) for image_id in contents]

    @staticmethod
    def get_project_photo(p_project_id, p_image_id):
        images_yaml = config.pics_yaml_file_with_id(p_project_id)
        project_config_path = config.project_config_file_path_with_id(p_project_id)
        project_data = dict_from_yaml(project_config_path)
        images_data = dict_from_yaml(images_yaml)

        images_data = images_data if images_data else dict()

        image_data = images_data.get(p_image_id, dict())

        image_default_config = project_data.get('scantailor', dict())

        if project_data.get('scantailor', None):
            if 'config' not in image_data or not image_data.get('config'):
                image_data['config'] = dict()

            # NOTE: Assuming attributes not deeper than one level
            for k, v in image_default_config.items():
                if k not in image_data['config']:
                    image_data['config'][k] = v

        return ProjectPhoto(p_image_id, p_project_id, image_data)
    
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

    @classmethod
    def append_image_to_yaml(cls, p_project_photo, p_config=None):
        yaml_path = config.pics_yaml_path()

        photos_data = dict_from_yaml(yaml_path)

        photos_data = photos_data if photos_data else dict()

        photo_file_data = photos_data.get(p_project_photo.id, dict())

        photo_data = p_project_photo.to_dict()

        print("----------------------------")
        print(photo_data)
        print()

        # Merge memory object with (file object or new dic)
        photo_data = cls.__merge_dic(photo_data, photo_file_data)

        print(photo_data)
        print()

        if p_config and isinstance(p_config, dict):
            photo_data = cls.__merge_dic(photo_data, p_config)
            print(photo_data)
            print()

        photos_data[p_project_photo.id] = photo_data
        write_dict(yaml_path, photos_data)

        return cls.get_project_photo(p_project_photo.project_id, p_project_photo.id)

    @staticmethod
    def mark_image_as_deleted(p_image_id):
        yaml_path = config.pics_yaml_path()
        data_map = dict_from_yaml(yaml_path)
        data_map[p_image_id]['deleted'] = True
        write_dict(yaml_path, data_map)

    @classmethod
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

    @classmethod
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
                # TODO: take in count project layout (1 or 2 pages)
                last_pics = contents[-2:]
            return last_pics

    @classmethod
    def __merge_dic(cls, original, update):
        """
        Recursively update a dict.
        Subdict's won't be overwritten but also updated.
        """
        for key, value in original.items():
            if not update:
                return dict()
            if key not in update:
                update[key] = value
            elif isinstance(value, dict):
                cls.__merge_dic(value, update[key])
        return update
