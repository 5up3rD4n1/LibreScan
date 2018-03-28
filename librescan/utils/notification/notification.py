from abc import ABCMeta, abstractmethod

IMAGE_PROCESSED_EVENT = 'image_processed'


class Notification(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def notify(p_event, p_data):
        pass

    @staticmethod
    @abstractmethod
    def notify_image_processed(p_data):
        pass
