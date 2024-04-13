from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class TerminalEventEnum(Enum):
    ISSUE="ISSUE"
    COMPLETE="COMPLETE"
    REGISTER="REGISTER"

class STerminalEvent(BaseModel):
    address: str
    type: str
    message: str