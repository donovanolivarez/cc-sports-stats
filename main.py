#!/usr/bin/env python3

from typing import Union
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()


@app.get("/")
def read_root():
    client = get_database()
    print(client)
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def get_database(): 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = ""
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['user_shopping_list']