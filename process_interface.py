import abc
import json
import time
import hashlib
import boto3
from enum import Enum


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
    ) -> bool:
        raise NotImplementedError


class AWSBaseInterface(BaseInterface):
    def __init__(self, db_url):
        super(AWSBaseInterface, self).__init__(db_url)

    @staticmethod
    def check_hash(hex_digest_to_check: str, original_message: str) -> bool:
        return hex_digest_to_check == hashlib.md5(original_message.encode()).hexdigest()

    def process(
        self, username: str, list_id: str, access_token: str, access_token_secret: str
    ):
        package = self.prepare_package(
            username, list_id, access_token, access_token_secret
        )

        sqs_resource = boto3.resource("sqs")
        queue = sqs_resource.get_queue_by_name(QueueName="process")
        response = queue.send_message(MessageBody=package)
        message_sent = self.check_hash(response["MD5OfMessageBody"], package)
        return message_sent


class TestAWSAPI(BaseInterface):
    def __init__(self, url="test"):
        super(TestAWSAPI, self).__init__(url)

    def process(
        self, username: str, list_id: str, access_token: str, access_token_secret: str
    ):
        time.sleep(4)
        message_as_str = self.prepare_package(
            username, list_id, access_token, access_token_secret
        )
        message_body_hash = hashlib.md5(message_as_str.encode()).hexdigest()
        return {
            "MD5OfMessageBody": message_body_hash,
            "MD5OfMessageAttributes": "string",
            "MD5OfMessageSystemAttributes": "string",
            "MessageId": "string",
            "SequenceNumber": "string",
        }


class Interfaces(Enum):
    AWS = 1
    TEST_AWS = 2


class ProcessInterfaceFactory:
    interfaces = {Interfaces.AWS: AWSBaseInterface, Interfaces.TEST_AWS: TestAWSAPI}

    @classmethod
    def create_interface(cls, queue_tool: Interfaces):
        return ProcessInterfaceFactory.interfaces.get(queue_tool)
