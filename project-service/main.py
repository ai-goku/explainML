import os
from event_handlers.project_created_event_handler import handle_project_created_event
from event_handlers.project_deleted_event_handler import handle_project_deleted_event
from events.event import Event
from utils.helpers import get_message_broker
from utils.message_broker import MessageBroker
import json

from utils.minio_client import MinioClient
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        event = Event(**data)
        logger.info(f'Received: {event}')

        if event.name == "PROJECT_CREATED":
            minio_client = MinioClient(
                endpoint=os.environ.get("MINIO", "localhost:9000"),
                access_key=os.environ.get("MINIO_ACCESS_KEY", "minio"),
                secret_key=os.environ.get("MINIO_SECRET_KEY", "minio123")
            )
            handle_project_created_event(event, minio_client)
        elif event.name == "PROJECT_DELETED":
            minio_client = MinioClient(
                endpoint=os.environ.get("MINIO", "localhost:9000"),
                access_key=os.environ.get("MINIO_ACCESS_KEY", "minio"),
                secret_key=os.environ.get("MINIO_SECRET_KEY", "minio123")
            )
            handle_project_deleted_event(event, minio_client)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"Completed: {event}")
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    message_broker: MessageBroker = get_message_broker()
    message_broker.subscribe(queue="project", callback=callback)
