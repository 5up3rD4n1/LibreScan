from . import Scantailor
from . import Tesseract
from yaml import safe_load
from librescan.config import config, LS_PROJECT_CONFIG_FILE
from librescan.utils import task
from librescan.utils.log import get_logger


class TaskManager:

    def __init__(self):
        self.logger = get_logger()

    def process(self, p_photos):
        for photo in p_photos:
            tasks = self.__get_tasks(photo.project_id)
            params = {'input_dir': photo.working_dir, 'photo': photo.id}
            for task_instance in tasks:
                task_instance.exec(params)
                self.logger.debug("Executing task: " + str(task_instance.__class__.__name__) + " for image " + photo.id)

    @classmethod
    def __get_tasks(cls, p_project_id):
        project_path = config.get_project_path_with_id(p_project_id)
        configuration = cls.__get_configuration(project_path)
        tasks = []
        for task_name in configuration['general-info'].get('tasks', []):
            class_ = getattr(task, to_capitalize(task_name))
            tasks.append(class_(configuration.get(task_name, dict())))

        return tasks

    # Loads tools configuration from the project configuration.
    @staticmethod
    def __get_configuration(p_project_path):
        config_path = p_project_path + LS_PROJECT_CONFIG_FILE
        f = open(config_path)
        data_map = safe_load(f)
        f.close()
        return data_map


# TODO: move this to a tools module
def to_capitalize(snake_str):
    components = snake_str.split('_')
    return "".join(x.title() for x in components)
