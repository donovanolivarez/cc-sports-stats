#!/usr/bin/env python3
from typing import List, Dict

from models import NBAData
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import certifi
import json

app = FastAPI()

@app.get("/")
def read_root():
    client = get_database()
    print(client)
    return {"Hello": "World"}

@app.get("/teams", response_description="List all NBA teams", response_model=List[str])
def get_teams():
    mycol = get_database()
    teams = list(mycol.find().distinct("HomeTeam"))
    return teams

@app.get("/teams/{team_id}", response_description="List all the games of the given team", response_model=List[NBAData], response_model_exclude_none=True)
def get_team_info(team_id: str):
    count = 0
    mycol = get_database()
    myQuery = {"WinningTeam": team_id, "Quarter": 4, "SecLeft": 0, "AwayPlay":"End of Game"}
    results = mycol.find(myQuery)
    print(results)
    nba_data = [NBAData(**doc).model_dump() for doc in results]
    # for doc1 in results:
    #     count = count + 1
    #     print(doc1)
    #     print(NBAData(**doc1))

    myString = "The total number of games won by " + team_id + " was " + str(count)
    return nba_data


@app.post("/teams/{team_id}/gameInfo", response_description="Create a new entry for game data")
async def create_gameInfo(gameInfo: NBAData):
    return gameInfo

@app.delete("/{id}", response_description="Remove a given set of game data by ID")
async def remove_gameInfo_byId(id: str):
    mycol = get_database()
    return mycol.delete_one(id)


def get_database(): 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
#    CONNECTION_STRING = "mongodb+srv://heyubaidullah:LroLDx3UdCyQO5fA@cc-sports-stat-cluster.ruyzwup.mongodb.net/?retryWrites=true&w=majority&appName=cc-sports-stat-cluster"
   CONNECTION_STRING = "mongodb+srv://ep1085:HXExdlceJdiMIcem@cluster0.s1reytw.mongodb.net/"
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
   db = client['cc-sports-stats-nba']
   table = db['2019-2020']
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return table

"""
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
"""
