from dataclasses import dataclass

@dataclass
class Job_Posting:
    "Job posting class for storing all job attributes"
    hash: str
    title: str
    date_posted: str
    link: str
    company: str
    location: str
    level: str
    description: str
    accepted: int