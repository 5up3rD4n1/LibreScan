from ..patterns import Singleton
from ..utils import TaskManager
from ..models import ProjectPhoto
from queue import Queue
import threading
from librescan.config import config
from librescan.utils import logger


class QueueService(metaclass=Singleton):

    def __init__(self, p_worker_threads=2):
        self.queue = Queue()
        self.worker_threads = p_worker_threads
        self.task_manager = TaskManager()
        self.reset_queue()
        for i in range(self.worker_threads):
            t = threading.Thread(target=self.start)
            t.setDaemon(True)
            t.start()

    def start(self):
        while True:
            photos = [self.queue.get(block=True)]
            logger.info("Processing image: " + photos[0].id)
            self.task_manager.process(photos)
            logger.info("Finished processing image " + photos[0].id)
            self.queue.task_done()

    def push(self, p_image_list):
        if isinstance(p_image_list, list):
            for image in p_image_list:
                self._queue_pic(image)
        else:
            self._queue_pic(p_image_list)

    def is_processing(self):
        return not(self.queue.empty())

    def wait_process(self):
        self.queue.join()

    def clean_queue(self):
        with self.queue.mutex:
            self.queue.queue.clear()
        logger.info("The queue has been cleaned")

    def reset_queue(self):
        self.clean_queue()
        self.wait_process()

    def _queue_pic(self, p_picture):
        photo = ProjectPhoto(p_picture, config.project_id)
        self.queue.put(photo)

    @staticmethod
    def get_active_threads():
        return threading.active_count()


queue_service = QueueService()
