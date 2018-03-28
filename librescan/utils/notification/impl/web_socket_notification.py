from ..notification import Notification, IMAGE_PROCESSED_EVENT
from librescan.api.app import socketio
from librescan.utils import logger


class WebSocketNotification(Notification):

    @staticmethod
    def notify(p_event, p_data):
        pass

    # TODO: serialize photo_image
    @staticmethod
    def notify_image_processed(p_data):
        data = {
            'projectId': p_data.project_id,
            'imageId': p_data.id
        }

        logger.info(f'Emitting through socket {IMAGE_PROCESSED_EVENT} {str(data)}')
        socketio.emit(IMAGE_PROCESSED_EVENT, data, json=True)
        # self.__dispatch_thread_notification(IMAGE_PROCESSED_EVENT, data)
