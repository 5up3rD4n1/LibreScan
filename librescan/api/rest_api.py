from librescan.api.app import api
from librescan.api.controllers import (
    ImagesListController,
    ImagesController,
    ProjectsController,
    ProjectsListController,
    OutputsListController,
    FormsController
)

api.add_resource(ProjectsListController, '/api/projects')
api.add_resource(ProjectsController, '/api/projects/<string:_id>')
api.add_resource(ImagesListController, '/api/projects/<string:_id>/images')
api.add_resource(ImagesController, '/api/projects/<string:_id>/images/<string:image_id>')
api.add_resource(OutputsListController, '/api/projects/<string:_id>/outputs')
api.add_resource(FormsController, '/api/preferences/forms')
