from datetime import datetime

from fastapi.encoders import jsonable_encoder

from events.project_created_event import ProjectCreatedEvent
from events.project_deleted_event import ProjectDeletedEvent
from exceptions.project_exceptions import ProjectAlreadyExistsException, ProjectNotFoundException
from model.project_model.project_create_model import ProjectCreate
from model.project_model.project_model import Project
from model.project_model.project_status_enum import ProjectStatusEnum
from model.project_model.project_update_model import ProjectUpdate
from utils.message_broker import MessageBroker


async def create_project(project: ProjectCreate, db, message_broker: MessageBroker):
    existing_project = await db['projects'].find_one({
        'name': project.name,
        "user_id": project.user_id
    })

    if existing_project:
        raise ProjectAlreadyExistsException(message="Project already exists")

    new_project = Project(
        name=project.name,
        version=1,
        project_type=project.project_type,
        user_id=project.user_id,
        parent_project=None,
        description=project.description,
        status=ProjectStatusEnum.created,
        created_date=datetime.now()
    )
    new_project = jsonable_encoder(new_project)
    new_project = await db['projects'].insert_one(new_project)
    created_project = await db['projects'].find_one({
        "_id": new_project.inserted_id
    })
    project_created_event = ProjectCreatedEvent(created_project)
    message_broker.publish(
        queue="projects",
        routing_key="project",
        event=project_created_event
    )
    return created_project


async def list_projects(db):
    projects = await db["projects"].find().to_list(1000)
    return projects


async def find_one(db, project_id) -> Project:
    project = await db['projects'].find_one({
        "_id": project_id
    })
    if not project:
        raise ProjectNotFoundException(message="Project not found")
    return Project(**project)


async def update_project(db, project_id, project: ProjectUpdate):
    existing_project = await db['projects'].find_one({
        "_id": project_id
    })
    if not existing_project:
        raise ProjectNotFoundException(message='Project not found')

    project = {k: v for k, v in project.dict().items() if v is not None}

    if len(project) >= 1:
        update_result = await db['projects'].update_one(
            {"_id": project_id},
            {"$set": project}
        )
        if update_result.modified_count == 1:
            if (updated_project := await db['projects'].find_one({"_id": project_id})) is not None:
                return updated_project



async def delete_project(db, message_broker, project_id):
    project = await db["projects"].find_one({"_id": project_id})
    if not project:
        raise ProjectNotFoundException('Project not found')

    delete_result = await db["projects"].delete_one({"_id": project_id})
    project_deleted_event = ProjectDeletedEvent(project)
    message_broker.publish(
        queue="projects",
        routing_key="project",
        event=project_deleted_event
    )
    if delete_result.deleted_count == 1:
        return True