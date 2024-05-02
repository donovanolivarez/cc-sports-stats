#!/usr/bin/env python3

from typing import Union
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()


@app.get("/")
def read_root():
    client = get_database()
    print(client)
    return {"Hello": "World"}


@app.get("/sports-data/stats/nba/teams")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/sports-data/stats/nba/teams/{team_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"team_id": item_id, "q": q}

@app.get("/sports-data/stats/nba/teams/{team_id}/wins)
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def get_database(): 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://heyubaidullah:LroLDx3UdCyQO5fA@cc-sports-stat-cluster.ruyzwup.mongodb.net/?retryWrites=true&w=majority&appName=cc-sports-stat-cluster"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['user_shopping_list']

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
