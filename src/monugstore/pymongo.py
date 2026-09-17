import logging
from typing import Any

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
except ImportError as exc:
    raise ImportError(
        "Mongo helpers require the optional extra 'mongo'. Install with: pip install 'monugstore[mongo]'"
    ) from exc

logger = logging.getLogger(__name__)


def get_client(conn_str: str) -> MongoClient[Any] | None:
    try:
        client: MongoClient[Any] = MongoClient(conn_str)
        return client
    except PyMongoError:
        logger.exception("mongo_client_failed")
        return None
