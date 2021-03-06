from dataclasses import dataclass
from typing import Dict, List

from ..patterns import FullQualifiedId
from .event import Event

Information = Dict[FullQualifiedId, List[str]]


@dataclass
class WriteRequestElement:
    """
    Write request element that can be sent to the datastore.
    """

    events: List[Event]
    information: Information
    user_id: int
