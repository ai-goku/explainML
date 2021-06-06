import logging

from minio import Minio
from minio.notificationconfig import NotificationConfig, QueueConfig, SuffixFilterRule


class MinioClient:

    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self._client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def make_bucket(self, bucket):
        if not self._client.bucket_exists(bucket):
            self._client.make_bucket(bucket)
        else:
            print(f"bucket '{bucket}' exists")

    def delete_bucket(self, bucket):
        if self._client.bucket_exists(bucket):

            for item in self._client.list_objects(bucket):
                self._client.remove_object(bucket, item.object_name)

            self._client.delete_bucket_notification(bucket)
            self._client.remove_bucket(bucket)
        else:
            logging.warning("Bucket Not Found: ", bucket)


    def put_object(self, bucket, file_name, data, content_type="application/octet-stream"):
        self._client.put_object(
            bucket_name=bucket,
            object_name=file_name,
            data=data,
            content_type=content_type,
            length=-1,
            part_size=10 * 1024 * 1024
        )

    def get_object(self, bucket, object_name):
        file = self._client.get_object(
            bucket_name=bucket,
            object_name=object_name
        )
        return file

    def get_presigned_url(self, bucket, object_name):
        return self._client.presigned_get_object(
            bucket_name=bucket,
            object_name=object_name
        )

    def set_bucket_notification(self, bucket):
        config = NotificationConfig(
            queue_config_list=[
                QueueConfig(
                    "arn:minio:sqs:us-east-1:1:amqp",
                    ["s3:ObjectCreated:*"],
                    config_id="1",
                    suffix_filter_rule=SuffixFilterRule(".csv"),
                ),
            ],
        )

        self._client.set_bucket_notification(bucket, config)
