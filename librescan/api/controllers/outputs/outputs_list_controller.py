from flask_restful import Resource
from librescan.services import OutputService
from librescan.config import config


class OutputsListController(Resource):

    def __init__(self):
        self.output_service = OutputService()

    def post(self, _id):
        config.change_project(_id)
        self.output_service.generate()
        self.output_service.wait_process()
        return None, 201
