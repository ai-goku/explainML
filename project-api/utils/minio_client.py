import os.path
from datetime import timedelta

from minio import Minio


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

    def get_presigned_put_object(self, bucket, object_name, expires=timedelta(hours=1)):
        return self._client.presigned_put_object(
            bucket_name=bucket,
            object_name=object_name,
            expires=expires
        )
