from datetime import datetime
from pydantic import BaseModel


class JobItem(BaseModel):
    id: str
    title: str
    subtitle: str
    description: str
    location: str
    posted: datetime
