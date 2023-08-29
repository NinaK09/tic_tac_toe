#!/bin/bash

function showPlayers() {
    curl -X 'GET' \
  'http://localhost:8000/showPlayers' \
  -H 'accept: application/json' | json_pp
}

function startGame(){
  echo "podaj ID graczy, między którymi ma się odbyć pojedynek"
  echo "gracz pierwszy: "
  declare -i player1
  read player1

  echo "gracz drugi: "
  declare -i player2
  read player2

  curl -X 'POST' \
  'http://localhost:8000/start?player1_id='$player1'&player2_id='$player2'' \
  -H 'accept: application/json' \
  -d '' | json_pp
}

function showGames(){
  echo "czy chcesz zastosować filtry? y/n"
  read filtrYN
  URL="http://localhost:8000/showGames/?"

  if [ $filtrYN == y ]; then
    echo "czy chcesz zastosować filtry zwiazane z remisem?"
    echo "rozgrywki zakonczone remisem - T"
    echo "rozgrywki nie zakonczone remisem - NT"
    echo "nie chce stosowac filtru - N"
    read filtrTIE

    echo "czy chcesz wyswietlić gry, w jakich brał udział użytkownik o danym ID? jeśli tak, podaj id jako liczbę"
    declare -i filtrID
    read filtrID
    echo $filtrID

    echo "Czy chcesz wyświetlić rozgrywki, przeprowadzone OD podanej daty? jeśli tak, podaj datę w formacie RRRR-MM-DD"
    read filtrDataSince

    echo "Czy chcesz wyświetlić rozgrywki, przeprowadzone DO podanej daty? jeśli tak, podaj datę w formacie RRRR-MM-DD"
    read filtrDataTo

  is_smth_query=False #flaga sprawdzajaca, czy będzie potrzebny '&' w query

  #tworzenie poprawnego URl
    if [ $filtrTIE == T ]; then
      URL+=game_result=tie
      is_smth_query=True
    elif [ $filtrTIE == NT ]; then
      URL+=game_result=notTie
      is_smth_query=True
    fi

    re='^[0-9]+$' #regex - do sprawdzenia czy ID jest liczbą
    if [[ $filtrID =~ $re && $filtrID -gt 0 ]]; then
      if [ $is_smth_query == True ]; then
        URL+=\&player_id=${filtrID}
      else
        URL+=player_id=${filtrID}
        is_smth_query=True
      fi
    fi

    if [ ${#filtrDataSince} -gt 9 ]; then
      if [ $is_smth_query == True ]; then
        URL+=\&data_since=${filtrDataSince}
      else
        URL+=data_since=${filtrDataSince}
        is_smth_query=True
      fi
    fi

    if [ ${#filtrDataTo} -gt 9 ]; then
      if [ $is_smth_query == True ]; then
        URL+=\&data_to=${filtrDataTo}
      else
        URL+=data_to=${filtrDataTo}
        is_smth_query=True
      fi
    fi
  fi
    #echo $URL

  curl -X 'GET' \
  $URL \
  -H 'accept: application/json' | json_pp

}

function addPlayer(){
  echo "podaj imie gracza"
  read name

  echo "podaj nazwisko gracza"
  read surname

  curl -X 'POST' \
  'http://localhost:8000/addPlayers' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "'$name'",
  "surname": "'$surname'"
}'
}


echo "Co chcesz zrobić?"
echo "1 - rozpocznij rozgrywkę"
echo "2 - wyswietl rozgrywki"
echo "3 - wyświetl graczy"
echo "4 - dodaj gracza"

read choice

if [ $choice == 1 ]; then
  echo "rozpoczynamy rozgrywkę"
  startGame
elif [ $choice == 2 ]; then
  echo "wyswietlam gry"
  showGames
elif [ $choice == 3 ]; then
  echo "wyswietlam graczy"
  showPlayers
elif [ $choice == 4 ]; then
  echo "dodawanie gracza"
  addPlayer
else
  echo "wybierz poprawną opcję"
fi