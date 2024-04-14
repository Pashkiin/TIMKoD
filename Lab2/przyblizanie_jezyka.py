from collections import defaultdict
import os
import random

def generuj_tekst(zrodlo_markowa, dlugosc_tekstu):
    order = len(next(iter(zrodlo_markowa.keys()))) - 1
    poczatkowe_slowa = random.choice(list(zrodlo_markowa.keys()))
    wygenerowany_tekst = []
    for slowo in poczatkowe_slowa:
        wygenerowany_tekst.append(slowo)
        wygenerowany_tekst.append(' ')

    while len(wygenerowany_tekst) < dlugosc_tekstu:
        ostatnie_slowa = tuple(wygenerowany_tekst[-order:])
        mozliwe_klucze = [klucz for klucz in zrodlo_markowa.keys() if klucz[:order] == ostatnie_slowa]
        if not mozliwe_klucze:
            break
        wagi = [zrodlo_markowa[klucz] for klucz in mozliwe_klucze]
        wybrany_klucz = random.choices(mozliwe_klucze, weights=wagi, k=1)[0]
        nastepne_slowo = wybrany_klucz[order]
        wygenerowany_tekst.append(' ')
        wygenerowany_tekst.append(nastepne_slowo)

    return wygenerowany_tekst

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
    wygenerowany_tekst_drugi = generuj_tekst(tabela_markowa_drugi, dlugosc_tekstu)
    analiza_slow(tabela_slow)
    print("Wygenerowany tekst dla pierwszego rzędu:", wygenerowany_tekst_pierwszy)
    print("##############################################################################################################")
    print("Wygenerowany tekst dla drugiego rzędu:", wygenerowany_tekst_drugi)

    # # Wyświetlenie tabeli markowej
    # for para, czestosc in tabela_markowa.items():
    #     print(para, ":", czestosc)

if __name__ == "__main__":
    main()