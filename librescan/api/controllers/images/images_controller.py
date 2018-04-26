from flask import abort, request, send_file, Response
from flask_restful import Resource
from librescan.api.app import app
from librescan.services import ImageService, ScannerService
from librescan.utils import logger


class ImagesController(Resource):
    def __init__(self):
        self.scanner_service = ScannerService()

    def put(self, _id, image_id):
        request_type = request.args.get('type', None)

        if request_type == 'attributes':
            logger.info(request.get_json())


@app.route('/api/projects/<p_project_id>/images/<p_image_id>')
def get_image(p_project_id, p_image_id):
    try:
        return send_file(
            ImageService.image_path(p_project_id, p_image_id),
            mimetype='image/jpeg'
        )
    except FileNotFoundError as err:
        abort(404, f'File Not Found: {str(err)}')
    except (TypeError, ValueError) as err:
        abort(400, str(err))


@app.route('/api/projects/<p_project_id>/thumbnails/<p_image_id>')
def get_thumbnail(p_project_id, p_image_id):
    try:
        height = int(request.args.get('height', 250))
        width = int(request.args.get('width', 175))
        image = ImageService.thumbnail(p_project_id, p_image_id, height, width)
        return Response(image, mimetype='image/jpeg')
    except FileNotFoundError as err:
        abort(404, f'File Not Found: {str(err)}')
    except (TypeError, ValueError) as err:
        abort(400, f'Error: height and width parameter must be integers; {str(err)}')


@app.route('/api/projects/<p_project_id>/tifs/<p_image_id>')
def get_tif(p_project_id, p_image_id):
    try:
        height = int(request.args.get('height', 250))
        width = int(request.args.get('width', 175))
        image = ImageService.tif(p_project_id, p_image_id, height, width)
        return Response(image, mimetype='image/jpeg')
    except FileNotFoundError as err:
        abort(404, f'File Not Found: {str(err)}')
    except (TypeError, ValueError) as err:
        abort(400, f'Error: height and width parameter must be integers; {str(err)}')
