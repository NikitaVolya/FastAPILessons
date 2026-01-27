from pydantic import BaseModel, Field, ConfigDict



class RoleCreate(BaseModel):
    name: str = Field(min_length=3)

class RoleRead(RoleCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)