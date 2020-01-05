from typing import Any, Callable, Dict, Text

from mypy_extensions import TypedDict

Environment = TypedDict(
    "Environment",
    {
        "database_url": str,
        "event_store_url": str,
        "auth_url": str,
        "worker_timeout": int,
    },
)

ApplicationConfig = TypedDict("ApplicationConfig", {"environment": Environment})

StartResponse = Callable

WSGIEnvironment = Dict[Text, Any]

Headers = Any  # TODO

KEYSEPARATOR = "/"


class Collection:
    """
    The first part of a full qualified field (also known as "key")
    """

    def __init__(self, collection: str) -> None:
        self.collection = collection

    def __str__(self) -> str:
        return self.collection

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Collection):
            return NotImplemented
        return self.collection == other.collection

    def __hash__(self) -> int:
        return hash(str(self))


class FullQualifiedId:
    """
    Part of a full qualified field (also known as "key"),
    e. g. motions.change_recommendation/42
    """

    def __init__(self, collection: Collection, id: int) -> None:
        self.collection = collection
        self.id = id

    def __str__(self) -> str:
        return KEYSEPARATOR.join((str(self.collection), str(self.id)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FullQualifiedId):
            return NotImplemented
        return self.collection == other.collection and self.id == other.id

    def __hash__(self) -> int:
        return hash(str(self))


class FullQualifiedField:
    """
    The key used in the key-value store i. e. the event store.
    """

    def __init__(self, collection: Collection, id: int, field: str) -> None:
        self.collection = collection
        self.id = id
        self.field = field

    def __str__(self) -> str:
        return KEYSEPARATOR.join((str(self.collection), str(self.id), self.field))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FullQualifiedField):
            return NotImplemented
        print(self.collection, self.field)
        print(self.collection == other.collection)
        return (
            self.collection == other.collection
            and self.id == other.id
            and self.field == other.field
        )

    def __hash__(self) -> int:
        return hash(str(self))


class Event(TypedDict):
    """
    Event that can be sent to the event store.
    """

    type: str
    position: int
    information: Dict[str, Any]
    fields: Dict[FullQualifiedField, Any]
