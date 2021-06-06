from pika import PlainCredentials, BlockingConnection, ConnectionParameters, BasicProperties

from events.event import Event


class MessageBroker:

    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str
    ):
        self._credentials = PlainCredentials(user, password)
        self._host = host
        self._port = port

    def publish(self, queue: str, routing_key, event: Event):
        connection = self._get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=event.serialize(),
            properties=BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

    def subscribe(self, queue, callback):
        connection = self._get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        channel.basic_consume(queue=queue,
                              on_message_callback=callback)
        channel.start_consuming()

    def _get_connection(self):
        connection = BlockingConnection(
            ConnectionParameters(
                credentials=self._credentials,
                host=self._host,
                port=self._port
            )
        )
        return connection
