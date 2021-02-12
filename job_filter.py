def accepted_title(title):
    unaccepted = {'staff', 'senior', 'test', 'fullstack', 'full stack', 'webdev', 'web dev', 'web developer', 'front end', 'frontend', 'analyst', 'embedded', 'lead', 'hardware', 'principal', 'sr.'}
    accepted = {'software engineer', 'software developer', 'swe', 'junior developer', 'developer', 'software', 'engineer',
    'software development engineer', 'machine learning', 'ml engineer', 'backend engineer', 'new grad', 'recent'}
    for t in unaccepted:
        if t in title.lower():
            return False
    for t in accepted:
        if t in title.lower():
            return True
    return False

def acceted_level(level):
    if not level:
        return True
    unaccepted = {'senior', 'mid-senior', 'director'}
    for i in unaccepted:
        if i in level.lower():
            return False
    return True

def accepted_description(job_description):
    unaccepted = {'phd', '3+', '2+', '4+', '5+', '6+', '7+', '3 or more years', '4 or more years'}
    for i in unaccepted:
        if i in job_description.lower():
            return False
    return True
