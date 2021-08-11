import json
import random
import pickle

import numpy as np
import spacy

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

nlp = spacy.blank('id')

factory = StemmerFactory()
stemmer = factory.create_stemmer()
intens = json.loads(open('intest.json').read())

kalimat =[]
kelas = []
dokumen = []
karakter_ilegal = ["?", ".", ",", "!"]

for intens in intens['intents']:
    for pattern in intens['patterns']:
        stem = stemmer.stem(pattern)
        teks = nlp(stem)
        wordlist = [token.text for token in teks]
        kalimat.extend(wordlist)
        dokumen.append((wordlist, intens['tag']))
        if intens['tag'] not in kelas:
            kelas.append(intens['tag'])

kata = sorted(set(kalimat))

pickle.dump(kalimat, open('kata.pkl', 'wb'))
pickle.dump(kelas, open('kelas.pkl', 'wb'))

training = []
out_kosong = [0] * len(kelas)

for data in dokumen:
    bag = []
    pola_kalimat = data[0]
    for kata in kalimat:
        bag.append(1) if kata in pola_kalimat else bag.append(0)

    out_row = list(out_kosong)
    out_row[kelas.index(data[1])] = 1
    training.append([bag,out_row])

random.shuffle(training)

training = np.array(training)


train_x = list(training[:,0])
train_y = list(training[:,1])


model = Sequential()

model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=5, verbose=1)
model.save('chatbot.model')

print("done")
