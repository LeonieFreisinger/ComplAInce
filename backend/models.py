
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, List

class Message(BaseModel):
    body: Any
    author: str
    timestamp: datetime

class Query(BaseModel):
    chatContent: List[Message]