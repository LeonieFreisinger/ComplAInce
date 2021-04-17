from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

import os
import openai
from dotenv import load_dotenv

# backend code
openai.api_key = os.getenv("OPENAI_API_KEY")

## response bodies
response_1 = openai.Completion.create(engine="davinci", prompt="This is a test", max_tokens=5)
print(response_1)

# API code 
app = FastAPI() #app is an instance of teh class FastAPI()

## class definitions
class Contact(BaseModel):
    contact_id:int
    first_name:str
    last_name:str
    user_name:str
    password:str

class ContactOut(BaseModel):
    contact_id:int
    first_name:str
    last_name:str
    user_name:str

## endpoints 
@app.get("/") # decorator 
def home():
    return {"Hello": "FastAPI"}

@app.get("/contactes/{contact_id}")
def contact_details(contact_id: int, page: Optional[int] = 1):
    if page:
        return {'contact_id': contact_id, 'page': page}
    return {'contact_id': contact_id}

@app.post('/contactes')
async def create_contact(contact: Contact): #async converts the simple python function into a coroutine
    return contact

@app.post('/contact', response_model=ContactOut) # using a response model you can control what kind of data should be returned back to the user against a request
async def create_contact(contact: Contact):
    return contact    

# testing
print("test")