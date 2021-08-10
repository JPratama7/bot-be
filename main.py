from fastapi import FastAPI
from pydantic import BaseModel

#create app
app = FastAPI()

class Chat(BaseModel):
    nomor : int
    body : str

def log(nomor, pesan):
    with open('log', 'a') as file:
        text = f"Dari {nomor}\nPesan {pesan}\n"
        file.write(text)
        file.close()

@app.get("/")
async def get():
    return {
        "code" : 200,
        "body" : "THIS IS HELLO WORLD"
    }

@app.post("/chatbot")
async def post(Whatsapp: Chat):
    kalimat = ["main", "mabar", "ayo"]
    if Whatsapp.body.lower() in kalimat:
        body = "okeh ayoklah lobby"
    else:
        body = ""

    return {
        "nomor" : Whatsapp.nomor,
        "body" : body
    }
