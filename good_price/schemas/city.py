from typing import Optional

from pydantic import BaseModel, Extra, Field


class CityBase(BaseModel):
    name: Optional[str] = Field(None, max_length=25)
    country: Optional[str] = Field(None, max_length=15)

    class Config:
        extra = Extra.forbid


class CityCreate(BaseModel):
    name: str = Field(..., max_length=25)
    country: str = Field(..., max_length=15)

    class Config:
        extra = Extra.forbid


class CityUpdate(CityBase):
    pass


class CityDB(BaseModel):
    id: int
    name: str
    country: str

    class Config:
        orm_mode = True
