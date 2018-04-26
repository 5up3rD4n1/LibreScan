from flask_restful import fields
from librescan.config import config


class ProjectPhoto:
    attributes = ['id', 'project_id', 'working_dir', 'processed', 'deleted']

    def __init__(self, p_id, p_project_id):
        self.id = p_id
        self.project_id = p_project_id
        self.working_dir = config.project_folder
        self.config = {}
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
            'processed': fields.Boolean,
            'deleted': fields.Boolean,
            'config': fields.Nested({
                'color-mode': fields.String,
                'dewarping': fields.String,
                'despeckle': fields.String,
                'dpi-x': fields.Fixed,
                'dpi-y': fields.Float,
                'layout': fields.Float,
                'margins-bottom': fields.Float,
                'margins-left': fields.Float,
                'margins-right': fields.Float,
                'margins-top': fields.Float,
                'threshold': fields.Float,
            })
        }
