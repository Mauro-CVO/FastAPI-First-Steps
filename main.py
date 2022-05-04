#Python
import email
from typing import Optional
from enum import Enum
from urllib.parse import scheme_chars

# Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr, PaymentCardNumber, PastDate

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Country(Enum):
    mexico = "Mexico"
    colombia = "Colombia"
    peru = "Peru"
    chile = "Chile"
    argentina = "Argentina"
    brazil = "Brasil"

class Location(BaseModel):
    city:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="CDMX"
        )
    state:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="CDMX"
        )
    country:Optional[Country] = Field(default=None, example="Mexico")
    

class User(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Mauro"
        )
    last_name: str= Field(
        ...,
        min_length=1,
        max_length=50,
        example="Cortes"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example="23"
        )
    email: EmailStr = Field(..., example="mau@gmail.com")
    credit_card: PaymentCardNumber = Field(..., example="4417123456789113")
    birthday: PastDate = Field(..., example="1999-04-21")
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=True)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name" : "Mauro",
    #             "last_name" : "Cortes",
    #             "age" : "23",
    #             "email": "mauro@gmail.com",
    #             "credit_card": "4417123456789113",
    #             "birthday" : "1999-04-21",
    #             "hair_color" :"black",
    #             "is_married" : True
    #         }
    #     }


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
