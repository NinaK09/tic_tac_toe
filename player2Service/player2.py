from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Dict
import json
import random
import requests

app = FastAPI()

class Data(BaseModel):
    input_json: Dict

@app.post("/putmark")
def putMark(data: Data):
    mark = 'Y' #duże O jest tak mało czytelne, have mercy
    sent_data = data.input_json
    table = data.input_json["matrix"]
    #for rows in table:
    #    print(rows)
    #print(table)

    free_spaces = []  # miejsca wolne
    for i, element in enumerate(table):  # element - wiersz, i - indeks wiersza
        for position in element:  # position - zawartość podanej listy
            if (position == 0):
                free_spaces.append((i, element.index(position)))  # KROTKA!!

    #wstawianie na miejsce
    choose_place = random.randint(0, len(free_spaces) - 1)  # -1 bo random jest a<=N<=b
    place = free_spaces[choose_place]
    table[place[0]][place[1]] = mark

    data.input_json["matrix"] = table
    data.input_json["whoseTurn"] = "player1"

    print("PLANSZA OBECNIE:")
    for rows in data.input_json["matrix"]:
        print(rows)

    data = check_if_win(data)

    wins = data.input_json["wins"]
    isWin = wins["player1"] + wins["player2"] + wins["tie"]
    if (isWin >= 1):
        json_compatible_data = jsonable_encoder(data)
        r = requests.put(url="http://judge:8000/updateWins", data=json.dumps(json_compatible_data))
    else:
        json_compatible_data = jsonable_encoder(data)
        r = requests.post(url="http://player1:8000/putmark", data=json.dumps(json_compatible_data))
    print("=================================================================")


def check_if_win(results):
    def clearMatrix():
        results.input_json["matrix"] = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def addPoint(key):
        results.input_json["wins"][key] += 1

    # GDY TABLICA JEST PELNA OBSULGA
    player1_symbol = 'X'
    player2_symbol = 'Y'

    table = results.input_json["matrix"]
    gameResult = results.input_json["wins"]


    free_spaces = []  # miejsca wolne
    for i, element in enumerate(table):  # elm - tablica, i - indeks
        for position in element:  # position - miejsce w tablicy
            if (position == 0 or position == '0'):
                free_spaces.append((i, element.index(position)))  # KROTKA!!

    if len(free_spaces) == 0:
        print("TIE")
        addPoint("tie")
        clearMatrix()
        return results

    # poziomo:
    for i, element in enumerate(table):  # element - wiersz, i - indeks wiersza
        # poziomo:
        if (element[0] == element[1] == element[2] and element[0] != 0):
            print("POZIOMO")
            if (element[0] == player1_symbol):
                print("player1 won")
                addPoint("player1")
                clearMatrix()
            else:
                print("player2 won")
                addPoint("player2")
                clearMatrix()
            return results

    # pion - its hard :(
    if (table[0][0] == table[1][0] == table[2][0] and table[0][0] != 0):
        print("PIONOWO 1")
        if (table[0][0] == player1_symbol):
            print("player1 won")
            addPoint("player1")
            clearMatrix()
        else:
            print("player2 won")
            addPoint("player2")
            clearMatrix()

        return results

    if (table[0][1] == table[1][1] == table[2][1] and table[0][1] != 0):
        print("PIONOWO 2")
        if (table[0][1] == player1_symbol):
            print("player1 won")
            addPoint("player1")
            clearMatrix()
        else:
            print("player2 won")
            addPoint("player2")
            clearMatrix()

        return results

    if (table[0][2] == table[1][2] == table[2][2] and table[0][2] != 0):
        print("PIONOWO 3")
        if (table[0][2] == player1_symbol):
            print("player1 won")
            addPoint("player1")
            clearMatrix()
        else:
            print("player2 won")
            addPoint("player2")
            clearMatrix()

        return results

    # skos
    if (table[1][1] != 0 and (table[0][0] == table[1][1] == table[2][2] or
                              table[0][2] == table[1][1] == table[2][0])):
        print("SKOS")
        if (table[1][1] == player1_symbol):
            print("player1 won")
            addPoint("player1")
            clearMatrix()
        if (table[1][1] == player2_symbol):
            print("player2 won")
            addPoint("player2")
            clearMatrix()
        return results

    return results

