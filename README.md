# Ocena prawdopodobieństwa występowania wariantów sekwencji białkowych (BWT)

Projekt realizowany w celu weryfikacji i oceny wiarygodności wariantów sekwencji białkowych zidentyfikowanych przy pomocy Transformacji Burrowsa-Wheelera (BWT) w danych proteomicznych.

## Kontekst naukowy i problem badawczy
Obecne standardowe metody analizy danych proteomicznych z pomiarów spektrometrii mas pozwalają głównie na identyfikację tzw. kanonicznych sekwencji aminokwasowych. Powoduje to utratę cennych informacji o różnorodności populacyjnej, ponieważ proteom jest traktowany jako zamknięty zbiór, nieoddający różnic między osobnikami tego samego gatunku.

W **Pracowni Struktury Biopolimerów MWB** opracowano bazę danych [AliceDB](http://alicedb.ug.edu.pl/) oraz narzędzia bioinformatyczne pozwalające na identyfikację sekwencji unikalnych dla danego osobnika. Zastosowanie **Transformacji Burrowsa-Wheelera (BWT)** umożliwiło poszukiwanie wariantów jeszcze nieopisanych w literaturze. 

**Główny problem:** Zastosowanie BWT wiąże się ze znacznym prawdopodobieństwem otrzymania fałszywie pozytywnych identyfikacji. 

**Cel projektu:** Opracowanie metody odfiltrowania wyników fałszywie pozytywnych i ocena ich wiarygodności na podstawie prostych reguł funkcjonowania kodu genetycznego i prawdopodobieństwa wystąpienia danej mutacji.

## Zawartość repozytorium

W repozytorium znajdują się kluczowe pliki pozwalające na weryfikację zidentyfikowanych mutacji:

* `macierz_prawdopodobienstw_1_literowa.csv` – Macierz prawdopodobieństw podstawień (substytucji) aminokwasów, oparta na regułach kodu genetycznego. Wskazuje, z jakim prawdopodobieństwem dany aminokwas ("dziki" / *wild type*) może zmutować w inny w wyniku zmian na poziomie nukleotydów.
* `validate_2.0.py` – Zaktualizowany skrypt weryfikujący. Przetwarza dane wyjściowe (pliki `.tsv`), przypisuje prawdopodobieństwa oraz generuje zaawansowane wizualizacje wyników.

## Jak działa walidator (wersja 2.0)?

Skrypt ładuje plik z wynikami oraz macierz podstawień. Przetwarzanie odbywa się w paczkach (*chunks*), co pozwala na analizę bardzo dużych zbiorów danych SNP. Dla każdego wariantu:
1. Ekstrahuje aminokwas oryginalny oraz zmutowany.
2. Sprawdza prawdopodobieństwo zmiany w macierzy.
3. Zapisuje wyniki do plików:
   * `_all.tsv` – wszystkie warianty z przypisanym prawdopodobieństwem.
   * `_possible.tsv` – tylko warianty o prawdopodobieństwie wyższym niż 0.

### Wizualizacja i Statystyki
Nowa wersja skryptu automatycznie generuje wykresy analityczne:
* **Rozkład prawdopodobieństw (Histogramy)**: Zestawienie skali liniowej i logarytmicznej. Skala logarytmiczna pozwala na dokładną analizę rzadkich, ale biologicznie dopuszczalnych wariantów.
* **Analiza najczęstszych podstawień**: Wykres słupkowy prezentujący 15 najczęściej występujących typów mutacji (np. L -> I) w badanym zbiorze danych, co pozwala na szybką ocenę trendów biologicznych w bazie.

## Uruchomienie

### Wymagania
* Python 3.x
* Biblioteki: `pandas`, `matplotlib`, `seaborn`, `tqdm`

Instalacja wymaganych pakietów:
```bash
pip install pandas matplotlib seaborn tqdm