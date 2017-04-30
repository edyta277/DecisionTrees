import operator
from math import log

def liczenieEntropii(zbiorDanych):
    liczbaInstancji = len(zbiorDanych) #liczba instancji w zbiorze danych
    liczbaEtykiet = {} #slownik (tablica indeksowana kluczami) -kluczami beda wartosci  ostatniej kolumny
    for element in zbiorDanych: #dla kazdej cechy w zbiorze danych
        aktualnaEtykieta = element[-1] #aktualna etykieta =...?
        if aktualnaEtykieta not in liczbaEtykiet.keys(): #jezeli currentLabel nie jest juz kluczem w LabelCounts (klucze nie moga sie powtarzac)
            liczbaEtykiet[aktualnaEtykieta] = 0 #wtedy liczba wynosi 0
        liczbaEtykiet[aktualnaEtykieta] += 1 #dodanie jednego
    entropia = 0.0 #przypisanie wartosci 0.0
    for key in liczbaEtykiet: #dla kazdego klucza
        prawdopodobienstwo = float(liczbaEtykiet[key])/liczbaInstancji #prawdopodobienstwo=liczbawystapien etykiety/liczba instancji
        entropia -= prawdopodobienstwo * log(prawdopodobienstwo, 2) #odjęcie wartosci
    return entropia #zwrocenie shannonEnt

def utworzZbiorDanych():
     zbior = [['bialy', 'brak', 'niedzwiedz polarny'],
                ['czarno-bialy', 'brak', 'panda wielka'],
                ['brazowy', 'brak', 'niedzwiedz brunatny'],
                ['czarny', 'duza warga', 'wargacz'],
                ['czarny', 'plama w ksztalcie okularow', 'niedzwiedz andyjski'],
                ['czarny', 'plama w ksztalcie V', 'niedzwiedz himalajski'],
                ['czarny', 'brak','baribal']]
     etykiety = ['kolor','cecha charakterystyczna']
     return zbior, etykiety

def rozdzielenie(zbiorDanych, cecha, wartoscCechy): #trzy dane wejsciowe:zbior danych, cecha, ktora podzielimy i wartosc cechy
    podzielonyZD = [] #tablica/lista
    for element in zbiorDanych: #iteracja po kazdym elemencie w zbiorze danych
        if element[cecha] == wartoscCechy: #az do znalezienia wartosci ktorej szukamy
            zmniejszony = element[:cecha]
            zmniejszony.extend(element[cecha+1:])
            podzielonyZD.append(zmniejszony) #dodanie szukanej wartosci
    return podzielonyZD

def wyborNajlepszejCechy(zbiorDanych): #Wwybiera najlepsza ceche do podzialu
    liczbaCech = len(zbiorDanych[0]) - 1 #liczba cech
    podstawowaEntropia = liczenieEntropii(zbiorDanych) #obliczenie shannon entropii przed podzialem
    najlepszyZyskInformacji = 0.0; najlepszaCecha = -1
    for i in range(liczbaCech): #iteracja po kazdej cesze
        listaCech = [example[i] for example in zbiorDanych] #lista ..?
        unikalneWartosci = set(listaCech) #ustalenie typu danych
        nowaEntropia = 0.0 #nowa entropia po podziale
        for wartosc in unikalneWartosci: #iteracja po kazdej wartosci
            podzbiorDanych = rozdzielenie(zbiorDanych, i, wartosc) #podzial zbioru danych
            prawdopodobienstwo = len(podzbiorDanych)/float(len(zbiorDanych)) #obliczenie prawdopodobienstwa
            nowaEntropia += prawdopodobienstwo * liczenieEntropii(podzbiorDanych) #nowa entropia
        zyskInformacji = podstawowaEntropia - nowaEntropia #obliczenie zysku na informacji
        if (zyskInformacji > najlepszyZyskInformacji):
            najlepszyZyskInformacji = zyskInformacji
            najlepszaCecha = i
    return najlepszaCecha #zwrocenie najlepszej cechy

def wystepowanieKlasy(listaKlas):
    slownikKlas={} #slownik gdzie kluczami beda unikalne wartosci w listaKlas
    for element in listaKlas: #iteracja po elementach listaKlas
        if element not in slownikKlas.keys(): #jezeli element nie jest kluczem
            slownikKlas[element] = 0 #wtedy nadajemy mu wartosc 0
            slownikKlas[element] += 1 #dodanie wartosci
    posortowanaLiczbaKlas = sorted(slownikKlas.iteritems(), key=operator.itemgetter(1), reverse=True)
    return posortowanaLiczbaKlas[0][0] #zwraca klase ktora najczesciej wystepowala

def stworzDrzewo(zbiorDanych,etykiety): #2 wyjscia - zbior danych i etykiety
    listaKlas = [example[-1] for example in zbiorDanych] #lista wszystkich etykiet klas
    if listaKlas.count(listaKlas[0]) == len(listaKlas): #jezeli wszystkie etykiety sa takie same
        return listaKlas[0] #wtedy zwracasz ta etykiete
    if len(zbiorDanych[0]) == 1: #jezeli nie ma juz cech do podzialu
        return wystepowanieKlasy(listaKlas)
    najlepszaCecha = wyborNajlepszejCechy(zbiorDanych)#najlepsza cecha do podzialu
    etykietaNajlepszejCechy = etykiety[najlepszaCecha] #etykieta najleszej cechy
    mojeDrzewo = {etykietaNajlepszejCechy:{}}#slownik ...?
    del(etykiety[najlepszaCecha]) #usuniecie z bazy danych etykiety bestFeat
    wartosciCech = [example[najlepszaCecha] for example in zbiorDanych] #cechy dla wartosci bestfeat
    unikalneWartosci = set(wartosciCech) #unikalne wartosci cechy beatFeat
    for wartosc in unikalneWartosci: #iteracja po unikalnych wartosciach
        kopiaEtykiet = etykiety[:] #kopia listy labels
        mojeDrzewo[etykietaNajlepszejCechy][wartosc] = stworzDrzewo(rozdzielenie\
                (zbiorDanych, najlepszaCecha, wartosc),kopiaEtykiet)#rekurencyjne wywolanie funkcji
    return mojeDrzewo

def klasyfikuj(wejscie,etykiety,test): #klasyfikacja do klas
    pierwszy = wejscie.keys()[0]
    drugi = wejscie[pierwszy]
    indeks = etykiety.index(pierwszy)
    for key in drugi.keys():
        if test[indeks] == key:
            if type(drugi[key]).__name__=='dict':
                nazwaKlasy = klasyfikuj(drugi[key],etykiety,test)
            else:   nazwaKlasy = drugi[key]
    return nazwaKlasy

def zapiszDrzewo(wejscie, nazwaPliku):
    import pickle
    fw = open(nazwaPliku, 'w')
    pickle.dump(wejscie, fw) #zapis do pliku
    fw.close()

def otworzDrzewo(nazwaPliku):
    import pickle
    fr = open(nazwaPliku)
    return pickle.load(fr) #odczyt z pliku

myDat = []
myDat, etykiety = utworzZbiorDanych()
print(myDat)
print(liczenieEntropii(myDat))
print(wyborNajlepszejCechy(myDat))
myTree = stworzDrzewo(myDat, etykiety)
print(myTree)
import treeplotter
print(treeplotter.getNumLeafs(myTree))
print(treeplotter.getTreeDepth(myTree))
treeplotter.createPlot(myTree)