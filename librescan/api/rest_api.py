from librescan.api.app import api
from librescan.api.controllers import (
    ImagesListController,
    ProjectsController,
    ProjectsListController,
    OutputsListController
)

api.add_resource(ProjectsListController, '/api/projects')
api.add_resource(ProjectsController, '/api/projects/<string:_id>')
api.add_resource(ImagesListController, '/api/projects/<string:_id>/images')
api.add_resource(OutputsListController, '/api/projects/<string:_id>/outputs')
