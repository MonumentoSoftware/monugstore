from typing import Any

try:
    from pymongo import MongoClient
except ImportError as exc:
    raise ImportError(
        "Mongo helpers require the optional extra 'mongo'. Install with: pip install 'monugstore[mongo]'"
    ) from exc


def get_client(conn_str: str) -> MongoClient[Any] | None:
    try:
        client: MongoClient[Any] = MongoClient(conn_str)
        return client
    except Exception as e:
        print(f"Error: {e}")
        return None
