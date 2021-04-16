# Project: Chatbot 

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

## backend code
### pipeline
    create post enpoint: request-body: has the question; respond-body: has the answer
    create a function with post request enpoint to GPT3: request-body is the whole input info; response-body: is the answer 
    placeholder for text input
### usage
- change the session_prompt if needed
- chnage the start_sequence if needed 
- chnage the restart_sequence if needed 
- change the parameters of the request if neede

### functions
    aks
    append_interaction_to_chat_log


## api definitions

##versions
- main_01: only GPT3 running
- main_02   first version, where GPT3 and FastAPI is working
