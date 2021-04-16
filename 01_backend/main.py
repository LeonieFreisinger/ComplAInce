from fastapi import FastAPI
from pydantic import BaseModel

from .config import SESSION_PROMPT
from gpt3 import GPT3

app = FastAPI() #app is an instance of teh class FastAPI()
gpt3 = GPT3()
class Query(BaseModel):
    question: str

@app.post('/send-question')
async def send_question(query: Query):
    return gpt3.get_answer(query.question)
    # answer_api = gpt3.ask(query.question, SESSION_PROMPT)