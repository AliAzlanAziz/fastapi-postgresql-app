from typing import Optional
from pydantic import BaseModel, ConfigDict

class EducationCreate(BaseModel):
    degree: str
    field: str
    institute: str

class EducationUpdate(BaseModel):
    degree: Optional[str] = None
    field: Optional[str] = None
    institute: Optional[str] = None

class EducationOut(BaseModel):
    id: int
    degree: str
    field: str
    institute: str
    model_config = ConfigDict(from_attributes=True)
