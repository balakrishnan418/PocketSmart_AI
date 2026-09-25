from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1)
    style: str = "Modern"
    notes: str = ""


class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10_000)
    event_type: str = "Birthday"
    venue: str = "Home"
    city: str = ""
    notes: str = ""


class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = "Casual"
    style: str = "Elegant"
    outfit_color: str = ""
    notes: str = ""
