## Praca dyplomowa
#### Uniwersytet Wrocławski \n Instytut informatyki \\ Alicja Danilczuk i Klaudia Osowska \\ Luty 2021

Pliki umieszczone w repozytorium służą do prezentacji i przetestowania działania algorytmów omówionych w pracy "Implementacja i omówienie algorytmów analizujących dźwięki z perspektywy porównywania utworów". W skład repozytorium wchodzą programy obliczające wyniki algorytmów zatytułowanymi ich nazwami oraz pliki pomocnicze służące do szybszej obsługi programów, przekazywania danych z dokumentów txt oraz generowania dokumentów prezentujących ich działanie.

Zaprezentowane pliki to zgodnie ze strukturą pracy:
1. magnitudeMethod.py
2. shortTermEnergyMethod.py
3. surfMethod.py
4. envelopeMatchFilter.py
5. markThePlot.py

    Do ich uruchomienia potrzeba nazwy nagrania w pliku wav podanej bez rozszerzenia. W pierwszych czterech można zmieniać wartości stałych (wielkość okna, próg oraz epsilon) a ich działanie jest automatyczne. Ostatnia Daje możliwość samodzielnego zaznaczenia pożądanych początków dźwięków (ang. onsets), następnie zapisuje ich wynik do pliku Onsets.txt w formacie: nazwa_piosenki kolejne_indeksy_wartości_w_których_zaznaczono_onset.
6. autocorrelationFunction.py
7. averageMagnitudeDifferenceFunction.py
8. harmonicProduct.py
9. thirdBiggestFft.py
10. cepstralMethod.py

    Działanie każdego z powyższych pięciu programów uruchamia funkcja calculatePitchExtraction z parametrem nazwy nagrania jak w poprzednich funkcjach. Dane do obliczania częstotliwości pobierane są z pliku Onsets.txt za pomocą funkcji loadOnsetsFromFile.py, w razie nieobecności nagrania o szukanej nazwie w analizowanych pliku użytkownik dostanie pytanie o to skąd pobrane mają być dane o początkach dźwięków - zaznaczone ręcznie funkcją markThePlot czy wyliczone za pomocą envelopeMatchFilter. Dodatkowo calculatePitchExtraction w cepstralMethod.py przyjmuje parametr version oznaczające, którą wersją z pracy chcemy wyliczyć wysokości dźwięków (1 lub 2).
11. comparePitchExtractionMethods.py

    Dwie najważniejsze funkcje w powyższym pliku to: chooseNotes, która uruchamia 8., 9., 10.1 i 10.2 i na ich podstawie zwraca najczęściej występujące nuty według schematu opisanego w pracy, oraz comparePitchResults -- może ona wyświetlać porównanie wyników dla wszystkich funkcji wyliczajacych częstotliwości i zapisywać tożsame im nuty do pliku NoteCalculations.txt.
12. dynamicProgramming.py
13. linearScaling.py

    Działanie porównania melodii poprzez programowanie dynamiczne rozpocząć można uruchamiając funkcję dynamic_programming z wyliczonymi w poprzednim kroku częstotliwościami (np. wczytanymi z pliku FrequenciesCalculations.txt za pomocą funkcji loadFreqsFromFile.py) oraz nazwą pliku MIDI z którym chcemy porównać nagranie. Natomiast linearScaling.py uruchamia się funkcją linearScaling, tak samo z częstotliwościami i nazwą pliku MIDI, jednak potrzeba jeszcze listy czasów, w których pojawiają się te częstotliwości. Można je uzyskać ładując onsety za pomocą loadOnsetsFromFile.py i każdy element dzieląc przez ilość klatek na sekundę nagrania. 
