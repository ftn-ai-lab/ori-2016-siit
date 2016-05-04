"""
    @author:    SW 15/2013   Dragutin Marjanovic
    @email:     dmarjanovic94@gmail.com
"""

from __future__ import print_function

import re, csv, string, math
# Ubacena biblioteka za stemizaciju rijeci
from stemming.porter2 import stem

# Ucitajemo 150 stop rijeci iz fajla 'english_stopwords.txt'
english_stopwords = []

def load_data():
    # TODO 1: ucitati podatke iz data/train.tsv datoteke
    # rezultat treba da budu dve liste, texts i sentiments
    texts, sentiments = [], []
    
    with open('../../data/train.tsv','rb') as input_file:
        input_file = csv.reader(input_file, delimiter='\t')
        # Skip header
        next(input_file)
        for row in input_file:
            sentiments.append(row[0])
            texts.append(row[1])

    stop_words_file = open('english_stopwords.txt', 'r')
    for stop_word in stop_words_file.readlines():
        english_stopwords.append(stop_word[:-1])

    return texts, sentiments


def preprocess(text):
    # TODO 2: implementirano preprocesiranje teksta
    # - izbacivanje znakova interpunkcije
    # - svodjenje celog teksta na mala slova
    # rezultat treba da bude preprocesiran tekst
    text = text.lower()
    text = re.sub('[^a-zA-Z]+', ' ', text).strip()
    return text
        

def tokenize(text, stemming = False):
    text = preprocess(text)
    # TODO 3: implementirana tokenizacija teksta na reci
    # rezultat treba da bude lista reci koje se nalaze u datom tekstu
    words = text.split(' ')
    
    # Vrsimo stemizaciju rijeci
    if stemming:
        filtered_words = []
        for word in words:
            # Izbacujemo engleske stop rijeci
            if word not in english_stopwords:
                filtered_words.append(stem(word))
                
        return filtered_words

    return words


def count_words(text):
    # Ako smo vec proslijedili listu, nije potrebna tokenizacija
    if isinstance(text, list):
        words = text
    else:
        words = tokenize(text, stemming=True)
        
    # TODO 4: implementirano prebrojavanje reci u datom tekstu
    # rezultat treba da bude mapa, ciji kljucevi su reci, a vrednosti broj ponavljanja te reci u datoj recenici
    words_count = {}
    for word in words:
        if words_count.has_key(word):
            words_count[word] += 1
        else:
            words_count[word] = 1
            
    return words_count


def fit(texts, sentiments):
    # inicijalizacija struktura
    bag_of_words = {}               # bag-of-words za sve recenzije
    words_count = {'pos': {},       # isto bag-of-words, ali posebno za pozivitne i negativne recenzije
                   'neg': {}}
    texts_count = {'pos': 0.0,      # broj tekstova za pozivitne i negativne recenzije
                   'neg': 0.0}

    # TODO 5: proci kroz sve recenzije i sentimente i napuniti gore inicijalizovane strukture
    # bag-of-words je mapa svih reci i broja njihovih ponavljanja u celom korpusu recenzija
    
    for text, sentiment in zip(texts, sentiments):
        text_dict = count_words(text)
        
        for word, count in text_dict.iteritems():
            # Iteriramo kroz svaku rijec za dati tekst i dodajemo u listu svih rijeci
            if bag_of_words.has_key(word):
                bag_of_words[word] += count
            else:
                bag_of_words[word] = count
            
            # Dodajemo rijec u odgovarajuci rjecnik - pozitivnih ili negativnih recenzija    
            if words_count[sentiment].has_key(word):
                words_count[sentiment][word] += count
            else:
                words_count[sentiment][word] = count
        
        # Uvecamo broj pozitivnih ili negativnih recenzija
        texts_count[sentiment] += 1
    
    return bag_of_words, words_count, texts_count


def predict(text, bag_of_words, words_count, texts_count):
    words = tokenize(text, stemming=True)  # tokenizacija teksta
    counts = count_words(words)            # prebrojavanje reci u tekstu
 
    # TODO 6: implementiran Naivni Bayes klasifikator za sentiment teksta (recenzije)
    # rezultat treba da bude mapa verovatnoca da je dati tekst klasifikovan kao pozitivnu i negativna recenzija
    score_pos, score_neg = 0.0, 0.0

    # Broj svih rijeci
    sum_all_words = float(sum(bag_of_words.values()))
    
    # Broj rijeci za svaki sentiment (pos, neg) 
    sum_words = {}       
    for sentiment in words_count.keys():
        sum_words[sentiment] = float(sum(words_count[sentiment].values()))
    
    # Broj rijeci u svim sentimentima (pos, neg)
    sum_all_sentiments = float(sum(texts_count.values()))   
    
    # Vjerovatnoca da se rijec pojavljuje u svakom od sentimenata
    p_sentiments = {}
    for sentiment in texts_count.keys():
        p_sentiments[sentiment] = texts_count[sentiment] / sum_all_sentiments

    sum_sentiments = {'pos': 0.0,
                      'neg': 0.0}
   
    for word in words:
        if bag_of_words.has_key(word):
            # Vjerovatnoca da se rijec pojavljuje
            word_probability = bag_of_words[word] / sum_all_words
        
        for sentiment in sum_sentiments.keys():
            if words_count[sentiment].has_key(word) and words_count[sentiment][word] > 0:
                pp_word = words_count[sentiment][word] / sum_words[sentiment]
                sum_sentiments[sentiment] += math.log(pp_word/word_probability)    
       
    score_pos = math.exp(sum_sentiments['pos'] + math.log(p_sentiments['pos']))
    score_neg = math.exp(sum_sentiments['neg'] + math.log(p_sentiments['neg']))
 
    return {'pos': score_pos, 'neg': score_neg}

if __name__ == '__main__':
    # ucitavanje data seta
    texts, sentiments = load_data()

    # izracunavanje / prebrojavanje stvari potrebnih za primenu Naivnog Bayesa
    bag_of_words, words_count, texts_count = fit(texts, sentiments)

    # recenzija
    text = 'My favourite movie is Batman: The Dark Knight. I really like this movie. But I like Baco even more. :)'

    # klasifikovati sentiment recenzije koriscenjem Naivnog Bayes klasifikatora
    predictions = predict(text, bag_of_words, words_count, texts_count)
    
    print('-'*30)
    print('Review: {0}'.format(text))
    print('Score(pos): {0}'.format(predictions['pos']))
    print('Score(neg): {0}'.format(predictions['neg']))

    index = true_predicts = 0   
    for text in texts:
        predictions = predict(text, bag_of_words, words_count, texts_count)
        # print(predictions2)
        if predictions['pos'] > predictions['neg'] and sentiments[index] == 'pos':
            true_predicts += 1
        
        if predictions['neg'] > predictions['pos'] and sentiments[index] == 'neg':
            true_predicts += 1
        index += 1

    print ('True predicts:  {0}'.format(true_predicts))
    print ('Data set count: {0}'.format(len(sentiments)))