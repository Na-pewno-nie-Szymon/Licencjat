# Ocena prawdopodobieństwa występowania wariantów sekwencji białkowych (BWT)

Projekt realizowany w celu weryfikacji i oceny wiarygodności wariantów sekwencji białkowych zidentyfikowanych przy pomocy Transformacji Burrowsa-Wheelera (BWT) w danych proteomicznych.

## Kontekst naukowy i problem badawczy
Obecne standardowe metody analizy danych proteomicznych z pomiarów spektrometrii mas pozwalają głównie na identyfikację tzw. kanonicznych sekwencji aminokwasowych. Powoduje to utratę cennych informacji o różnorodności populacyjnej, ponieważ proteom jest traktowany jako zamknięty zbiór, nieoddający różnic między osobnikami tego samego gatunku.

W **Pracowni Struktury Biopolimerów MWB** opracowano bazę danych [AliceDB](http://alicedb.ug.edu.pl/) oraz narzędzia bioinformatyczne pozwalające na identyfikację sekwencji unikalnych dla danego osobnika. Zastosowanie **Transformacji Burrowsa-Wheelera (BWT)** umożliwiło poszukiwanie wariantów jeszcze nieopisanych w literaturze. 

**Główny problem:** Zastosowanie BWT wiąże się ze znacznym prawdopodobieństwem otrzymania fałszywie pozytywnych identyfikacji. 

**Cel projektu:** Opracowanie metody odfiltrowania wyników fałszywie pozytywnych i ocena ich wiarygodności na podstawie prostych reguł funkcjonowania kodu genetycznego i prawdopodobieństwa wystąpienia danej mutacji.

## Zawartość repozytorium

W repozytorium znajdują się kluczowe pliki pozwalające na weryfikację zidentyfikowanych mutacji:

* `macierz_mutacji.csv` – Autorska macierz prawdopodobieństw podstawień (substytucji) aminokwasów, oparta na regułach kodu genetycznego. Wskazuje, z jakim prawdopodobieństwem dany aminokwas ("dziki" / *wild type*) może zmutować w inny w wyniku zmian na poziomie nukleotydów.
* `validate_ver_1.0.py` – Skrypt weryfikujący w języku Python. Przetwarza dane wyjściowe z identyfikacji (pliki `.tsv`), odczytuje mutacje i na podstawie macierzy przypisuje im prawdopodobieństwo wystąpienia.

## Jak działa walidator (`validate_ver_1.0.py`)?

Skrypt ładuje plik z wynikami (np. `hs_can_sp_...tsv`) oraz macierz podstawień. Dla każdego zidentyfikowanego peptydu:
1. Ekstrahuje aminokwas oryginalny (*wild type*) oraz zmutowany.
2. Sprawdza prawdopodobieństwo takiej zmiany w `macierz_mutacji.csv`.
3. Zapisuje wyniki do nowych plików `.csv`, dzieląc je na:
   * **Wszystkie warianty** (wraz z przypisanym prawdopodobieństwem).
   * **Warianty możliwe (possible)** – odfiltrowane tylko do tych, dla których prawdopodobieństwo mutacji jest większe niż `0`.

## Uruchomienie

### Wymagania
* Python 3.x
* Biblioteka `pandas`

Aby zainstalować wymagane pakiety, użyj:
```bash
pip install pandas