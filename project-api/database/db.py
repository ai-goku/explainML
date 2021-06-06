import motor.motor_asyncio
import urllib.parse
import os

from fastapi import Header

from exceptions.tenant_exceptions import TenantIDMissingException, InvalidTenantIDException
from utils.message_broker import MessageBroker


def _get_tenants(tenant_id):
    tenants = dict(
        lumoz={
            "db": "lumoz",
            "username": "lumozuser",
            "password": "lumoz123"
        },
        other={
            "db": "other",
            "username": "otheruser",
            "password": "other123"
        }
    )
    return tenants.get(tenant_id, None)


async def get_tenant_db_client(tenant_id: str = Header(alias="X-TenantID", default="lumoz")):
    if not tenant_id:
        raise TenantIDMissingException("TenantId Not Set")

    tenant_db = _get_tenants(tenant_id)

    if not tenant_db:
        raise InvalidTenantIDException("Invalid TenantId")

    host = os.environ.get('MONGODB', "0.0.0.0:27017")

    username = urllib.parse.quote_plus(tenant_db.get('username'))
    password = urllib.parse.quote_plus(tenant_db.get('password'))
    db = urllib.parse.quote_plus(tenant_db.get('db'))

    mongodb_url = f"mongodb://{username}:{password}@{host}/{db}?retryWrites=true&w=majority"
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
    return client[db]


