from os import getenv, path
import yaml

from ..patterns.singleton import Singleton

LS_HOME_DIR = getenv("HOME")
LS_CONFIG_PATH = f'{LS_HOME_DIR}/.librescan'
LS_PROJECTS_FILE = f'{LS_CONFIG_PATH}/projects.yaml'
LS_CONFIG_FILE = f'{LS_CONFIG_PATH}/config.yaml'
LS_PROJECT_CONFIG_FILE = '/.projectConfig.yaml'
LS_DELETE_PICS_FILE = '/.toDelete.ls'
LS_PROCESSED_PATH = '/processed'
LS_PICS_FILE = '/.pics.ls'
LS_PICS_YAML_FILE = '/.pics.yaml'
LS_RAW_PATH = '/raw'
LS_OUTPUT_NAME='out'

LS_SOURCE_PATH = path.dirname(path.dirname(path.realpath(__file__)))

LS_DEV_PICS_PATH = f'{LS_SOURCE_PATH}/resources/devModePics'


class Config(metaclass=Singleton):
    def __init__(self, p_id=None):
        if not hasattr(self, 'project_id'):
            self.project_id = p_id
        self.config_folder = LS_CONFIG_PATH
        self.config_file_path = LS_CONFIG_FILE
        self.projects_path = self.get_projects_path()
        self.project_folder = f'{self.projects_path}/{self.project_id}'
        self.output_name = LS_OUTPUT_NAME

    def change_project(self, p_id):
        self.project_id = p_id
        self.project_folder = f'{self.projects_path}/{p_id}'

    def processed_folder(self):
        return f'{self.project_folder}{LS_PROCESSED_PATH}'

    def raw_folder(self):
        return f'{self.project_folder}{LS_RAW_PATH}'

    def pics_file_path(self):
        return f'{self.project_folder}{LS_PICS_FILE}'

    def pics_yaml_path(self):
        return f'{self.project_folder}{LS_PICS_YAML_FILE}'

    def to_delete_pics_file_path(self):
        return f'{self.project_folder}{LS_DELETE_PICS_FILE}'

    def project_config_file_path(self):
        return f'{self.project_folder}{LS_PROJECT_CONFIG_FILE}'

    def get_config_folder(self):
        return self.config_folder

    @classmethod
    def get_project_path_with_id(cls, p_id):
        return f'{cls.get_projects_path()}/{p_id}'

    @classmethod
    def project_config_file_path_with_id(cls, p_id):
        return f'{cls.get_projects_path()}/{p_id}/{LS_PROJECT_CONFIG_FILE}'

    def pics_yaml_file_with_id(cls, p_id):
        return f'{cls.get_projects_path()}/{p_id}{LS_PICS_YAML_FILE}'

    @staticmethod
    def projects_file_path():
        return LS_PROJECTS_FILE

    @staticmethod
    def get_projects_path():
        f = open(LS_CONFIG_FILE)
        projects_path = yaml.safe_load(f)['project']['path']
        f.close()
        return projects_path.replace("~", LS_HOME_DIR)


config = Config()
