from fastapi import FastAPI, status
from pydantic import BaseModel , SecretStr
from typing import List, Optional
from pydantic.networks import EmailStr
from uuid import uuid4
from fastapi.responses import JSONResponse , Response

app = FastAPI()

class UserModel(BaseModel):
    id: Optional[str]
    name: str
    surname: Optional[str]
    email: EmailStr
    password: SecretStr


users: List[UserModel] = []  



@app.get('/')
def read_root():
    content = dict(status = 'Ok!')
    content_redundant = {'status':'OK!'}
    return content

@app.get('/users')
def get_users():
    return users

@app.get('/users/{id}')
def get_user(id:str):

    for user in users:
        if user.id == id:
            return user

    return  JSONResponse(dict(error = 'user not found.'),status_code=status.HTTP_404_NOT_FOUND)


@app.post('/users',status_code=status.HTTP_201_CREATED)
def create_user(user: UserModel):
    id = str(uuid4())
    new_user = UserModel(
        id = id,
        name = user.name,
        surname = user.surname,
        email = user.email,
        password = user.password,      
    )
    users.append(new_user)
    return new_user
     
@app.put('/users')
def update_user(user: UserModel):
    if user.id is None:
        return JSONResponse(dict(error = 'Id Missing...'),status_code=status.HTTP_400_BAD_REQUEST)
    
    for updated_user in users:
        if updated_user.id == user.id:
            updated_user.name = user.name
            updated_user.email = user.email
            update_user.surname = user.surname
            update_user.password = user.password.get_secret_value()

            return updated_user
    
    return  JSONResponse(dict(error = 'user not found.'),status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/users/{id}')
def delete_user(id:str):
    for user in users:
        if user.id == id:
            users.remove(user)
            return Response(user.id)
    
    return  JSONResponse(dict(error = 'user not found.'),status_code=status.HTTP_404_NOT_FOUND)





    





