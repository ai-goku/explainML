from datetime import datetime
from tempfile import TemporaryFile

from model.data_model.data_model import Data
from model.project_model.project_model import Project
from model.project_model.project_status_enum import ProjectStatusEnum
from model.project_model.project_update_model import ProjectUpdate
from service import project_service
from utils.minio_client import MinioClient
import os


async def upload_data(project_id, file, minio_client, db):
    project: Project = await project_service.find_one(db, project_id)


    bucket = f"user-{project.user_id}-{project.name}-v{project.version}-data".lower().strip().replace("_", "-")
    minio_client.make_bucket(bucket)
    d = await file.read()

    with TemporaryFile() as tmp:
        tmp.write(d)
        tmp.seek(0)
        minio_client.put_object(
            bucket=bucket,
            file_name=file.filename,
            data=tmp
        )
    data = Data(
        file_name=file.filename,
        content_type=file.content_type,
        project_id=project_id,
        version=1,
        created_at=datetime.now(),
        url=f"{bucket}/{file.filename}"
    )

    project_update = ProjectUpdate(status=ProjectStatusEnum.uploaded)
    project = await project_service.update_project(db, project_id, project_update)
    return data


async def get_presigned_get_url(project_id, minio_client: MinioClient, db):
    project: Project = await project_service.find_one(db=db, project_id=project_id)
    object_name = 'profile.html'
    bucket = f"user-{project.user_id}-{project.name}-v{project.version}-data".lower().strip().replace("_", "-")
    return minio_client.get_presigned_url(bucket, object_name)