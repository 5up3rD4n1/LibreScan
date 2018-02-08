
# I don't like this but Flask recommend it
# http://flask.pocoo.org/docs/0.12/patterns/packages/

from flask import Flask
from flask_restful import Api
from .controllers import (
    ImagesListController,
    ProjectsController,
    ProjectsListController,
    OutputsListController
)

app = Flask(__name__)
api = Api(app)

# Import individual image and thumbnail route
from .controllers.images import images_controller

api.add_resource(ProjectsListController, '/projects')
api.add_resource(ProjectsController, '/projects/<string:_id>')
api.add_resource(ImagesListController, '/projects/<string:_id>/images')
api.add_resource(OutputsListController, '/projects/<string:_id>/outputs')
