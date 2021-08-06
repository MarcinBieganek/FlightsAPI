# FlightsAPI
## Projekt prostego API z funkcjami dla lotów

Projekt realizowany w ramach przedmiotu Bazy Danych na Uniwersytecie Wrocławskim w czerwcu 2021. Autor: Marcin Bieganek.
Program jest napisany w języku Python. Projekt wykorzystuje PostgreSQL.

Jest to proste API, które przyjmuje zapytania w formcie JSON na standardowe wejście i zwraca odpowiedzi w formacie JSON na standardowe wyjście. Baza danych jest przechowywana lokalnie.

### Baza Danych

Zakładamy, że w Bazie Danych są dwie tabele Airport oraz City, które są już wypełnione danymi. Dodatkowo przy pierwszym uruchomieniu program tworzy tabelę Flight Segment wraz z indeksem geograficznym, która będzie przechowywać informację o fragmentach lotów.

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
