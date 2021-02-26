def accepted_title(title):
    """ Checks if job title should be accepted

    unaccepted -- list of keywords that make a job title unacceptable
    accepted -- list of keywords that make a job title acceptable
    """
    unaccepted = {'staff', 'senior', 'test', 'fullstack', 'full stack', 'webdev', 'web dev', \
        'web developer', 'front end', 'frontend', 'analyst', 'embedded', 'lead', 'hardware', \
            'principal', 'sr.', 'c++', 'ruby', 'java', 'phd', 'postgraduate', 'node'}
    accepted = {'software engineer', 'software developer', 'swe', 'junior developer', 'developer',\
         'software', 'engineer', 'software development engineer', 'machine learning', 'ml engineer', \
            'backend engineer', 'new grad', 'recent'}

    if any(w in title.lower() for w in unaccepted):
        return False
    if any(w in title.lower() for w in accepted):
        return True
    return False

def accepted_level(level):
    """ Checks if job level should be accepted

    unaccepted -- lisy of levels that make a job posting unacceptable
    Empty level is accepted
    """
    unaccepted = {'senior', 'mid-senior', 'director'}

    if any(w in level.lower() for w in unaccepted):
        return False
    return True

def accepted_description(description):
    """ Checks if job description should be accepted 

    unaccepted -- list of keywords that make job description unacceptable
    """
    unaccepted = {'3+', '2+', '4+', '5+', '6+', '7+', '3 or more years', '4 or more years', '5 or more years'}

    if any(w in description.lower() for w in unaccepted):
        return False
    return True


# Test title filter
assert accepted_title('Staff Software Engineer') == False, 'Unaccepted keyword in title not detected'
assert accepted_title('Python Software Engineer') == True, 'Accepted keyword in title not detected'
assert accepted_title('Sales representative') == False, 'Unaccepted title not filtered out'


# Test level filter
assert accepted_level('Senior') == False, 'Unaccepted level is not filtered out'
assert accepted_level('Entry Level') == True, 'Accepted level in title not detected'
assert accepted_level('') == True, 'Empty level should be accepted'

# Test description
assert accepted_description('Requirements: 5+ years experience') == False, 'Unaccepted keyword in description is not filtered out'
assert accepted_description('Requirements: A degree in Computer Science') == True, 'Accepted description should not be filtered out'







