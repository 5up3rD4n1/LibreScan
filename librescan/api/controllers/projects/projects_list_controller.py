from flask import request
from flask_restful import Resource, marshal_with
from librescan.services import ProjectService
from librescan.models import CameraConfig, Project


class ProjectsListController(Resource):

    def __init__(self):
        self.project_service = ProjectService()

    @marshal_with(Project.get_fields())
    def get(self):
        return self.project_service.get_all() or []

    @marshal_with(Project.get_fields())
    def post(self):
        params = request.get_json()
        name = params['name']
        description = params['description']
        language = params['config']['language']
        zoom = int(params['config']['zoom'])
        camera_config = CameraConfig(zoom, 0)
        project = Project(None, name, description, language, camera_config,
                          ['pdfbeads'])
        return self.project_service.create(project)
