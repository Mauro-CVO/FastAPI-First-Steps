#Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class Location(BaseModel):
    city:str
    state:str
    country:str

class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World!"}

# Request and Response Body

@app.post("/user/new")
def create_user(user: User = Body(...)):
    return user

# Validations Query Parameters

@app.get("/user/details")
def show_user(
    name: Optional[str] = Query(
        None, 
        min_length=2,
        max_length=50,
        title="User name",
        description="This is the user name. It's between 1 and 50 characters"
        ),
    age: int = Query(
        ...,
        title="User age",
        description="This is the user age. It's required"
        ) 
):
    return {name: age}

# Validaciones: Path Parameters

@app.get("/user/details/{user_id}")
def show_user(
    user_id: int = Path(
        ..., 
        gt=0,
        title="User ID",
        description="This is the user ID. It's required"
        )
):
    return {user_id: "User exists"}

# Validations: Request Body

@app.put("/user/{user_id}")
def update_user(
    user_id: int = Path(
        ...,
        title="User ID",
        description="This is the user ID. It's required",
        gte=0
        ),
    user: User = Body(...),
    location: Location = Body(...)
):
    results = user.dict()
    results.update(location.dict())
    return results
