from typing import List,Dict, Any


def normalize_resume_data(data: Dict[str, Any]) -> Dict[str, Any]:
    structured_data = normalize_structure(data)
    return {
        "personal_info": normalize_personal_info(structured_data["personal_info"]),
        "skills": normalize_skills(structured_data["skills"]),
        "experience": normalize_experience(structured_data["experience"]),
        "projects": normalize_projects(structured_data["projects"]),
        "education": normalize_education(structured_data["education"]),
        "certifications": structured_data.get("certifications", []),
    }


def normalize_structure(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "personal_info": data.get("personal_info", {}),
        "skills": data.get("skills", []),
        "experience": data.get("experience", []),
        "projects": data.get("projects", []),
        "education": data.get("education", []),
        "certifications": data.get("certifications", []),
        "meta": data.get("meta", {}),
    }


def normalize_personal_info(info: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "full_name": info.get("full_name", "").strip(),
        "email": info.get("email", "").strip(),
        "phone": info.get("phone", "").strip(),
        "location": info.get("location", "").strip(),
        "github": info.get("github", "").strip(),
        "linkedin": info.get("linkedin", "").strip(),
        "website": info.get("website", "").strip(),
        "summary": info.get("summary", "").strip(),
    }


def normalize_skills(skills: list):
    return list(
        map(
            lambda s: (
                {"name": s.strip()}
                if isinstance(s, str)
                else {"name": s.get("name", "").strip()}
            ),
            skills,
        )
    )


def normalize_experience(experiences: List[Dict[str, Any]]):
    normalized_experiences = []
    for exp in experiences:
        normalized_experiences.append(
            {
                "company": exp.get("company", "").strip(),
                "role": exp.get("role", "").strip(),
                "start_date": exp.get("start_date"),
                "end_date": exp.get("end_date"),
                "description": list(
                    map(lambda d: d.strip(), exp.get("description", []))
                ),
                "technologies": list(
                    map(lambda t: t.strip(), exp.get("technologies", []))
                ),
            }
        )
    return normalized_experiences


def normalize_projects(projects: List[Dict[str, Any]]):
    normalized_projects = []
    for proj in projects:
        normalized_projects.append(
            {
                "title": proj.get("title", "").strip(),
                "description": list(
                    map(lambda d: d.strip(), proj.get("description", []))
                ),
                "technologies": list(
                    map(lambda t: t.strip(), proj.get("technologies", []))
                ),
                "link": proj.get("link", "").strip(),
            }
        )
    return normalized_projects


def normalize_education(educations: List[Dict[str, Any]]):
    normalized_educations = []
    for edu in educations:
        normalized_educations.append(
            {
                "institution": edu.get("institution", "").strip(),
                "degree": edu.get("degree", "").strip(),
                "start_year": edu.get("start_year"),
                "end_year": edu.get("end_year"),
            }
        )
    return normalized_educations
