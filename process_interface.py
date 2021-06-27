import abc
import json
import os
import re
import time
from abc import ABC

import boto3


class ProcessInterface(ABC):

    @staticmethod
    def prepare_package(username: str, list_id: str, access_token: str, access_token_secret: str):
        package = {
            'access_token': access_token,
            'access_token_secret': access_token_secret,
            'user_id': username,
            'list_id': list_id
        }
        return package

    @abc.abstractmethod
    def process(self, username: str, list_id: str, access_token: str, access_token_secret: str):
        pass

    @property
    @abc.abstractmethod
    def db(self):
        pass


class AWSProcessInterface(ProcessInterface):
    def __init__(self, db_url, ):
        self.db = db_url

    def process(self, username: str, list_id: str, access_token: str, access_token_secret: str):
        package = self.prepare_package(username, list_id, access_token, access_token_secret)

        sqs_resource = boto3.resource('sqs')
        queue = sqs_resource.get_queue_by_name(QueueName='process')
        response = queue.send_message(MessageBody=json.dumps(package))
        return response

    @property
    def db(self):
        return self.db

    @db.setter
    def db(self, url):
        if re.match(r'aws', url):
            self.db = url
        else:
            raise Exception


class TestProcessAPI(ProcessInterface):
    def __init__(self):
        pass

    def process(self, username: str, list_id: str, access_token: str, access_token_secret: str):
        time.sleep(4)
        return 200

    def db(self):
        return None


class ProcessInterfaceFactory:
    @classmethod
    def create_interface(cls, queue_tool):
        if queue_tool is None:
            return TestProcessAPI()
