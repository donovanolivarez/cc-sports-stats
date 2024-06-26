#!/usr/bin/env python3
from typing import List

from bson import ObjectId

from models import NBAData, NBADataUpdate
from fastapi import FastAPI
from pymongo import MongoClient
import certifi

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    CONNECTION_STRING = "mongodb+srv://heyubaidullah:LroLDx3UdCyQO5fA@cc-sports-stat-cluster.ruyzwup.mongodb.net/?retryWrites=true&w=majority&appName=cc-sports-stat-cluster"
    app.mongodb_client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
    app.database = app.mongodb_client['sports-stats']


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
def read_root():
    print(app.database['pbp-nba'])
    return "Welcome to the Sports Statistics app!"

@app.get("/teams", response_description="List all NBA teams", response_model=List[str])
def get_teams():
    teams = list(app.database['pbp-nba'].find().distinct("HomeTeam"))
    return teams

@app.get("/teams/{team_id}", response_description="List all the games of the given team", response_model=List[NBAData], response_model_exclude_none=True)
def get_team_info(team_id: str):
    count = 0
    mycol = app.database['pbp-nba']
    myQuery = {"$or":[{"HomeTeam":team_id},{"AwayTeam":team_id}], "Quarter": 4, "SecLeft": 0, "AwayPlay":"End of Game"}
    results = mycol.find(myQuery)
    print(results)
    nba_data = [NBAData(**doc).model_dump() for doc in results]

    return nba_data


@app.post("/teams/{team_id}/gameInfo", response_description="Create a new entry for game data")
async def create_gameInfo(gameInfo: NBADataUpdate):
    app.database['pbp-nba'].insert_one(gameInfo.model_dump(by_alias=True, exclude=["id"]))
    return gameInfo


@app.delete("/{record_id}", response_description="Remove a given set of game data by ID")
async def remove_gameInfo_byId(record_id: str):
    mongo_id = ObjectId(record_id)
    app.database['pbp-nba'].delete_one({"_id": mongo_id})
    return "Successfully deleted record with ID: " + record_id


@app.delete("/teams/{team_id}", response_description="Remove a given set of game data by Team ID")
async def remove_gameInfo_byId(team_id: str):
    myQuery = {"$or":[{"HomeTeam":team_id},{"AwayTeam":team_id}]}
    app.database['pbp-nba'].delete_many(myQuery)
    return "Successfully deleted all records for team: " + team_id
