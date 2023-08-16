from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import requests
import json
import datetime
import psycopg2
import os
from dotenv import load_dotenv


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

def dbconnect():
    cnxn = psycopg2.connect(dbname=os.getenv('POSTGRES_DB'),
                            host='postgresTTT',
                            port=5432,
                            user=os.getenv('POSTGRES_USER'),
                            password=os.getenv('POSTGRES_PASSWORD'))
    print('Połączono z DB')
    return cnxn.cursor(), cnxn

class Data(BaseModel):
    input_json: Dict

@app.get("/")
async def root():
    print(os.getenv('POSTGRES_DB'))
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
    #ZMIEN NA BAZE DANYCH
    return winsGlobal

@app.put("/updateWins")
def winners(data: Data):
    def add_record(cursor, cnxn, winner):
        current_time = datetime.datetime.now()
        str_date_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
        query_result = ""

        query = f"INSERT INTO games VALUES (DEFAULT, NOW(), '{winner}') RETURNING game_id;"
        try:
            cursor.execute(query)
        except Exception as e:
            query_result = str(e)
        else:
            cnxn.commit()
            query_result = cursor.fetchall()[0]

        return query_result

    #sent_data = data.input_json
    wins = data.input_json["wins"]
    winner = ""

    global winsGlobal
    if (wins["player1"] == 1):
        winsGlobal["player1"] += 1
        winner = "player1"
    if (wins["player2"] == 1):
        winsGlobal["player2"] += 1
        winner = "player2"
    if (wins["tie"] == 1):
        winsGlobal["tie"] += 1
        winner = "tie"

    query_result = "uhoh"

    try:
        cursor, connection = dbconnect()
        query_result = add_record(cursor, connection, winner)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        print(query_result)
        cursor.close()
        connection.close()

    """
    with open('scoresVol/WinHistory.csv', 'a+') as f:
        f.write(str_date_time + ", " + str(winsGlobal)[1:-1] + ";\n")
    """

