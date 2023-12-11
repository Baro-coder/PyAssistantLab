# Laboratorium nr 2

## *Asystent głosowy o funkcji kalkulatora prostego - GUI*

## Zadanie

### Treść

Stworzyć oprogramowanie prototypu głosowego systemu dialogowego zdolnego do wykonywania prostych operacji matematycznych (dodawanie, odejmowanie, mnożenie i dzielenie).
System rozpoznaje podane przez użytkownika dwie liczby całkowite i rodzaj operacji, którą następnie wykonuje i zwraca wynik.

Oprogramowanie należy zrealizować jako aplikację desktopową z graficznym interfejsem użytkownika (GUI).

### Format wiadomości

Użytkownik podaje polecenie zgodnie z ustalonym formatem wiadomości.

**`CMD_START` | `NUM_1` | `OP` | `NUM_2`**

gdzie:

`CMD_START` : Komenda inicjująca polecenie : jedno z <*Ile jest*>

`NUM_x` : liczba całkowita nr *x*

`OP` : Rodzaj operacji - jedno z <*dodać / plus, odjąć / minus, razy / pomnożyć / podzielić*>

Po zadanym poleceniu system wykonuje działanie zdefiniowane w `OP` na liczbach `NUM_1` i `NUM_2` oraz zwraca wynik operacji lub informuje o błędzie operacji, np. w przypadku polecenia dzielenia przez 0.

Do zaimplementowania tej logiki użyto gramatyki zapisanej w [grammar.xml](SwpLab/grammar.xml).

### Inne polecenia

Poza określonym powyżej poleceniem użytkowik może wydać jeszcze dwa inne polecenia pomocnicze:

`CMD_CLS` : Komenda czyszczenia : aplikacja czyści interfejs z poprzedniego działania - <*wyczyść*>

---

## Realizacja

### Technologia

W celu realizacji zadania laboratoryjnego wykorzystano język programowania **C#** do wytworzenia aplikacji **WPF** we współpracy z framework'iem **.NET 4.7.2**.

Do operacji rozpoznawania i syntezy mowy wykorzystano **Microsoft Speech Platform**.

### Kod źródłowy

Zbudowano rozwiązanie Visual Studio: [`SwpLab`](SwpLab/).
