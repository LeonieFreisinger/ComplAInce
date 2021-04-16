# How to build a fastAPI in Python 

tutorial: https://towardsdatascience.com/create-your-first-rest-api-in-fastapi-e728ae649a60

# dependencies
refers to the file main_fastapi.py
refers to Pipefile

## setting up development envrionments
use Pipenv
1. install Pipenv $pip install pipenv
2. create envrioment $pipenv install --python 3.9 (optional: $pipenv install --three$ where three means Python 3.x.)
3. activate envrionment $pipenv shell

## creating the endpoint
1. create a main.py file
2. write the basic code 
    import FASTApi
    instantiate: app = FASTApi()
3. create a route via decorater
    what is a decorator: https://www.datacamp.com/community/tutorials/decorators-python?utm_source=adwords_ppc&utm_campaignid=898687156&utm_adgroupid=48947256715&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=&utm_creative=229765585183&utm_targetid=aud-392016246653:dsa-429603003980&utm_loc_interest_ms=&utm_loc_physical_ms=1004054&gclid=Cj0KCQjwpdqDBhCSARIsAEUJ0hP0kONp2-NpOY1cTs2gKwWiKS55P-W10bx5gKuTjRUfxI_tZP-cntIaAubzEALw_wcB
4. run your main: uvicorn main:app --reload
    uvicorn: https://www.fatalerrors.org/a/uvicorn-a-lightweight-and-fast-python-asgi-framework.html
    using --reload so it reloads after every change
5. visit http://localhost:8000/ to check
    or visit http://127.0.0.1:8000/docs to see the documentation
6. add further endpoints
7. use 'from typing import Optional' to allow optinal input arguments passing through
8. use 'from pydantic import BaseModel' to make sure your input is santized 

## hilfreiche Posts:
curl Befehl in powershell: https://stackoverflow.com/questions/45183355/invoke-webrequest-cannot-bind-parameter-headers
pipenv/ virtualenv: https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe
postman localhost:
dotenv: https://medium.com/@thejasonfile/using-dotenv-package-to-create-environment-variables-33da4ac4ea8f