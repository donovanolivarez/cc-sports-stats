#!/usr/bin/env python3
from datetime import datetime
from typing import List

from models import NBAData
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import MongoClient

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    CONNECTION_STRING = "mongodb+srv://heyubaidullah:LroLDx3UdCyQO5fA@cc-sports-stat-cluster.ruyzwup.mongodb.net/?retryWrites=true&w=majority&appName=cc-sports-stat-cluster"
    app.mongodb_client = MongoClient(CONNECTION_STRING)
    app.database = app.mongodb_client['sports-stats']
    app.database['pbp-nba']


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

@app.get("/teams/{team_id}", response_description="List all the games of the given team", response_model=str)
def get_team_info(team_id: str):
    count = 0
    mycol = app.database['pbp-nba']
    myQuery = {"WinningTeam": team_id, "Quarter": 4, "SecLeft": 0, "AwayPlay":"End of Game"}
    results = mycol.find(myQuery)
    for doc1 in results:
        count = count + 1
        print(doc1)

    myString = "The total number of games won by " + team_id + " was " + str(count)
    return myString


# @app.post("/teams/{team_id}/gameInfo", response_description="Create a new entry for game data")
# async def create_gameInfo(post: postingModel.Posting = Body(...)):
#     post = jsonable_encoder(post)
#     app.database['pbp-nba'].insert_one(nbadata_helper(post))
#     return "Game info for " + post.WinningTeam + " was inserted."

@app.post("/teams/{team_id}/gameInfo", response_description="Create a new entry for game data")
async def create_gameInfo(gameInfo: NBAData):
    print(gameInfo)
    json_compatible_item_data = jsonable_encoder(NBAData)
    app.database['pbp-nba'].insert_one(gameInfo.model_dump())
    return "Game info for " + gameInfo.WinningTeam + " was inserted."


@app.delete("/{id}", response_description="Remove a given set of game data by ID")
async def remove_gameInfo_byId(id: str):
    return app.database['pbp-nba'].delete_one(id)


def nbadata_helper(nbadata) -> dict:
    return {
        "GameType": str(NBAData["GameType"]),
        "Location": str(NBAData["Location"]),
        "Quarter": int(NBAData["Quarter"]),
        "SecLeft": int(NBAData["SecLeft"]),
        "Date": datetime(NBAData["Date"]),
        "WinningTeam": str(NBAData["WinningTeam"]),
        "HomeTeam": str(NBAData["HomeTeam"]),
        "HomeScore": int(NBAData["HomeScore"]),
        "AwayTeam": str(NBAData["AwayTeam"]),
        "AwayScore": int(NBAData["AwayScore"])
    }
