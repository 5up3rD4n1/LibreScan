from flask_restful import fields
from librescan.config import config


class ProjectPhoto:

    attributes = ['id', 'project_id', 'working_dir', 'processed', 'deleted']

    def __init__(self, p_id, p_project_id):
        self.id = p_id
        self.project_id = p_project_id
        self.working_dir = config.project_folder
        self.processed = False
        self.deleted = False

    def to_dict(self):
        data_map = {}
        for attr in self.attributes:
            data_map[attr] = getattr(self, attr)
        return data_map

    @staticmethod
    def get_fields():
        return {
            'id': fields.String,
            'project_id': fields.String,
            'processed': fields.String,
            'deleted': fields.String
        }
