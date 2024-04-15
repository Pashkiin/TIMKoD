from collections import defaultdict
import os
import random

def generuj_tekst(zrodlo_markowa, dlugosc_tekstu):
    tekst = []
    klucz = random.choice(list(zrodlo_markowa.keys()))  # losowy klucz
    for i in range(dlugosc_tekstu):
        tekst.append(klucz[1])  # dodaje słowo do tekstu
        mozliwe_klucze = [k for k in zrodlo_markowa if k[0] == klucz[1]]
        if mozliwe_klucze:
            wagi = [zrodlo_markowa[k] for k in mozliwe_klucze]
            klucz = random.choices(mozliwe_klucze, weights=wagi, k=1)[0]
        else:
            klucz = random.choice(list(zrodlo_markowa.keys()))
    return ' '.join(tekst)

def generuj_tekst2(zrodlo_markowa, dlugosc_tekstu, start_word=None):
    tekst = []
    # Find a key that starts with the start_word
    if start_word is not None:
        klucz = next((k for k in zrodlo_markowa.keys() if k[0][0] == start_word), None)
    else:
        print(f"No key found , using a random key instead.")
        klucz = random.choice(list(zrodlo_markowa.keys()))  # losowy klucz
        
    slowo  =  klucz[0][0]
    slowo2 = klucz[0][1]
    tekst.append(slowo)  # convert tuple to string and add to tekst
    tekst.append(slowo2)  # convert tuple to string and add to tekst

    for i in range(dlugosc_tekstu - 2):  # -2 because two words are already added
        mozliwe_klucze = [k for k in zrodlo_markowa if k[:2] == klucz]
        if mozliwe_klucze:
            wagi = [zrodlo_markowa[k] for k in mozliwe_klucze]
            klucz = random.choices(mozliwe_klucze, weights=wagi, k=1)
            slowo = klucz[0][1]
            tekst.append(slowo)  # convert tuple to string before adding to tekst
        else:
            klucz = random.choice(list(zrodlo_markowa.keys()))
            slowo = klucz[0]
            tekst.extend(slowo)  # convert tuple to string and add to tekst
    return ' '.join(tekst)

def wczytaj_plik_do_tabeli(nazwa_pliku):
    tabela_slow = []
    try:
        with open(nazwa_pliku, 'r') as plik:
            for linia in plik:
                slowa_w_linii = linia.split()  # dzieli linię na słowa
                tabela_slow.extend(slowa_w_linii)  # dodaje słowa do tabeli
    except FileNotFoundError:
        print("Plik", nazwa_pliku, "nie został znaleziony.")
        print("Zawartość bieżącego folderu:", os.listdir())  # wyświetla zawartość folderu
    return tabela_slow

def tabela_markowa(tabela_slow, order):
    tabela_markowa = defaultdict(int)
    for i in range(len(tabela_slow) - order):
        klucz = tuple(tabela_slow[i:i+order])
        wartosc = tabela_slow[i+order]
        tabela_markowa[klucz, wartosc] += 1
    return tabela_markowa

def analiza_slow(tabela_slow):
    unikalne_slowa = set(tabela_slow)
    liczba_roznych_slow = len(unikalne_slowa)
    procentB = (30000 / liczba_roznych_slow) * 100
    procent = (6000 / liczba_roznych_slow) * 100
    print("Liczba różnych słów w tabeli:", liczba_roznych_slow)
    print("Procent 30000 z liczby różnych słów:", procentB, "%")
    print("Procent 6000 z liczby różnych słów:", procent, "%")

def main():
    # Przykładowe użycie:
    nazwa_pliku = 'norm_wiki_sample.txt'  # zastąp 'tekst.txt' nazwą swojego pliku
    tabela_slow = wczytaj_plik_do_tabeli(nazwa_pliku)
    tabela_markowa_pierwszy = tabela_markowa(tabela_slow,1)
    tabela_markowa_drugi = tabela_markowa(tabela_slow,2)

    # Wygenerowanie tekstu
    dlugosc_tekstu = 100
    wygenerowany_tekst_pierwszy = generuj_tekst(tabela_markowa_pierwszy, dlugosc_tekstu)
    wygenerowany_tekst_drugi = generuj_tekst2(tabela_markowa_drugi, dlugosc_tekstu)
    wygenerowany_tekst_drugi_prob = generuj_tekst2(tabela_markowa_drugi, dlugosc_tekstu, start_word="probability")
    analiza_slow(tabela_slow)
    print("Wygenerowany tekst dla pierwszego rzędu:", wygenerowany_tekst_pierwszy)
    print("##############################################################################################################")
    print("Wygenerowany tekst dla drugiego rzędu:", wygenerowany_tekst_drugi)
    print("##############################################################################################################")
    print("Wygenerowany tekst dla drugiego rzędu z początkiem probability:", wygenerowany_tekst_drugi_prob)

    # # Wyświetlenie tabeli markowej
    # for para, czestosc in tabela_markowa.items():
    #     print(para, ":", czestosc)

if __name__ == "__main__":
    main()