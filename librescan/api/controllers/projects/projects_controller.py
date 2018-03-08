from flask import abort
from flask_restful import Resource, marshal_with
from librescan.services import ProjectService
from librescan.models import Project
from librescan.utils import Log


class ProjectsController(Resource):
    def __init__(self):
        self.project_service = ProjectService()

    @marshal_with(Project.get_fields())
    def get(self, _id):
        Log().debug("this is the id")
        Log().debug(_id)
        project = self.project_service.load(_id)
        if not project:
            abort(404, 'Project not found')
        return project
