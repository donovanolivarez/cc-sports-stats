import uuid
from typing import Optional

import pydantic
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """ Custom Type for reading MongoDB IDs """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")
        field_schema.insert(type="string")


class NBAData(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    URL: Optional[str] = Field(default=None)
    GameType: Optional[str] = Field(default=None)
    Location: Optional[str] = Field(default=None)
    Date: Optional[datetime] = Field(default=None)
    Time: Optional[str] = Field(default=None)
    WinningTeam: str = Field(default=None)
    Quarter: Optional[int] = Field(default=None)
    SecLeft: Optional[int] = Field(default=None)
    AwayTeam: Optional[str] = Field(default=None)
    AwayPlay: Optional[str] = Field(default=None)
    AwayScore: Optional[int] = Field(default=None)
    HomeTeam: Optional[str] = Field(default=None)
    HomePlay: Optional[str] = Field(default=None)
    HomeScore: Optional[int] = Field(default=None)
    Shooter: Optional[str] = Field(default=None)
    ShotType: Optional[str] = Field(default=None)
    ShotOutcome: Optional[str] = Field(default=None)
    ShotDist: Optional[int] = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class NBADataUpdate(BaseModel):
    URL: Optional[str] = Field(default=None)
    GameType: Optional[str] = Field(default=None)
    Location: Optional[str] = Field(default=None)
    Date: Optional[datetime] = Field(default=None)
    Time: Optional[str] = Field(default=None)
    WinningTeam: str = Field(default=None)
    Quarter: Optional[int] = Field(default=None)
    SecLeft: Optional[int] = Field(default=None)
    AwayTeam: Optional[str] = Field(default=None)
    AwayPlay: Optional[str] = Field(default=None)
    AwayScore: Optional[int] = Field(default=None)
    HomeTeam: Optional[str] = Field(default=None)
    HomePlay: Optional[str] = Field(default=None)
    HomeScore: Optional[int] = Field(default=None)
    Shooter: Optional[str] = Field(default=None)
    ShotType: Optional[str] = Field(default=None)
    ShotOutcome: Optional[str] = Field(default=None)
    ShotDist: Optional[int] = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
