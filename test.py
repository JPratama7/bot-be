import json
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from newspaper import Article

import spacy

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

artikel = Article('https://id.wikipedia.org/wiki/Penyakit_koronavirus_2019')
artikel.download()
artikel.parse()
artikel.nlp()

spacy = spacy.blank('id')

stemed = stemmer.stem(artikel.text)
list_word = nltk.sent_tokenize(artikel.text)

# def index_sort(list):
#   lenght = len(list)
#   list_index=list[range(0,lenght)]
#
#   x = list
#   for i in range(lenght):
#       print(i)
#       for j in range(lenght):
#           print(j)
#           # if x[list_index[i]] > x[list_index[j]]:
#           #     list_index[i], list_index[j] = list_index[j], list_index[i]
#   # for i in range(leng):
#   #   for j in range(leng):
#   #     if x[list_index[i]] > x[list_index[j]]:
#   #       list_index[i], list_index[j] = list_index[j], list_index[i]
#
#   return list_index


# user_inp = 'wokeh'
# list_word.append(user_inp)
# bot_res = ''
# cv = CountVectorizer().fit_transform(list_word)
# similiar_score = cosine_similarity(cv[-1], cv)
# similiar_score_list = similiar_score.flatten()
# index = sorted(similiar_score_list, reverse=True)
# print(index)


def bot_res(list,input):
    user_inp = input.lower()
    kata = spacy(user_inp)
    token = [token.text for token in kata]
    print(token)
    list.extend(token)
    print(list_word)
    cv = CountVectorizer().fit_transform(list)
    similiar_score = cosine_similarity(cv[-1], cv)
    similiar_score_list = similiar_score.flatten()
    index = sorted(similiar_score_list, reverse=True)
    index = index[1:]
    respon_flag = 0

    reply = ''

    j = 0

    for i in range(len(index)):
        if similiar_score_list[i] > 0.0:
            reply = reply + ' ' + list[i]
            respon_flag = 1
            j = j+1
        if j > 2:
            break
    if respon_flag == 0:
        reply = "IDK LOL"
    list = [x for x in list if x not in token]

    return reply

while True:
    data = input("SAY SOMETHING : ")
    print("bot response  is : " + bot_res(data))
    print(list_word)