from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveFloat, PositiveInt


class CityBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=25)
    country: Optional[str] = Field(None, min_length=1, max_length=15)

    class Config:
        extra = Extra.forbid


class ProcessoryCreate(BaseModel):
    name: str = Field(..., max_length=150)
    lineup: Optional[str] = Field(max_length=20)
    socket: str = Field(..., max_length=15)
    tech_process: Optional[str] = Field(max_length=25)
    equipment: Optional[str] = Field(max_length=3)

    clock_frequency: Optional[PositiveFloat] = Field(ge=1, le=10)
    turboboost_frequency: Optional[PositiveFloat] = Field(ge=1, le=10)
    cores_amount: Optional[PositiveInt] = Field(ge=1, le=80)
    productive_cores_amount: Optional[PositiveInt] = Field(ge=1, le=80)
    energy_efficient_cores_amount: Optional[PositiveInt] = Field(ge=1, le=80)
    threads_amount: Optional[PositiveInt] = Field(ge=4, le=160)
    tdp: Optional[PositiveInt] = Field(ge=10, le=500)
    second_level_cache: Optional[str] = Field(max_length=10)
    third_level_cache: Optional[str] = Field(max_length=10)
    free_multiplier: Optional[str] = Field(max_length=3)
    RAM_support: Optional[str] = Field(max_length=4)
    graphics_core: Optional[str] = Field(max_length=4)

    class Config:
        extra = Extra.forbid


class CityUpdate(CityBase):
    pass


class ProcessoryDB(BaseModel):
    id: int
    name: str
    lineup: str
    socket: str
    tech_process: str
    equipment: str

    clock_frequency: float
    turboboost_frequency: float
    cores_amount: int
    productive_cores_amount: int
    energy_efficient_cores_amount: int
    threads_amount: int
    tdp: int
    second_level_cache: str
    third_level_cache: str
    free_multiplier: str
    RAM_support: str
    graphics_core: str

    class Config:
        orm_mode = True
