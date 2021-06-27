import abc
import json
import re
import time

import boto3


class BaseInterface:
    def __init__(self, db_url: str):
        self._db = db_url

    @staticmethod
    def prepare_package(
        username: str, list_id: str, access_token: str, access_token_secret: str
    ) -> str:
        package = {
            "access_token": access_token,
            "access_token_secret": access_token_secret,
            "user_id": username,
            "list_id": list_id,
        }
        return json.dumps(package)

    @abc.abstractmethod
    def process(
        self, username: str, list_id: str, access_token: str, access_token_secret: str
    ):
        raise NotImplementedError

    @property
    def db(self):
        return self._db

    @db.setter
    @abc.abstractmethod
    def db(self, new_url: str):
        raise NotImplementedError


class AWSBaseInterface(BaseInterface):
    def __init__(self, db_url):
        super(AWSBaseInterface, self).__init__(db_url)

    def process(
        self, username: str, list_id: str, access_token: str, access_token_secret: str
    ):
        package = self.prepare_package(
            username, list_id, access_token, access_token_secret
        )

        sqs_resource = boto3.resource("sqs")
        queue = sqs_resource.get_queue_by_name(QueueName="process")
        response = queue.send_message(MessageBody=package)
        return response

    @BaseInterface.db.setter
    def db(self, new_url: str):
        if re.match(r"aws", new_url):
            self._db = new_url
        else:
            raise Exception


class TestBaseAPI(BaseInterface):
    def __init__(self, url="test"):
        super(TestBaseAPI, self).__init__(url)

    def process(
        self, username: str, list_id: str, access_token: str, access_token_secret: str
    ):
        time.sleep(4)
        return 200

    @BaseInterface.db.setter
    def db(self, new_url):
        self._db = new_url


class ProcessInterfaceFactory:
    @classmethod
    def create_interface(cls, queue_tool):
        if queue_tool is None:
            return TestBaseAPI()
