from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class STerminalAkk(BaseModel):
    address: str
    proxy: Optional[str]
    is_completed: Optional[bool]
    issued: Optional[datetime]
    winrate: Optional[int]
    points: Optional[int]
    created_at: datetime
    updated_at: datetime