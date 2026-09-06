from pydantic import BaseModel, Field
from typing import Optional, List

class Profile(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    age: int = Field(ge=0, le=120)
    state: str = "Tamil Nadu"
    district: Optional[str] = Field(default=None, max_length=100)
    gender: str = "any"
    occupation: str = "student"
    annual_income: Optional[float] = None
    life_events: List[str] = []
    family_size: int = Field(default=1, ge=1, le=30)
    education_level: Optional[str] = Field(default=None, max_length=100)
    disability_status: Optional[str] = Field(default=None, max_length=50)
    saved_scheme_ids: List[str] = []

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    profile: Optional[Profile] = None

class SearchRequest(BaseModel):
    query: str = Field(default="", max_length=500)
    category: Optional[str] = None
    state: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=120)
    income: Optional[float] = Field(default=None, ge=0)

class EligibilityRequest(Profile):
    pass

class ProfileRequest(Profile):
    pass

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
