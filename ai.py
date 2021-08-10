import json
import random
import pickle

import numpy as np
import spacy

from tensorflow.keras.models import load_model

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

nlp = spacy.blank('id')

factory = StemmerFactory()
stemmer = factory.create_stemmer()
intens = json.loads(open('intest.json').read())

kalimat = pickle.load(open('kata.pkl', 'rb'))
kelas = pickle.load(open('kelas.pkl', 'rb'))
model = load_model('model')

def pembersih(sentence):
    teks = nlp(sentence)
    wordlist = [token.text for token in teks]
    return wordlist

def kantong(sentence):
    kata = pembersih(sentence)
    bag = [0] * len(kalimat)

    for w in kata:
        for i, word in enumerate(kalimat):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def prediksi(sentence):
    kantong_kata = kantong(sentence)
    print(kantong_kata)
    res = model.predict(np.array([kantong_kata]))[0]
    ERROR_THRES = 0.25
    hasil = [[i,r] for i,r in enumerate(res) if r > ERROR_THRES]
    print(hasil)

    hasil.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in hasil:
        return_list.append({"intent" : kelas[r[0]], "probability" : str(r[1])})

    return return_list

def response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    print(tag)
    list_intent = intents_json['intents']
    print(list_intent)
    for i in list_intent:
        if i['tag'] == tag:
            hasil = random.choice(i['responses'])
            break

    return hasil

print("BOT IS RUN")

while True:
    pesan = input("COBA :")
    ints = prediksi(pesan)
    res = response(ints, intens)
    print(res)
