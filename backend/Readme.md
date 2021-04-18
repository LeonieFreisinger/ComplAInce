# Project: Chatbot

## Quickstart
1. Activate pipenv shell `pipenv shell`
2. Install all dependencies `pipenv install`
3. If initial start run `python -m gpt3` to upload files to openai
4. Run `uvicorn main:app --reload`

## Structure
1. general
2. backend code
3. API code
4. versions

## general
- pipenv envrionment is used 
- open AI key is imported via env. using dotenv

### useful links
whole setup: https://chatbotslife.com/deploying-transformer-models-1350876016f
tutorial heruko: https://davedodea.medium.com/how-to-deploy-a-python-app-to-heroku-12289912f29c
tutorial fastAPI: https://towardsdatascience.com/create-your-first-rest-api-in-fastapi-e728ae649a60
pipenv commands: https://realpython.com/pipenv-guide/

## backend code
### pipeline
    create post enpoint: request-body: has the question; respond-body: has the answer
    create a function with post request enpoint to GPT3: request-body is the whole input info; response-body: is the answer 
    placeholder for text input
### usage
- change the session_prompt if needed
- change the start_sequence if needed 
- change the restart_sequence if needed 
- change the parameters of the request if neede
- run $uvicorn main:app --reload$ to invoke the Uvicorn server (= make endpoint alive); options: uvicorn --port 5000 --host 127.0.0.1 main:app --reload

### functions
    aks
    append_interaction_to_chat_log


## api definitions

##versions
- main_01: only GPT3 running
- main_02   first version, where GPT3 and FastAPI is working
