from pydantic import BaseModel, Field
from typing import Optional, List

class Profile(BaseModel):
    age: int = Field(ge=0, le=120)
    state: str = "Tamil Nadu"
    gender: str = "any"
    occupation: str = "student"
    annual_income: Optional[float] = None
    life_events: List[str] = []
    family_size: int = Field(default=1, ge=1, le=30)

class AskRequest(BaseModel):
    question: str
    profile: Optional[Profile] = None

class Scheme(BaseModel):
    id: str
    name: str
    short_description: str
    category: str
    state: str
    min_age: int
    max_age: int
    income_max: Optional[float] = None
    occupations: List[str]
    genders: List[str]
    life_events: List[str]
    benefit: str
    documents: List[str]
    official_url: str
    source: str
    verified: bool = True
    keywords: str = ""

class SchemeResult(Scheme):
    score: int
    reasons: List[str]
