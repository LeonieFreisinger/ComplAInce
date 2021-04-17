from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from gpt3 import GPT3

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
class Query(BaseModel):
    question: str

@app.post('/send-question')
async def send_question(query: Query):
    answer = gpt3.get_answer(query.question)
    return {
        "answer": answer
    }