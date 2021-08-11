import json
import random
import pickle

import numpy as np
import spacy

from tensorflow.keras.models import load_model


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
    ERROR_THRES = 0.25
    hasil = [[i,r] for i,r in enumerate(res) if r > ERROR_THRES]

    hasil.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in hasil:
        return_list.append({"intent" : kelas[r[0]], "probability" : str(r[1])})

    return return_list

def response(sentence):
    # tag = intents_list[0]['intent']
    tag = prediksi(sentence)[0]['intent']
    list_intent = intens['intents']
    for i in list_intent:
        if i['tag'] == tag:
            hasil = random.choice(i['responses'])
            break

    return hasil

print("BOT IS RUN")

start = True
while start:
    pesan = input("COBA :")
    if pesan == "stop":
        start = False
    else:
        res = response(pesan)
        # ints = prediksi(pesan)
        # res = response(ints, intens)
        print(res)