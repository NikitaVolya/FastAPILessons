from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class DepartamentCreate(BaseModel):
    name: str
    description: Optional[str] = Field(default="", max_length=500)

class DepartamentRead(DepartamentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)