import uuid
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId
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
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    URL: Optional[str] = None
    GameType: Optional[str] = None
    Location: Optional[str] = None
    Date: Optional[datetime] = None
    Time: Optional[str] = None
    WinningTeam: str
    Quarter: Optional[int] = None
    SecLeft: Optional[int] = None
    AwayTeam: str
    AwayPlay: Optional[str] = None
    AwayScore: Optional[int] = None
    HomeTeam: str
    HomePlay: Optional[str] = None
    HomeScore: Optional[int]
    Shooter: Optional[str] = None
    ShotType: Optional[str] = None
    ShotOutcome: Optional[str] = None
    ShotDist: Optional[int] = None