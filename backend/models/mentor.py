from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

Base = declarative_base()

class Mentor(Base):
    __tablename__ = "mentors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    photo_url = Column(String(500), nullable=True)
    expertise = Column(String(200), nullable=False)
    bio = Column(Text, nullable=False)
    years_experience = Column(Integer, nullable=False)
    industry = Column(String(100), nullable=False)
    availability_status = Column(String(20), default="available")  # available, busy, unavailable
    email = Column(String(100), unique=True, nullable=False)
    linkedin_profile = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Pydantic models for API
class MentorBase(BaseModel):
    name: str
    expertise: str
    bio: str
    years_experience: int
    industry: str
    email: str
    linkedin_profile: Optional[str] = None
    photo_url: Optional[str] = None

class MentorCreate(MentorBase):
    pass

class MentorResponse(MentorBase):
    id: int
    availability_status: str
    is_verified: bool
    is_active: bool
    rating: float
    total_reviews: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MentorUpdate(BaseModel):
    name: Optional[str] = None
    expertise: Optional[str] = None
    bio: Optional[str] = None
    years_experience: Optional[int] = None
    industry: Optional[str] = None
    availability_status: Optional[str] = None
    linkedin_profile: Optional[str] = None
    photo_url: Optional[str] = None


