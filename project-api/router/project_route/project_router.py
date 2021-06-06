from typing import List

from fastapi import APIRouter, Body, Path
from fastapi.params import Header, Depends
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from database.db import get_tenant_db_client
from model.project_model.project_create_model import ProjectCreate
from model.project_model.project_model import Project
from model.project_model.project_update_model import ProjectUpdate
from router.project_route.project_router_exception_handler import ProjectErrorHandler
from service import project_service

# Exception Handlers
from utils.helpers import get_message_broker

router = APIRouter(tags=["projects"], route_class=ProjectErrorHandler)


@router.post(
    path="/",
    response_description="Create a project",
    response_model=Project,
    status_code=HTTP_201_CREATED
)
async def create_project(
        project: ProjectCreate = Body(...),
        # tenant_id: str = Header(alias="X-TenantID", default=None)
        db=Depends(get_tenant_db_client),
        message_broker=Depends(get_message_broker)
):
    created_project = await project_service.create_project(project, db, message_broker)
    return JSONResponse(status_code=HTTP_201_CREATED, content=created_project)


@router.get(
    path="/",
    response_description="List all projects",
    response_model=List[Project]
)
async def list_projects(
        db=Depends(get_tenant_db_client)

):
    projects = await project_service.list_projects(db)
    return projects


@router.get(
    path="/{project_id}",
    response_description="List a project",
    response_model=Project
)
async def find_one(
        project_id: str,
        db=Depends(get_tenant_db_client)
):
    project = await project_service.find_one(db, project_id)
    return project


@router.put(
    path="/{project_id}",
    response_description="Update a project_model",
    response_model=Project
)
async def update_project(
        project_id: str,
        project_update: ProjectUpdate = Body(...),
        db=Depends(get_tenant_db_client)
):
    project = await project_service.update_project(db, project_id, project_update)
    if project:
        return project
    else:
        raise Exception("Something bad happened")


@router.delete(
    path="/{project_id}",
    response_description="Delete a project_model",
    response_model=None,
    status_code=HTTP_204_NO_CONTENT
)
async def delete_one(
        project_id: str,
        db=Depends(get_tenant_db_client),
        message_broker=Depends(get_message_broker)
):
    result = await project_service.delete_project(db, message_broker, project_id)
    if result:
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        raise Exception("Something bad happened")
