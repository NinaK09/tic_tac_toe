from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import requests
import json


winsGlobal = { #zapamietywanie wynikow rozgrywek
    "player1": 0,
    "player2": 0,
    "tie": 0
}


app = FastAPI()
#PORT: 8000

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
    #czysty słownik startowy
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

    #obecnie po wygranej pierwszy ruch ma ten, na ktorym skonczylo sie sprawdzanie

    #pierwsze wyslanie czystego jsona
    r = requests.put(url="http://player1:8000/putmark", data=json.dumps(data)) #json.dumps() - wysylasz rodzaj BASEMODEL
    global winsGlobal #bez tego nie da sie modyfikowac zawartosci
    isWin = 0
    whoWon = "none"

    while(True):
        dataR = r.json() #r.json() zmienia uzyskany wynik na zwykły Dict. nie traktuj go jak json/dict z basemodel
        wins = dataR["input_json"]["wins"]
        isWin = wins["player1"] + wins["player2"] + wins["tie"] #ilość wygranych
        if(isWin >= 1): #jesli wystapila wygrana:
            if(wins["player1"] == 1):
                winsGlobal["player1"] += 1
                whoWon = "player1"
            if (wins["player2"] == 1):
                winsGlobal["player2"] += 1
                whoWon = "player2"
            if (wins["tie"] == 1):
                winsGlobal["tie"] += 1
                whoWon = "tie"
            break
        #===przeslanie do player2===
        rr = requests.put(url="http://player2:8000/putmark", data=json.dumps(dataR)) #8000, bo taki jest domyslny dla uvicorna
        dataRR = rr.json()
        wins = dataRR["input_json"]["wins"]
        isWin = wins["player1"] + wins["player2"] + wins["tie"]  # ilość wygranych
        if (isWin >= 1):  #jesli wystapila wygrana:
            if (wins["player1"] == 1):
                winsGlobal["player1"] += 1
                whoWon = "player1"
            if (wins["player2"] == 1):
                winsGlobal["player2"] += 1
                whoWon = "player2"
            if (wins["tie"] == 1):
                winsGlobal["tie"] += 1
                whoWon = "tie"
            break
        #==ponowne przeslanie do player1===
        r = requests.put(url="http://player1:8000/putmark", data=json.dumps(dataRR))

    return {"winner": whoWon}

@app.get("/stats")
def gamesStats():
    #pobieramy z zmiennej globalnej wyniki
    return winsGlobal
