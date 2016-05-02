"""
    @author:    SW 15/2013   Dragutin Marjanovic
    @email:     dmarjanovic94@gmail.com
"""

"""
    Preuzeti '20news-bydate.tar.gz' podatke sa sajta 'http://qwone.com/~jason/20Newsgroups/'.
    Smjestiti ih u folder bonus u folder '20news-bydate-test' koji se koristi za testiranje i
    '20news-bydate-train' kojim obucavamo Naive Bayes-a. 
    
    Kategorije clanaka odgovaraju pojedinacnom direktorijumu u folderu. 
    
    Preciznost je 5869 tacnih od 7453 artikala u testnom skupu. ~78.7%
"""

from __future__ import print_function

import re, csv, string, math, os
# Ubacena biblioteka za stemizaciju rijeci
from stemming.porter2 import stem

# Ucitajemo 150 stop rijeci iz fajla 'english_stopwords.txt'
english_stopwords = []

def process_article(article):
    processed_article = ''
    
    for line in article.split('\n'):
        # Simple header remove (if startswith 'SomeText:'')
        if not re.match("[a-zA-Z]+:", line):
            process_article += line
            
    return processed_article
    
    
def load_data():
    # TODO 1: ucitati podatke iz data/train.tsv datoteke
    # rezultat treba da budu dve liste, texts i sentiments
    texts, sentiments = [], []

    for directory in os.listdir('20news-bydate-train'):
        for article in os.listdir(os.path.join('20news-bydate-train', directory)):
            sentiments.append(directory)
            article_file = open('20news-bydate-train/' + directory + '/' + article, 'r')
            article_text = ''.join(article_file.readlines())
            texts.append(article_text)
            article_file.close()
            
    stop_words_file = open('../solutions/english_stopwords.txt', 'r')
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
    words_count = {}
    texts_count = {}
    for item in set(sentiments):
        words_count[item] = {}      # isto bag-of-words, ali posebno za pozivitne i negativne recenzije
        texts_count[item] = 0.0     # broj tekstova za pozivitne i negativne recenzije

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
    sum_sentiments = {}
    for sentiment in texts_count.keys():
        p_sentiments[sentiment] = texts_count[sentiment] / sum_all_sentiments
        sum_sentiments[sentiment] = 0.0
   
    for word in words:
        if bag_of_words.has_key(word):
            # Vjerovatnoca da se rijec pojavljuje
            word_probability = bag_of_words[word] / sum_all_words
        
        for sentiment in sum_sentiments.keys():
            if words_count[sentiment].has_key(word) and words_count[sentiment][word] > 0:
                pp_word = words_count[sentiment][word] / sum_words[sentiment]
                sum_sentiments[sentiment] += math.log(pp_word/word_probability)    
     
    ret_val = {}
    for sentiment in texts_count.keys():  
        ret_val[sentiment] = math.exp(sum_sentiments[sentiment] + math.log(p_sentiments[sentiment]))
 
    return ret_val

if __name__ == '__main__':
    # ucitavanje data seta
    texts, sentiments = load_data()

    # izracunavanje / prebrojavanje stvari potrebnih za primenu Naivnog Bayesa
    bag_of_words, words_count, texts_count = fit(texts, sentiments)

    # recenzija
    text = 'In machine learning and cognitive science, artificial neural networks (ANNs) are a family of models inspired by biological neural networks (the central nervous systems of animals, in particular the brain) which are used to estimate or approximate functions that can depend on a large number of inputs and are generally unknown. Artificial neural networks are generally presented as systems of interconnected "neurons" which exchange messages between each other. The connections have numeric weights that can be tuned based on experience, making neural nets adaptive to inputs and capable of learning.'

    # klasifikovati sentiment recenzije koriscenjem Naivnog Bayes klasifikatora
    predictions = predict(text, bag_of_words, words_count, texts_count)
    
    print('-'*30)
    print('Article: {0}'.format(text))
    # for i in set(sentiments):
    #     print('Score({0}): {1}'.format(i, predictions[i]))
        
    v = list(predictions.values())
    k = list(predictions.keys())
    print ('   Value: ' + str(max(v)))
    print ('Category: ' + k[v.index(max(v))])

    total_texts   = 0
    true_predicts = 0
    for directory in os.listdir('20news-bydate-test'):
        for article in os.listdir(os.path.join('20news-bydate-test', directory)):
            article_file = open('20news-bydate-test/' + directory + '/' + article, 'r')
            article_text = ''.join(article_file.readlines())
            article_file.close()
            
            try:
                predictions = predict(article_text, bag_of_words, words_count, texts_count)
                
                v = list(predictions.values())
                k = list(predictions.keys())
                if k[v.index(max(v))] == directory:
                    true_predicts += 1
                total_texts += 1
            except:
                print ('Math range error...')
            
    print ('Total test texts: ' + str(total_texts))
    print ('   True predicts: ' + str(true_predicts))