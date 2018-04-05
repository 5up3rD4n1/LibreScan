from abc import ABCMeta, abstractmethod


class OutputMaker(metaclass=ABCMeta):

    @abstractmethod
    def make(self, path, filename):
        pass

    @staticmethod
    @abstractmethod
    def get():
        pass
