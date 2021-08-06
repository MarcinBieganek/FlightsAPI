# FlightsAPI
## Projekt prostego API z funkcjami dla lotów

Projekt realizowany w ramach przedmiotu Bazy Danych na Uniwersytecie Wrocławskim w czerwcu 2021. Autor: Marcin Bieganek.
Program jest napisany w języku Python. Projekt wykorzystuje PostgreSQL.

Jest to proste API, które przyjmuje zapytania w formcie JSON na standardowe wejście i zwraca odpowiedzi w formacie JSON na standardowe wyjście. Baza danych jest przechowywana lokalnie.

### Baza Danych

Zakładamy, że w Bazie Danych są dwie tabele Airport oraz City, które są już wypełnione danymi. Dodatkowo przy pierwszym uruchomieniu program tworzy tabelę Flight Segment wraz z indeksem geograficznym, która będzie przechowywać informację o fragmentach lotów. Na kolumnie route tabeli Flight Segment został wykorzystany indeks GIST w celu optymalizacji zapytań.

### Format JSON

Zapytania API w formacie JSON mają dwa pola: nazwę funkcji i opcjonalne parametry. Przykładowe zapytanie:
```=
{
   "function":"flight",
   "params":{
      "id":"12345",
      "airports":[
         {
            "airport":"WAW",
            "takeoff_time":"2021-06-01 20:26:44.229109+02"
         },
         {
            "airport":"WRO",
            "takeoff_time":"2021-06-01 21:46:44.229109+02",
            "landing_time":"2021-06-01 21:26:44.229109+02"
         },
         {
            "airport":"GDN",
            "landing_time":"2021-06-01 22:46:44.229109+02"
         }
      ]
   }
}
```

Odpowiedż API w formacie JSON ma dwa pola: status oraz data.

Przykładowe zapytania można zobaczyć w pliku examples.txt.

### Funkcje

#### flight

Dodaje lot o podanym id i trasie lotu. Trasa lotu to lista lotnisk wraz z czasem przylotu i odlotu.

#### list_flights

Zwraca informacje o segmentach lotów, które przecinają się z dowolnym segmentem lotu o podanym id. Zwraca id lotu, kod IATA lotniska startu i lądowania oraz czas startu.

#### list_cities

Zwraca listę miast oddalonych mniej niż podana odległość od lotu o podanym id.

#### list_airport

Zwraca listę n ostatnich lotów startujących z lotniska o podanym id.

#### list_city

Zwraca listę n ostatnich lotów przelatujących w odległości mniejszej niż podany dist od podanego miasta.

### Użycie

###### Pierwsze uruchomienie

W celu rozpoczęcia działania systemu należy wykonać polecenie: **python3 app.py --init**.
Należy to zrobić przed pierwszym użyciem.

###### Dalsze użytkowanie

Zapytania można wykonywać na dwa sposoby: przekierować na standardowe wejście zawartość pliku z zapytaniami lub w trybie interaktywnym.

Przykład użycia korzystając z pliku. Powiedzmy, że mamy przygotowany plik req.txt w ktróym w każdej linii znajduje się jedno zapytania API w formacie JSON.
W takiej sytuacji należy wykonać polecenie: **python3 app.py < req.txt**.
Program wypisze na standardowe wyjście w kolejnych liniach odpowiedzi na kolejne zapytania API w formacie JSON.

Przykład użycia korzystając z trybu interaktywnego. Program uruchamiamy poleceniem: **python3 app.py**. W jednej lini wpisujemy nasze zapytanie API w formacie JSON. Po zatwierdzeniu klawiszem ENTER program wypisze jedną linię z odpowiedzią na to zapytanie w formacie JSON.
Gdy chcemy zakończyć pracę, wystarczy zatwierdzić klawiszem ENTER pustą linię.
