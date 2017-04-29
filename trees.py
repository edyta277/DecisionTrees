import operator
from math import log
# from pickletools import I


def liczenieEntropii(dataSet):
    liczbaInstancji = len(dataSet) #liczba instancji w zbiorze danych
    liczbaEtykiet = {} #slownik (tablica indeksowana kluczami) -kluczami beda wartosci  ostatniej kolumny
    for element in dataSet: #dla kazdej cechy w zbiorze danych
        aktualnaEtykieta = element[-1] #aktualna etykieta =...?
        if aktualnaEtykieta not in liczbaEtykiet.keys(): #jezeli currentLabel nie jest juz kluczem w LabelCounts (klucze nie moga sie powtarzac)
            liczbaEtykiet[aktualnaEtykieta] = 0 #wtedy liczba wynosi 0
        liczbaEtykiet[aktualnaEtykieta] += 1 #dodanie jednego
    entropia = 0.0 #przypisanie wartosci 0.0
    for key in liczbaEtykiet: #dla kazdego klucza
        prawdopodobienstwo = float(liczbaEtykiet[key])/liczbaInstancji #prawdopodobienstwo=liczbawystapien etykiety/liczba instancji
        entropia -= prawdopodobienstwo * log(prawdopodobienstwo, 2) #odjęcie wartosci
    return entropia #zwrocenie shannonEnt

#def createDataSet(): #stworzenie bazy danych
#    dataSet = [[1, 0, 0, 0, 0, 0, 'niedzwiedz polarny'],
#               [0, 1, 0, 0, 0, 0, 'panda wielka'],
#               [0, 0, 0, 0, 0, 0, 'niedzwiedz brunatny'],
#               [0, 0, 1, 1, 0, 0, 'wargacz'],
#               [0, 0, 1, 0, 1, 0,  'niedzwiedz andyjski'],
#               [0, 0, 1, 0, 0, 1, 'niedzwiedz himalajski'],
#               [0, 0, 1, 0, 0, 0, 'baribal']]
#    labels = ['bialy', 'czarno-bialy', 'czarny', 'duza warga', 'plama w ksztalcie okularow', 'plama w ksztalcie V']
#    return dataSet, labels

# def createDataSet():
#     dataSet = [[1, 0, 0, 0, 0, 0, 'niedzwiedz polarny'],
#                [1, 0, 0, 0, 0, 0, 'niedzwiedz polarny'],
#                [1, 0, 0, 0, 0, 0, 'niedzwiedz polarny'],
#                [0, 1, 0, 0, 0, 0, 'panda wielka'],
#                [0, 1, 0, 0, 0, 0, 'panda wielka'],
#                [0, 0, 0, 0, 0, 0, 'niedzwiedz brunatny'],
#                [0, 0, 0, 0, 0, 0, 'niedzwiedz brunatny'],
#                [0, 0, 0, 0, 0, 0, 'niedzwiedz brunatny'],
#                [0, 0, 1, 1, 0, 0, 'wargacz'],
#                [0, 0, 1, 1, 0, 0, 'wargacz'],
#                [0, 0, 1, 1, 0, 0, 'wargacz'],
#                [0, 0, 1, 0, 1, 0, 'niedzwiedz andyjski'],
#                [0, 0, 1, 0, 1, 0, 'niedzwiedz andyjski'],
#                [0, 0, 1, 0, 0, 1, 'niedzwiedz himalajski'],
#                [0, 0, 1, 0, 0, 1, 'niedzwiedz himalajski'],
#                [1, 0, 1, 0, 0, 0, 'baribal'],
#                [1, 0, 1, 0, 0, 0, 'baribal'],
#                [1, 0, 1, 0, 0, 0, 'baribal']]
#     labels = ['bialy', 'czarno-bialy', 'czarny', 'duza warga', 'plama w ksztalcie okularow', 'plama w ksztalcie V']
#     return dataSet, labels

def createDataSet():
     dataSet = [['bialy', 'brak', 'niedzwiedz polarny'],
                ['czarno-bialy', 'brak', 'panda wielka'],
                ['brazowy', 'brak', 'niedzwiedz brunatny'],
                ['czarny', 'duza warga', 'wargacz'],
                ['czarny', 'plama w ksztalcie okularow', 'niedzwiedz andyjski'],
                ['czarny', 'plama w ksztalcie V', 'niedzwiedz himalajski'],
                ['czarny', 'brak','baribal']]
     etykiety = ['kolor','cecha charakterystyczna']
     return dataSet, etykiety

