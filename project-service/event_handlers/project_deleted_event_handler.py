from events.event import Event
from models.project_deleted import ProjectDeleted
from utils.minio_client import MinioClient


def handle_project_deleted_event(
        event: Event,
        minio_client: MinioClient
):
    project = ProjectDeleted(**event.body)

    bucket = project.get_project_bucket()
    minio_client.delete_bucket(bucket)

