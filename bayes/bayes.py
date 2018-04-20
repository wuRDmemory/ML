import os, macpath
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]
    return postingList, classVec

def get_word(data_list):
    words = set()
    for data in data_list:
        for word in data:
            words.add(word)
    return list(words)

def get_train_data(words, sentence):
    data_vec = [0]*len(words)
    for data in sentence:
        # for word in words:
        if data in words:
            data_vec[words.index(data)] = 1
    return data_vec  

def get_condition_percentile(word, sentences, classes):
    p_perc = 0
    n_perc = 0
    i = 0
    for sentence in sentences:
        if word in sentence:
            if classes[i]==0:
                p_perc += 1
            else:
                n_perc += 1 
        i+=1
    return float(p_perc+1)/(len(classes)+2), float(n_perc+1)/(len(classes)+2)

def classify_sentence(sentence, words, words_positive_perc, words_nagetive_perc):
    vec = get_train_data(words, sentence)
    np_vec = np.array(vec)
    np_words_positive_perc = np.array(words_positive_perc)
    np_words_nagetive_perc = np.array(words_nagetive_perc)
    np_p_perc = np_words_positive_perc[np_vec==1]
    np_n_perc = np_words_nagetive_perc[np_vec==1]
    p_perc = reduce(lambda x,y: x*y, np_p_perc)*0.5
    n_perc = reduce(lambda x,y: x*y, np_n_perc)*0.5
    return p_perc, n_perc
    

if __name__=='__main__':
    postingList, classVec = load_data()
    words = get_word(postingList)
    # statistic
    word_positive_perc = list()
    word_nagetive_perc = list()
    for word in words:
        p_perc, n_perc = get_condition_percentile(word, postingList, classVec)
        word_positive_perc.append(p_perc)
        word_nagetive_perc.append(n_perc)
        print "word:%s\tp_perc:%.2f\tn_perc:%.2f" % (word, p_perc, n_perc)

    # classify
    sen1 = ['stupid', 'dog', 'my']
    sen2 = ['help', 'problem']
    p,n = classify_sentence(sen1, words, word_positive_perc, word_nagetive_perc)
    print p, n
    p,n = classify_sentence(sen2, words, word_positive_perc, word_nagetive_perc)
    print p, n