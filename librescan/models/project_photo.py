from flask_restful import fields
from librescan.config import config


class ProjectPhoto:

    def __init__(self, p_id, p_project_id):
        self.id = p_id
        self.project_id = p_project_id
        self.working_dir = config.project_folder

    @staticmethod
    def get_fields():
        return {
            'id': fields.String,
            'project_id': fields.String
        }
