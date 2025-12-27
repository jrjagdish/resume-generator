from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import List, Optional, Dict
from datetime import date


class PersonalInfo(BaseModel):
    full_name: str = Field(..., description="Full name of the person")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Location")
    github: Optional[HttpUrl] = Field(None, description="GitHub profile link")
    linkedin: Optional[HttpUrl] = Field(None, description="LinkedIn profile link")
    website: Optional[HttpUrl] = Field(None, description="Personal website")
    summary: str = Field(..., description="Professional summary")


class ExperienceInfo(BaseModel):
    company: str
    role: str
    start_date: date
    end_date: Optional[date] = None
    description: List[str]
    technologies: Optional[List[str]] = None


class ProjectInfo(BaseModel):
    title: str
    description: List[str]
    technologies: Optional[List[str]] = None
    link: Optional[HttpUrl] = None


class EducationInfo(BaseModel):
    institution: str
    degree: str
    start_year: int
    end_year: int


class Resume(BaseModel):
    personal_info: PersonalInfo

    skills: List[str] = Field(..., description="List of skills")

    experience: Optional[List[ExperienceInfo]] = None
    projects: Optional[List[ProjectInfo]] = None

    education: List[EducationInfo]

    certifications: Optional[List[str]] = None
    achievements: Optional[List[str]] = None

    meta: Dict[str, str] = Field(
        default_factory=dict, description="Template and rendering options"
    )
