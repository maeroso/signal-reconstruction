from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from utils.enums.status import Status


class ResultResponse(BaseModel):
    init_datetime: Optional[datetime]
    final_datetime: Optional[datetime]
    interactions: Optional[int]
    status: Optional[Status]

    class Config:
        use_enum_values = True
