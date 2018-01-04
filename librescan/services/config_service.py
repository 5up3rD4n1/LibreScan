
from os import getenv
import yaml

from ..patterns.singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self, p_id=None):
        if not hasattr(self, 'project_id'):
            self.project_id = p_id
        self.config_folder = f'{getenv("HOME")}/.librescan'
        self.config_file_path = f'{self.config_folder}/config.yaml'
        self.projects_path = self.get_projects_path(self.config_file_path)
        self.project_folder = f'{self.projects_path}/{self.project_id}'

    def change_project(self, p_id):
        self.project_id = p_id
        self.project_folder = f'{self.projects_path}/{p_id}'

    def processed_folder(self):
        return f'{self.project_folder}/processed'

    def pics_file_path(self):
        return f'{self.project_folder}/.pics.ls'

    def projects_file_path(self):
        return f'{self.config_folder}/projects.yaml'

    @staticmethod
    def get_projects_path(p_path):
        f = open(p_path)
        projects_path = yaml.safe_load(f)['project']['path']
        f.close()
        return projects_path

