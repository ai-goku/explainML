from events.event import Event
from model.project_model.project_model import Project


class ProjectCreatedEvent(Event):

    def __init__(self, body: Project):
        super().__init__("PROJECT_CREATED", body)
