from flask_restful import Resource, marshal_with
from librescan.services import ScannerService
from librescan.models import ProjectPhoto
from librescan.config import config


class ImagesListController(Resource):
    def __init__(self):
        self.scanner_service = ScannerService()

    @marshal_with(ProjectPhoto.get_fields())
    def post(self, _id):
        config.change_project(_id)
        picture_ids = self.scanner_service.take_pictures()
        return [ProjectPhoto(picture_id, _id) for picture_id in picture_ids]
