from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

import os
import openai
from dotenv import load_dotenv

#---------------------------------------------------------------------------------------------------
# backend code
openai.api_key = os.getenv("OPENAI_API_KEY")

## input for GPT3 
start_sequence = "\nA:" # our answer start with ... 
restart_sequence = "\n\nQ: " # each question starts with ...
session_prompt ="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: What is the name of the president of Germany?\nA: It is Joachim Gauck."

## response bodies

### test case completion
# response_1 = openai.Completion.create(
#   engine="davinci",
#   prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer.\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: What is the name of the president of Germany?\nA:",
#   temperature=0.1,
#   max_tokens=150,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0.6,
#   stop=["\n"]
# )
# #print("response_1", response_1)
# teststory_1 = response_1['choices'][0]['text']
# print(" teststory_1: ", teststory_1)

### test case easy Q&A
# response_2 = openai.Completion.create(
#   engine="davinci",
#   prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nQ: Hello, who are you?\nA: I am an AI created by OpenAI. How can I help you today?\nQ: What are you looking for?\nA:",
#   temperature=0.9,
#   max_tokens=150,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0.6,
#   stop=["\n", " Q:", " A:"]
# )
# #print("response_2: ", response_2)
# teststory_2 = response_2['choices'][0]['text']
# print(" teststory_2: ", teststory_2)

## functions
def ask(question, chat_log=None):
    """
    this function ask a question to the gpt3 enigne
    input: 
    question - str
    chat_log - str

    output:
    story - str

    """
    prompt_text = f'{chat_log}{restart_sequence}{question}{start_sequence}'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"]
    )
    story = response['choices'][0]['text']
    return str(story)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    """
    this function concatinates the new question and answer to the chatlog
    input: 
    question - str
    answer - str
    chat_log - str

    output:
    response - str

    """
    if chat_log is None: 
        chat_log = session_prompt 
    new_chat_log = f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
    return new_chat_log

## execution
chat_log = session_prompt
question_1 = "Who are you?"
print("question_1: ",question_1)
answer_1 = ask (question_1, chat_log)
print("answer1: ",answer_1)
chat_log = append_interaction_to_chat_log(question_1, answer_1, chat_log)
#print(chat_log)
question_2 = "What is your daily routine?"
print("question_2: ",question_2)
answer_2 = ask (question_2, chat_log)
print("answer2: ",answer_2)
chat_log = append_interaction_to_chat_log(question_2, answer_2, chat_log)
#print(chat_log)


#-----------------------------------------------------------------------------------------------------
# API code 
app = FastAPI() #app is an instance of teh class FastAPI()

## class definitions
class Query(BaseModel):
    question:str
    answer_out: Optional[str] = None
    

class ContactOut(BaseModel):
    contact_id:int
    first_name:str
    last_name:str
    user_name:str

## endpoints 
@app.post('/send_question')
async def send_question(query: Query):
    answer_api = ask(query.question, chat_log)
    query.answer_out = {"answer": answer_api}
    return query.answer_out 

### further
# @app.get("/") # decorator 
# def home():
#     return {"Hello": "FastAPI"}

# @app.get("/contactes/{contact_id}")
# def contact_details(contact_id: int, page: Optional[int] = 1):
#     if page:
#         return {'contact_id': contact_id, 'page': page}
#     return {'contact_id': contact_id}

# @app.post('/contactes')
# async def create_contact(contact: Contact): #async converts the simple python function into a coroutine
#     return contact

# @app.post('/contact', response_model=ContactOut) # using a response model you can control what kind of data should be returned back to the user against a request
# async def create_contact(contact: Contact):
#     return contact    

#-----------------------------------------------------------------------------------------------------------------------
# testing
#print("test")