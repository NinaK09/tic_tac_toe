from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import requests
import json
import datetime


winsGlobal = { #zapamietywanie wynikow rozgrywek
    "player1": 0,
    "player2": 0,
    "tie": 0
}

app = FastAPI()

"""
    data:
    {
        matrix: {[[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]},
        whoseTurn: "player1"/"player2", #domyslnie 1 zaczyna, moge zmienic ze zaczyna loser
        wins: {
                player1: /liczba/,
                player2: /liczba/,
                tie: /liczba/
            }
        #winner: "None"/"player1"/"player2"
    }

"""

class Data(BaseModel):
    input_json: Dict

@app.get("/")
async def root():
    return {"message": "Haii :3"}

#start rozgrywki
@app.get("/start")
def startGame():
    #czysty słownik na start
    data = {
        "input_json": {
            "matrix":
                    [
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                    ],
        "whoseTurn": "player1",
        "wins": {
                "player1": 0,
                "player2": 0,
                "tie": 0
            }
        }
    }

    #pierwsze przeslanie pustego jsona
    r = requests.post(url="http://player1:8000/putmark", data=json.dumps(data)) #json.dumps() - wysylasz klase BASEMODEL

    return {"game": "has started"}

@app.get("/stats")
def gamesStats():
    #pobieramy ze zmiennej globalnej wyniki
    return winsGlobal

@app.put("/updateWins")
def winners(data: Data):
    #sent_data = data.input_json
    wins = data.input_json["wins"]

    global winsGlobal
    if (wins["player1"] == 1):
        winsGlobal["player1"] += 1
    if (wins["player2"] == 1):
        winsGlobal["player2"] += 1
    if (wins["tie"] == 1):
        winsGlobal["tie"] += 1

    current_time = datetime.datetime.now()
    str_date_time = current_time.strftime("%d-%m-%Y %H:%M:%S")

    with open('scoresVol/WinHistory.csv', 'a+') as f:
        f.write(str_date_time + ", " + str(winsGlobal)[1:-1] + ";\n")
