# Laboratorium nr 1

## *Asystent głosowy o funkcji kalkulatora prostego*

## Zadanie

### Treść

Stworzyć oprogramowanie prototypu głosowego systemu dialogowego zdolnego do wykonywania prostych operacji matematycznych (dodawanie, odejmowanie, mnożenie i dzielenie).
System rozpoznaje podane przez użytkownika dwie liczby całkowite i rodzaj operacji, którą następnie wykonuje i zwraca wynik.

### Format wiadomości

Użytkownik podaje polecenie zgodnie z ustalonym formatem wiadomości.

**`CMD_START` | `NUM_1` | `OP` | `NUM_2`**

gdzie:

`CMD_START` : Komenda inicjująca polecenie : jedno z <*Ile jest, Policz, Oblicz*>

`NUM_x` : liczba całkowita nr *x*

`OP` : Rodzaj operacji - jedno z <*dodać / plus, odjąć / minus, razy / mnożone przez, podzielić na / dzielone przez*>

Po zadanym poleceniu system wykonuje działanie zdefiniowane w `OP` na liczbach `NUM_1` i `NUM_2` oraz zwraca wynik operacji lub informuje o błędzie operacji, np. w przypadku polecenia dzielenia przez 0.

### Inne polecenia

Poza określonym powyżej poleceniem użytkowik może wydać jeszcze dwa inne polecenia pomocnicze:

`CMD_HELP` : Komenda pomocy - system informuje użytkownika o sposobie korzystania z systemu - jedno z <*pomoc*>

`CMD_STOP` : Komenda stop - wyłączenie programu - jedno z <*stop, wyłącz*>

---

## Realizacja

### Technologia

W celu realizacji zadania laboratoryjnego wykorzystano język programowania **Python** wraz z odpowiednimi modułami:

1. Rozpoznawanie mowy do postaci tekstowej : ***PyAudio, SpeechRecognition***

2. Synteza tekstu do postaci głosowej : ***pyttsx3***

Szczegółowe wymagania i zależności modułów określone w pliku [`requirements.txt`](code/requirements.txt).

### Kod źródłowy

Kod źródłowy programu dostępny jest katalogu [`code`](code/).

Punt wejścia programu zdefiniowano jako plik [`main.py`](code/main.py).

Klasy wykonawcze i zasoby pomocnicze zdefiniowano w submodule [`utils.py`](code/utils/__init__.py).
