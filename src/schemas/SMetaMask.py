from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SMetaMask(BaseModel):
    sid: str
    address: str
    password: Optional[str]
    created_at: datetime
    updated_at: datetime