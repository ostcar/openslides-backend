from typing import Any, Dict, List, Tuple

import requests
import simplejson as json
from mypy_extensions import TypedDict

from ..shared.exceptions import DatabaseException
from ..shared.interfaces import Filter, LoggingModule
from ..shared.patterns import Collection, FullQualifiedId

PartialModel = Dict[str, Any]
Found = TypedDict("Found", {"exists": bool, "position": int})
Count = TypedDict("Count", {"count": int, "position": int})
Aggregate = TypedDict("Aggregate", {"value": object, "position": int})


class DatabaseHTTPAdapter:
    """
    Adapter to connect to (read-only) database.
    """

    def __init__(self, database_url: str, logging: LoggingModule) -> None:
        self.url = database_url
        self.logger = logging.getLogger(__name__)
        self.headers = {"Content-Type": "application/json"}

    def getIds(self, collection: Collection, range: int) -> Tuple[int]:
        raise

    def get(
        self, fqid: FullQualifiedId, mapped_fields: List[str] = None
    ) -> Tuple[PartialModel, int]:
        data = {
            "command": "get",
            "parameters": {"fqid": str(fqid), "mapped_fields": mapped_fields},
        }
        self.logger.debug(f"Start request to database with the following data: {data}")
        response = requests.get(self.url, data=json.dumps(data), headers=self.headers)
        if not response.ok:
            if response.status_code >= 500:
                raise DatabaseException("Connection to database failed.")
            if response.json().get("error") == "ModelDoesNotExist":
                pass
            else:
                pass
            # TODO: Check codes and raise error (ModelDoesNotExist, ModelLocked, ModelDoesExist, InvalidFormat, ModelNotDeleted, MeetingIdMissing)
        else:
            pass
            # Get data and position from db
        return ({"foo": "bar"}, 0)

    def getMany(
        self, collection: Collection, ids: List[int], mapped_fields: List[str] = None
    ) -> Tuple[Dict[int, PartialModel], int]:
        data = {
            "command": "getMany",
            "parameters": {
                "collection": str(collection),
                "ids": ids,
                "mapped_fields": mapped_fields,
            },
        }
        self.logger.debug(f"Start request to database with the following data: {data}")
        response = requests.get(self.url, data=json.dumps(data), headers=self.headers)
        print(response)  # TODO: Use response
        return ({42: {"foo": "bar"}}, 0)

    def getAll(
        self, collection: Collection, mapped_fields: List[str] = None
    ) -> Tuple[object]:
        raise

    def filter(
        self,
        collection: Collection,
        filter: Filter,
        meeting_id: int = None,
        mapped_fields: List[str] = None,
    ) -> Tuple[Dict[int, PartialModel], int]:
        raise

    def exists(self, collection: Collection, filter: Filter) -> Found:
        raise

    def count(self, collection: Collection, filter: Filter) -> Count:
        raise

    def min(self, collection: Collection, filter: Filter, type: str) -> Aggregate:
        raise

    def max(self, collection: Collection, filter: Filter, type: str) -> Aggregate:
        raise

    def getId(self, collection: Collection) -> Tuple[int, int]:
        data = {"command": "getId", "parameters": {"collection": str(collection)}}
        self.logger.debug(f"Start request to database with the following data: {data}")
        response = requests.get(self.url, data=json.dumps(data), headers=self.headers)
        print(response)  # TODO: Use response
        return (0, 0)
