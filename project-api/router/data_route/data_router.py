import datetime
import os
from tempfile import NamedTemporaryFile, TemporaryFile

from fastapi import APIRouter, UploadFile, File, Body, Header, Depends
from fastapi.params import Query
from starlette.background import BackgroundTasks
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from database.db import get_tenant_db_client
from model.data_model.data_model import Data
from model.data_model.presigned_put_url_model import PresignedPutURLResponse
from model.project_model.project_model import Project
from service import project_service, data_service
from utils.airflow_rest_client import AirflowRestClient
from utils.helpers import get_minio_client
from utils.minio_client import MinioClient

router = APIRouter(tags=["data"])


# @router.post(
#     path="/",
#     response_model=Data,
#     status_code=HTTP_201_CREATED
# )
# async def upload_data(
#         background_tasks: BackgroundTasks,
#         project_id: str = Body(...),
#         file: UploadFile = File(...),
#         db=Depends(get_tenant_db_client)
# ):
#     minio_client = MinioClient(
#         endpoint=os.environ.get("MINIO", "localhost:9000"),
#         access_key=os.environ.get("MINIO_ACCESS_KEY", "minio_access_key"),
#         secret_key=os.environ.get("MINIO_SECRET_KEY", "minio_secret_key")
#     )
#
#     airflow_client = AirflowRestClient(
#         base_url=("http://" + os.environ.get("AIRFLOW", "localhost:8080")),
#     )
#
#     data = await data_service.upload_data(
#         db=db,
#         minio_client=minio_client,
#         project_id=project_id,
#         file=file
#     )
#
#     (minio_bucket, minio_object) = tuple(data.url.split("/"))
#
#     params = {
#         'minio_bucket': minio_bucket,
#         'minio_object': minio_object,
#         'minio_endpoint': '0.0.0.0:9000',
#         'minio_secure': False,
#         'minio_secret_key': 'minio_secret_key',
#         'minio_access_key': 'minio_access_key',
#         'project_endpoint': f"http://localhost:3000",
#         'project_update_api': f"/api/v1/projects/{project_id}",
#         'project_update_status': 'profiled'
#     }
#
#     background_tasks.add_task(
#         func=airflow_client.trigger_dag,
#         dag_id='profiler_dag',
#         params=params
#     )
#
#     return data


@router.get(
    path="/",
    response_model=PresignedPutURLResponse
)
async def upload_data(
        project_id: str,
        file: str,
        db=Depends(get_tenant_db_client),
        minio_client=Depends(get_minio_client)
):

    project: Project = await project_service.find_one(
        project_id=project_id,
        db=db
    )
    presigned_put_url = minio_client.get_presigned_put_object(
        bucket=project.get_project_bucket(),
        object_name=file,
    )

    return PresignedPutURLResponse(
        url=presigned_put_url,
        api="/api/v1/data/profile"
    )


@router.get(
    path="/profile",
    response_model=str,
    status_code=HTTP_200_OK
)
async def upload_data(
        project_id: str = Query(...),
        db=Depends(get_tenant_db_client)
):
    minio_client = MinioClient(
        endpoint="localhost:9000",
        access_key="minio_access_key",
        secret_key="minio_secret_key"
    )
    url = await data_service.get_presigned_get_url(
        project_id=project_id,
        minio_client=minio_client,
        db=db
    )
    return url
