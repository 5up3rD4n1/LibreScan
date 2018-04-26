from flask import request
from flask_restful import Resource, marshal_with
from librescan.services import ScannerService, ImageService
from librescan.models import ProjectPhoto
from librescan.config import config


class ImagesListController(Resource):
    def __init__(self):
        self.scanner_service = ScannerService()
        self.image_service = ImageService()

    def put(self, _id):
        config.change_project(_id)
        data = request.get_json()
        picture_ids = self.scanner_service.take_pictures(-1, data['ids'])
        return [ProjectPhoto(picture_id, _id) for picture_id in picture_ids]

    @marshal_with(ProjectPhoto.get_fields())
    def get(self, _id):
        return self.image_service.get_all(_id)

    @marshal_with(ProjectPhoto.get_fields())
    def post(self, _id):
        config.change_project(_id)
        p_index = int(request.args.get('index', -1))
        picture_ids = self.scanner_service.take_pictures(p_index)
        return [self.image_service.get_project_photo(_id, picture_id) for picture_id in picture_ids]
