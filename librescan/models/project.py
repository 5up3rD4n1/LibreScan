from flask_restful import fields


class Project(object):

    def __init__(self, p_id, p_name, p_description, p_lang, p_cam_config,
                 p_output_formats, p_path=None, p_creation_date=None):
        self.id = p_id
        self.name = p_name
        self.description = p_description
        self.lang = p_lang
        self.cam_config = p_cam_config
        self.output_formats = p_output_formats
        self.path = p_path
        self.creation_date = p_creation_date

    @staticmethod
    def parse(p_id, p_data):
        return Project(
            p_id,
            p_data.get('name', None),
            p_data.get('description', None),
            None,
            None,
            None,
            p_data.get('path', None),
            p_data.get('creation_date', None)
        )

    @staticmethod
    def get_fields():
        return {
            'id': fields.String,
            'name': fields.String,
            'path': fields.String,
            'description': fields.String,
            'creation_date': fields.String
        }
