from flask import abort, jsonify
from flask_restful import Resource, marshal_with
from librescan.utils import dict_from_yaml
from librescan.config import config


class FormsController(Resource):

    def get(self):
        form_name = request.args.get('form', None)




        if form_name and form_name not in data_map:
            abort(404, jsonify(dict(message='Form metadata not found')))

        data_map = data_map if not form_name else data_map[form_name]

        return jsonify(data_map)
