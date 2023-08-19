from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import requests
import json
import psycopg2
import os
import random

app = FastAPI()

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

class Player(BaseModel):
    name: str
    surname: str

@app.get("/")
async def root():
    return {"message": ":3"}

#start rozgrywki
@app.post("/start")
def startGame(player1: Player, player2: Player):
    def check_if_exists_DB(cursor, cnxn, player_name, player_surname):
        query = f"SELECT EXISTS(SELECT 1 FROM players WHERE name='{player_name}' AND surname='{player_surname}')"
        try:
            cursor.execute(query)
        except Exception as e:
            query_result = str(e)
        else:
            cnxn.commit()
            query_result = cursor.fetchall()[0]

        return query_result

    def get_player_id(cursor, cnxn, player_name, player_surname):
        query = f"SELECT player_id FROM players WHERE name='{player_name}' AND surname='{player_surname}'"
        try:
            cursor.execute(query)
        except Exception as e:
            query_result = str(e)
        else:
            cnxn.commit()
            query_result = cursor.fetchall()[0]

        return query_result


    try:
        cursor, connection = dbconnect()
        player1_exist = check_if_exists_DB(cursor, connection, player1.name, player1.surname)
        player2_exist = check_if_exists_DB(cursor, connection, player2.name, player2.surname)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        cursor.close()
        connection.close()

    if(player1_exist[0] and player2_exist[0]): #jeśli tacy gracze są w DB:
        try:
            cursor, connection = dbconnect()
            player1_id = get_player_id(cursor, connection, player1.name, player1.surname)
            player2_id = get_player_id(cursor, connection, player2.name, player2.surname)
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
        finally:
            cursor.close()
            connection.close()

        if (player1_id != player2_id): #jeśli są to inni gracze
            data = {
                "input_json": {
                    "matrix":
                        [
                            [0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]
                        ],
                    "player1_id": player1_id[0],
                    "player2_id": player2_id[0],
                    "wins": {
                        "player1": 0,
                        "player2": 0,
                        "tie": 0
                    }
                }
            }

            who_starts = random.randint(0, 1)

            if(who_starts == 0):
                r = requests.post(url="http://player1:8000/putmark", data=json.dumps(data))

            else:
                r = requests.post(url="http://player2:8000/putmark", data=json.dumps(data))
            return {"msg": "rozpoczęto rozgrywke"}

        else:
            return {"msg": "Gracze muszą być różnymi osobami"}

    else:
        return {"msg": "Nie ma takich graczy; nie można odegrać rozgrywki"}


@app.get("/showPlayers")
def showPlayers():
    def players_from_DB(cursor, connection):
        result_query = []  # zapis wyników
        query = 'SELECT * FROM players'
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            row_dict = {}  # slowniki na rekordy
            for i, element in enumerate(row):
                row_dict[
                    columns[i]] = element
            result_query.append(row_dict)
        return result_query


    try:
        cursor, connection = dbconnect()
        query_result = players_from_DB(cursor, connection)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        print(query_result)
        cursor.close()
        connection.close()

    return query_result


@app.get("/stats")
def gamesStats():
    def show_games(cursor, connection):
        result_query = []
        query = 'SELECT * FROM games'
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            row_dict = {}
            for i, element in enumerate(row):
                row_dict[
                    columns[i]] = element
            result_query.append(row_dict)
        return result_query

    try:
        cursor, connection = dbconnect()
        query_result = show_games(cursor, connection)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        print(query_result)
        cursor.close()
        connection.close()

    return query_result

@app.put("/updateWins")
def winners(data: Data):
    def add_record(cursor, cnxn, winner, player1_id, player2_id):
        query_result = ""
        query = f"INSERT INTO games(game_id, date, result, player_id_one, player_id_two) " \
                f"VALUES (default, NOW(), '{winner}', {player1_id}, {player2_id});"

        try:
            cursor.execute(query)
        except Exception as e:
            query_result = str(e)
        else:
            cnxn.commit()
            query_result = cursor.fetchall()[0]

        return query_result

    wins = data.input_json["wins"]
    winner = ""
    query_result = ""

    if (wins["player1"] == 1):
        winner = "player1"
    if (wins["player2"] == 1):
        winner = "player2"
    if (wins["tie"] == 1):
        winner = "tie"

    player1_id = data.input_json["player1_id"]
    player2_id = data.input_json["player2_id"]


    try:
        cursor, connection = dbconnect()
        query_result = add_record(cursor, connection, winner, player1_id, player2_id)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        print(query_result)
        cursor.close()
        connection.close()