def rozdzielenie(dataSet, cecha, wartoscCechy): #trzy dane wejsciowe:zbior danych, cecha, ktora podzielimy i wartosc cechy
    podzielonyZD = [] #tablica/lista
    for element in dataSet: #iteracja po kazdym elemencie w zbiorze danych
        if element[cecha] == wartoscCechy: #az do znalezenia wartosci ktorej szukamy
            reducedFeatVec = element[:cecha]
            reducedFeatVec.extend(element[cecha+1:])
            podzielonyZD.append(reducedFeatVec) #dodanie szukanej wartosci
    return podzielonyZD

def wyborNajlepszejCechy(dataSet): #Wwybiera najlepsza ceche do podzialu
    liczbaCech = len(dataSet[0]) - 1 #liczba cech
    podstawowaEntropia = liczenieEntropii(dataSet) #obliczenie shannon entropii przed podzialem
    najlepszyZyskInformacji = 0.0; najlepszaCecha = -1
    for i in range(liczbaCech): #iteracja po kazdej cesze
        featList = [example[i] for example in dataSet] #lista ..?
        unikalneWartosci = set(featList) #ustalenie typu danych
        nowaEntropia = 0.0 #nowa entropia po podziale
        for wartosc in unikalneWartosci: #iteracja po kazdej wartosci
            subDataSet = rozdzielenie(dataSet, i, wartosc) #podzial zbioru danych
            prawdopodobienstwo = len(subDataSet)/float(len(dataSet)) #obliczenie prawdopodobienstwa
            nowaEntropia += prawdopodobienstwo * liczenieEntropii(subDataSet) #nowa entropia
        zyskInformacji = podstawowaEntropia - nowaEntropia #obliczenie zysku na informacji
        if (zyskInformacji > najlepszyZyskInformacji):
            najlepszyZyskInformacji = zyskInformacji
            najlepszaCecha = i
    return najlepszaCecha #zwrocenie najlepszej cechy

def wystepowanieKlasy(listaKlas):
    liczbaKlas={} #slownik gdzie kluczami beda unikalne wartosci w classList
    for element in listaKlas: #iteracja po elementach classList
        if element not in liczbaKlas.keys(): #jezeli element nie jest kluczme
            liczbaKlas[element] = 0 #wtedy nadajemy mu wartosc 0
        liczbaKlas[element] += 1 #dodanie wartosci
    posortowanaLiczbaKlas = sorted(liczbaKlas.iteritems(), key=operator.itemgetter(1), reverse=True)
    return posortowanaLiczbaKlas[0][0] #zwraca klase ktora najczesciej wystepowala

def stworzDrzewo(dataSet,etykiety): #2 wyjscia - zbior danych i etykiety
    listaKlas = [example[-1] for example in dataSet] #lista wszystkich etykiet klas
    if listaKlas.count(listaKlas[0]) == len(listaKlas): #jezeli wszystkie etykiety sa takie same
        return listaKlas[0] #wtedy zwracasz ta etykiete
    if len(dataSet[0]) == 1: #jezeli nie ma juz cech do podzialu
        return wystepowanieKlasy(listaKlas)
    najlepszaCecha = wyborNajlepszejCechy(dataSet)#najlepsza cecha do podzialu
    etykietaNajlepszejCechy = etykiety[najlepszaCecha] #etykieta najleszej cechy
    mojeDrzewo = {etykietaNajlepszejCechy:{}}#slownik ...?
    del(etykiety[najlepszaCecha]) #usuniecie z bazy danych etykiety bestFeat
    wartosciCech = [example[najlepszaCecha] for example in dataSet] #cechy dla wartosci bestfeat
    unikalneWartosci = set(wartosciCech) #unikalne wartosci cechy beatFeat
    for wartosc in unikalneWartosci: #iteracja po unikalnych wartosciach
        kopiaEtykiet = etykiety[:] #kopia listy labels
        mojeDrzewo[etykietaNajlepszejCechy][wartosc] = stworzDrzewo(rozdzielenie\
                (dataSet, najlepszaCecha, wartosc),kopiaEtykiet)#rekurencyjne wywolanie funkcji
    return mojeDrzewo

def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__=='dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else:   classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

myDat = []
myDat, etykiety = createDataSet()
print(myDat)
print(liczenieEntropii(myDat))
print(wyborNajlepszejCechy(myDat))
myTree = stworzDrzewo(myDat, etykiety)
print(myTree)
import treeplotter
# print(treeplotter.retrieveTree(1))
print(treeplotter.getNumLeafs(myTree))
print(treeplotter.getTreeDepth(myTree))
treeplotter.createPlot(myTree)