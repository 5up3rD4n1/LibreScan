from flask_restful import fields
from librescan.config import config
from copy import deepcopy


class ProjectPhoto:
    attributes = ['id', 'project_id', 'working_dir', 'processed', 'deleted', 'config']

    def __init__(self, p_id, p_project_id, p_config=None):
        self.id = p_id
        self.project_id = p_project_id
        self.working_dir = config.project_folder
        self.processed = False
        self.deleted = False

        if p_config and isinstance(p_config, dict):

            if 'config' in p_config and isinstance(p_config, dict):
                for k, v in p_config['config'].items():
                    p_config[k] = v

            config_copy = deepcopy(p_config)
            for k, v in config_copy.items():
                if k in dir(self):
                    setattr(self, k, v)
                    del p_config[k]

        self.config = p_config

    def to_dict(self):
        data_map = dict()
        for attr in self.attributes:
            data_map[attr] = getattr(self, attr)

        print(data_map)
        return data_map

    @staticmethod
    def get_fields():
        return {
            'id': fields.String,
            'project_id': fields.String,
            'processed': fields.Boolean,
            'deleted': fields.Boolean,
            'working_dir': fields.String,
            'config': fields.Nested({
                'color-mode': fields.String,
                'dewarping': fields.String,
                'despeckle': fields.String,
                'dpi-x': fields.Float,
                'dpi-y': fields.Float,
                'layout': fields.Float,
                'margins-bottom': fields.Float,
                'margins-left': fields.Float,
                'margins-right': fields.Float,
                'margins-top': fields.Float,
                'threshold': fields.Float,
            })
        }
