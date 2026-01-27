from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):

    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    role_name: str

class UserRead(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)