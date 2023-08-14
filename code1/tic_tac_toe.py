import random

def game_start():
    table = [[0, 0 , 0],
             [0, 0, 0],
             [0, 0, 0]]
    return table


def put_mark(table, symbol, gamer, play_game):
    free_spaces = [] #miejsca wolne
    #sprawdzanie czy miejsce jest wolne
    for i, element in enumerate(table): #element - wiersz, i - indeks wiersza
        for position in element: #position - zawartość podanej listy
            if(position == 0):
                free_spaces.append((i,element.index(position))) #KROTKA!!

    if len(free_spaces) == 0: #??
        print("pola są pełne")
        play_game = 1
        for x in range(len(table)):
            print(table[x])
        return table, play_game
    else:
        #print(free_spaces)
        #for x in range(len(free_spaces)):
        #   print(free_spaces[x])
        #print(len(free_spaces))
        choose_place = random.randint(0, len(free_spaces) - 1) #-1 bo random jest a<=N<=b
        #print("rand liczba: ",choose_place)
        place = free_spaces[choose_place]
        #print("wybrane pole: ", place)
        table[place[0]][place[1]] = symbol

        return table, play_game



def check_if_win(table, play_game, gamer1_symbol, gamer2_symbol):
    # poziomo:
    for i, element in enumerate(table): #element - wiersz, i - indeks wiersza
        # poziomo:
        if(element[0] == element[1] == element[2] and element[0] != 0):
            play_game = 1
            if(element[0] == gamer1_symbol):
                print("congarats gamer1 won")
            else:
                print("congarats gamer2 won")

            print("[poziomo]")
            for x in range(len(table)):
                print(table[x])
            return play_game

    #pion - its hard :(
    if (table[0][0] == table[1][0] == table[2][0] and table[0][0] != 0):
        play_game = 1
        if (table[0][0] == gamer1_symbol):
            print("congarats gamer1 won")
        else:
            print("congarats gamer2 won")

        print("[pionowo]")
        for x in range(len(table)):
            print(table[x])
        return play_game
    if (table[0][1] == table[1][1] == table[2][1] and table[0][1] != 0):
        play_game = 1
        if (table[0][1] == gamer1_symbol):
            print("congarats gamer1 won")
        else:
            print("congarats gamer2 won")

        print("[pionowo]")
        for x in range(len(table)):
            print(table[x])
        return play_game
    if (table[0][2] == table[1][2] == table[2][2] and table[0][2] != 0):
        play_game = 1
        if (table[0][2] == gamer1_symbol):
            print("congarats gamer1 won")
        else:
            print("congarats gamer2 won")

        print("[pionowo]")
        for x in range(len(table)):
            print(table[x])
        return play_game

    #skos
    if(table[1][1] != 0 and (table[0][0] == table[1][1] == table[2][2] or
        table[0][2] == table[1][1] == table[2][0])):
        play_game = 1
        if (table[1][1] == gamer1_symbol):
            print("congarats gamer1 won")
        if (table[1][1] == gamer2_symbol):
            print("congarats gamer2 won")
        print("[skos]")
        for x in range(len(table)):
            print(table[x])
        return play_game

    return play_game

#============
#można zmienić na słownik jak chcesz być cool (i raczej się przyda przy dockerach)
gamer1 = "gamer1"
gamer1_symbol = "X"
gamer2 = "gamer2"
gamer2_symbol = "O" #big o. font issue
#==========
"""
table = [["X", "X", "X"],
         ["X", "X", "X"],
         ["X", "X", "X"]]
"""

#jesli nie ma trzech znakow jednego gracza, nie ma co sprawdzac czy wygrana
table = game_start()
play_game = 0 #flaga czy trwa rozgrywka

while(play_game == 0):
        table, play_game = put_mark(table, gamer1_symbol, gamer1, play_game)
        play_game = check_if_win(table, play_game, gamer1_symbol, gamer2_symbol)
        if (play_game == 1):
            break
        table, play_game = put_mark(table, gamer2_symbol, gamer2, play_game)
        play_game = check_if_win(table, play_game, gamer1_symbol, gamer2_symbol)
        if (play_game == 1):
            break
