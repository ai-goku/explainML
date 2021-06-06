from typing import Callable

from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from fastapi import Request, Response, HTTPException

import json

from exceptions.project_exceptions import ProjectAlreadyExistsException, ProjectNotFoundException
from exceptions.tenant_exceptions import TenantIDMissingException, InvalidTenantIDException


class ProjectErrorHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=400, detail=detail)
            except ProjectAlreadyExistsException as exc:
                body = await request.body()
                detail = {"errors": [exc.message], "body": json.loads(body.decode())}
                raise HTTPException(status_code=409, detail=detail)
            except ProjectNotFoundException as exc:
                path_params = request.path_params
                detail = {"errors": [exc.message], "path": path_params}
                raise HTTPException(status_code=404, detail=detail)
            except TenantIDMissingException as exc:
                detail = {"errors": [exc.message]}
                raise HTTPException(status_code=403, detail=detail)
            except InvalidTenantIDException as exc:
                detail = {"errors": [exc.message]}
                raise HTTPException(status_code=403, detail=detail)

        return custom_route_handler
