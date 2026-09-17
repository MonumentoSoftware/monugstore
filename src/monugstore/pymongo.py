from pymongo import MongoClient


def get_client(conn_str: str) -> MongoClient:

    try:
        client = MongoClient(conn_str)
        return client
    except Exception as e:
        print(f"Error: {e}")
        return None
