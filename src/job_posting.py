from dataclasses import dataclass

@dataclass
class Job_Posting:
    "Job posting class for storing all job attributes"
    title: str
    date_posted: str
    link: str
    company: str
    location: str
    level: str
    description: str