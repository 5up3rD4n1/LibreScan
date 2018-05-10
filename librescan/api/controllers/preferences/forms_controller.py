from flask import jsonify, request
from flask_restful import Resource, marshal_with, abort
from librescan.utils import dict_from_yaml
from librescan.config import config


class FormsController(Resource):

    def get(self):
        form_name = request.args.get('form', None)

        data_map = dict_from_yaml(config.get_forms_metadata_path())

        if form_name and form_name not in data_map:
            response = jsonify({'message': f'Form metadata for {form_name} not found'})
            response.status_code = 404
            return response

        data_map = data_map if not form_name else data_map[form_name]

        return jsonify(data_map)
