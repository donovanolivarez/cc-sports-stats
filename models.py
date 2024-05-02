import uuid
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
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


class NBAData(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    URL: Optional[str]
    GameType: Optional[str]
    Location: Optional[str]
    Date: Optional[datetime]
    Time: Optional[str]
    WinningTeam: str
    Quarter: Optional[int]
    SecLeft: Optional[int]
    AwayTeam: str
    AwayPlay: Optional[str]
    AwayScore: Optional[int]
    HomeTeam: str
    HomePlay: Optional[str]
    HomeScore: Optional[int]
    Shooter: Optional[str]
    ShotType: Optional[str]
    ShotOutcome: Optional[str]
    ShotDist: Optional[int]