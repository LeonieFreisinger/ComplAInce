from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from gpt3 import GPT3
from models import Query

app = FastAPI() #app is an instance of teh class FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gpt3 = GPT3()

@app.post('/send-question')
async def send_question(query: Query):
    logging.info('Received query!')
    query.chatContent.pop(0)
    out = gpt3.get_answer(query.chatContent)
    return { "data": out }
    # return {
    #     "answer": answer
    # }