import json
import random
import pickle

import numpy as np
import spacy

from tensorflow.keras.models import load_model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.blank('id')


intens = json.loads(open('intest.json').read())

kalimat = pickle.load(open('kata.pkl', 'rb'))
kelas = pickle.load(open('kelas.pkl', 'rb'))
model = load_model('chatbot.model')

def kantong(sentence):
    teks = nlp(sentence)
    kata = [token.text for token in teks]
    bag = [0] * len(kalimat)

    for w in kata:
        for i, word in enumerate(kalimat):
            if word == w:
                bag[i] = 1

    return np.array(bag)


def prediksi(sentence):
    kantong_kata = kantong(sentence)
    res = model.predict(np.array([kantong_kata]))[0]
    ERROR_THRES = 0.50
    hasil = [[i,r] for i,r in enumerate(res) if r > ERROR_THRES]

    hasil.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in hasil:
        return_list.append({"intent" : kelas[r[0]], "probability" : str(r[1])})

    return return_list

def Similiarity_selector(list, sentence):
    user_inp = sentence
    kata = nlp(user_inp)
    token = [token.text for token in kata]
    list.extend(token)
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
    if respon_flag == 0:
        reply = "IDK LOL"

    list = [x for x in list if x not in token]
    return reply

def response(sentence):
    # tag = intents_list[0]['intent']
    tag = prediksi(sentence)[0]['intent']
    list_intent = intens['intents']
    for i in list_intent:
        if i['tag'] == tag:
            hasil = Similiarity_selector(i['responses'], sentence)
            break

    return hasil

# print("BOT IS RUN")
#
# start = True
# while start:
#     pesan = input("COBA :")
#     if pesan == "stop":
#         start = False
#     else:
#         res = response(pesan)
#         print(res)