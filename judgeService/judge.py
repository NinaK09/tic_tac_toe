from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from enum import Enum
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


@app.get("/")
async def root():
    return {"message": ":3"}


# start rozgrywki
@app.post("/start")
def startGame(player1_id: int, player2_id: int):
    def check_if_exists_DB(cursor, cnxn, player_id):
        query = f"SELECT EXISTS(SELECT 1 FROM players WHERE player_id = {player_id})"
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
        player1_exist = check_if_exists_DB(cursor, connection, player1_id)
        player2_exist = check_if_exists_DB(cursor, connection, player2_id)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        cursor.close()
        connection.close()

    print(player2_exist)

    if (player1_exist[0] and player2_exist[0] and (player1_id != player2_id)):  # jeśli są to inni gracze
        data = {
            "input_json": {
                "matrix":
                    [
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                    ],
                "player1_id": player1_id,
                "player2_id": player2_id,
                "wins": {
                    "player1": 0,
                    "player2": 0,
                    "tie": 0
                }
            }
        }

        who_starts = random.randint(0, 1)

        if (who_starts == 0):
            r = requests.post(url="http://player1:8000/putmark", data=json.dumps(data))

        else:
            r = requests.post(url="http://player2:8000/putmark", data=json.dumps(data))
        return {"msg": "rozpoczęto rozgrywke"}

    else:
        return {"msg": "nie można odegrać rozgrywki"}



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

class Player(BaseModel):
    name: str
    surname: str
@app.post("/addPlayers")
def addPlayers(player: Player):
    def add_players(cursor, cnxn, name, surname):
        result_query = []  # zapis wyników
        query = f"INSERT INTO public.players(player_id, name, surname) VALUES (default, '{name}', '{surname}') " \
                f"RETURNING player_id;"
        try:
            cursor.execute(query)
        except Exception as e:
            result_query = str(e)
        else:
            cnxn.commit()
            result_query = cursor.fetchall()[0]
        return result_query

    try:
        cursor, connection = dbconnect()
        query_result = add_players(cursor, connection, player.name, player.surname)
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        cursor.close()
        connection.close()

    return query_result

class TieMode(str, Enum):
    notTie = "notTie"
    tie = "tie"

@app.get("/showGames/")
def filterResults(game_result: TieMode = None, player_id: int = None, data_since: str = None, data_to: str = None):
    def isTie(cursor, connection, mode=None, player=None, data_since=None, data_to=None):
        result_query = []
        filtr = 0
        query = f"SELECT * FROM public.games WHERE "

        if (mode is None and player_id is None and data_since is None and data_to is None):
            query = 'SELECT * FROM games'

        if (mode == 'tie'):
            query += f"result = 'tie'"
            filtr += 1
        if (mode == 'notTie'):
            query += f"result NOT IN ('tie')"
            filtr += 1
        if (player):
            if (filtr >= 1):
                filtr += 1
                query += f" AND (player_id_one = {player_id} OR player_id_two = {player_id})"
            else:
                filtr += 1
                query += f" (player_id_one = {player_id} OR player_id_two = {player_id})"

        if (data_since):
            if (filtr >= 1):
                filtr += 1
                query += f" AND date > '{data_since}'"
            else:
                filtr += 1
                query += f" date > '{data_since}'"

        if (data_to):
            if (filtr >= 1):
                filtr += 1
                query += f" AND date < '{data_to}'"
            else:
                filtr += 1
                query += f" date < '{data_to}'"

        print(query)
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            row_dict = {}
            for i, element in enumerate(row):
                row_dict[
                    columns[i]] = element
            result_query.append(row_dict)
        return result_query

    # czy remis czy nie

    try:
        cursor, connection = dbconnect()
        query_result = isTie(cursor, connection, game_result, player_id, data_since, data_to)
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
