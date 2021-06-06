from typing import Callable

from fastapi import Response, Request, HTTPException
from fastapi.routing import APIRoute

from exceptions.tenant_exceptions import TenantIDMissingException, InvalidTenantIDException


class GeneralErrorHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except TenantIDMissingException as exc:
                detail = {"errors": [exc.message]}
                raise HTTPException(status_code=403, detail=detail)
            except InvalidTenantIDException as exc:
                detail = {"errors": [exc.message]}
                raise HTTPException(status_code=403, detail=detail)

        return custom_route_handler
