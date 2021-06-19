import abc
from abc import ABC


class ProcessInterface(ABC):

    @abc.abstractmethod
    def process(self, username: str, list_id: str):
        pass

    @property
    @abc.abstractmethod
    def _db(self):
        pass


class AWSProcessInterface(ProcessInterface):
    def __init__(self, db_url, ):
        pass