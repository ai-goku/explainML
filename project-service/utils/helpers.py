import os

from utils.message_broker import MessageBroker


def get_message_broker():
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
