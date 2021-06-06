import os

from utils.message_broker import MessageBroker
from utils.minio_client import MinioClient


async def get_message_broker():
    host = os.environ.get("MESSAGE_BROKER_HOST", "localhost")
    port = os.environ.get("MESSAGE_BROKER_PORT", 5672)
    user = os.environ.get("MESSAGE_BROKER_USER", "user")
    password = os.environ.get("MESSAGE_BROKER_PASSWORD", "password")

    return MessageBroker(
        host=host,
        port=port,
        user=user,
        password=password
    )

async def get_minio_client():
    minio_client = MinioClient(
        endpoint=os.environ.get("MINIO", "localhost:9000"),
        access_key=os.environ.get("MINIO_ACCESS_KEY", "minio"),
        secret_key=os.environ.get("MINIO_SECRET_KEY", "minio123")
    )
    return minio_client