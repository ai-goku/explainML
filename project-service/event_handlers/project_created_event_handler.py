
from events.event import Event
from models.project import Project
from utils.minio_client import MinioClient


def handle_project_created_event(
        event: Event,
        minio_client: MinioClient
):
    project = Project(**event.body)
    bucket_name = project.get_project_bucket()
    minio_client.make_bucket(bucket_name)
    minio_client.set_bucket_notification(bucket_name)

