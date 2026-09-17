from typing import Any

from pymongo import MongoClient


def get_client(conn_str: str) -> MongoClient[Any] | None:
    try:
        client: MongoClient[Any] = MongoClient(conn_str)
        return client
    except Exception as e:
        print(f"Error: {e}")
        return None
