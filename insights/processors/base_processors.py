from abc import ABC, abstractmethod


class BaseProcessor(ABC):
    @abstractmethod
    def process(self, data):
        """
        Process the given data and return the processed result.
        :param data:
        :return:
        """
        pass
