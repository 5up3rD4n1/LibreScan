from os import getenv
from os import mkdir
from os import system
from os.path import exists as f_checker
import subprocess
import time
import yaml

from .queue_service import QueueService
from librescan.models import Project
from librescan.config import config
from librescan.utils import logger


class ProjectService:
    def create(self, p_project):
        config_folder = config.config_folder
        config_file_path = config.config_file_path
        project_id = self.get_folder_name(config_file_path)
        config.change_project(project_id)

        mkdir(config.project_folder)
        mkdir(config.raw_folder())
        mkdir(config.processed_folder())

        # Creates the project config template with default values.
        src = config_folder + "/defaultProjectConfig.yaml"
        destiny = config.project_config_file_path()

        system("cp " + src + " " + destiny)
        system("touch " + config.pics_file_path())
        system("touch " + config.to_delete_pics_file_path())

        # Update project configuration
        self.change_config(p_project, destiny)

        # Append new project to projects file.
        p_project.id = project_id
        p_project.path = config.project_folder
        p_project.creation_date = time.strftime("%x %X")

        self.append_project(config.projects_file_path(), p_project)
        return p_project

    def remove(self, p_id):
        config.change_project(p_id)
        config_path = config.projects_file_path()
        data_map = self.get_projects_data(config_path)
        if data_map.get(p_id, False):
            project = Project.parse(p_id, data_map[p_id])
            data_map.pop(p_id)
            project_path = config.project_folder
            system("rm -rf " + project_path)

            f = open(config_path, 'w')
            if data_map:
                f.write(yaml.dump(data_map, default_flow_style=False, allow_unicode=True))
            else:
                f.seek(0)
                f.truncate()
            f.close()
            return project

    def load(self, p_id):
        config.change_project(p_id)
        config_path = config.projects_file_path()
        data_map = self.get_projects_data(config_path)

        if data_map and data_map.get(p_id, False):
            queue_service = QueueService()

            index = 1
            processed_path = config.processed_folder()
            contents = self.get_file_contents(config.pics_file_path())
            for c in contents:
                pic_path = processed_path + c[:-1]
                if (not f_checker(pic_path + ".tif") or
                        not f_checker(pic_path + ".hocr")):
                    if (not f_checker(processed_path + "rlsp" + str(index).zfill(5) + ".tif") or
                            not f_checker(processed_path + "rlsp" + str(index).zfill(5) + ".hocr")):
                        queue_service.push([c[:-1]])
                        logger.info("Pushing " + c[:-1])
                index += 1

            return Project.parse(p_id, data_map[p_id])

    def get_all(self):
        config_path = config.projects_file_path()
        f = open(config_path)
        data_map = yaml.safe_load(f)
        f.close()
        return [Project.parse(_id, data_map[_id]) for _id in data_map or []]

    @staticmethod
    def get_config(p_id):
        return 1

    @staticmethod
    def change_config(p_project, p_config_path):
        f = open(p_config_path)
        data_map = yaml.safe_load(f)
        f.close()
        if p_project.cam_config is not None:
            data_map['camera']['zoom'] = p_project.cam_config.zoom
            data_map['camera']['iso'] = p_project.cam_config.iso

        data_map['general-info']['name'] = p_project.name
        data_map['general-info']['description'] = p_project.description
        data_map['general-info']['output-formats'] = p_project.output_formats
        data_map['tesseract']['lang'] = p_project.lang

        f = open(p_config_path, 'w')
        f.write(yaml.dump(data_map, default_flow_style=False, allow_unicode=True))
        f.close()

    @staticmethod
    def get_folder_name(p_path):
        f = open(p_path)
        data_map = yaml.safe_load(f)
        f.close()
        project_id = data_map['project']['last-id'] + 1
        data_map['project']['last-id'] = project_id
        folder_name = "L" + str(project_id)
        f = open(p_path, 'w')
        f.write(yaml.dump(data_map, default_flow_style=False, allow_unicode=True))
        f.close()
        return folder_name

    @staticmethod
    def append_project(p_projects_path, p_project):
        project = {
            str(p_project.id): {
                'name': p_project.name,
                'path': p_project.path,
                'description': p_project.description,
                'creation_date': p_project.creation_date
            }
        }

        f = open(p_projects_path, "a")
        f.write(yaml.dump(project, default_flow_style=False, allow_unicode=True))
        f.close()

    @staticmethod
    def get_available_languages():
        available_langs = (subprocess.Popen(['tesseract', "--list-langs"],
                                            stderr=subprocess.STDOUT,
                                            stdout=subprocess.PIPE)
                           .communicate()[0].decode('utf-8')
                           .split("\n")[1:-1])
        return available_langs

    @staticmethod
    def get_project_last_pic(p_id):
        config_path = getenv("HOME") + '/LibreScanProjects/' + p_id + '/.projectConfig.yaml'
        f = open(config_path)
        last_pic_number = yaml.safe_load(f)['camera']['last-pic-number']
        f.close()
        return last_pic_number

    def remove_file_pics(self, p_index=-1):
        pics_file = self.working_dir + '/.pics.ls'
        f = open(pics_file, "r")
        contents = f.readlines()
        f.close()

        if p_index == -1:
            p_index = len(contents) - 2

        contents.pop(p_index)
        contents.pop(p_index+1)

        f = open(pics_file, "w")
        f.writelines(contents)
        f.close()

    @staticmethod
    def get_file_contents(p_path):
        f = open(p_path, "r")
        contents = f.readlines()
        f.close()
        return contents

    @staticmethod
    def get_projects_data(p_path):
        f = open(p_path)
        data_map = yaml.safe_load(f)
        f.close()
        return data_map
