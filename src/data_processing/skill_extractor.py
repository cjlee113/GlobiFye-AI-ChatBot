def extract_skills(data):
    """Extracts and refines skills from resume data."""
    skills = data.get('skills', [])
    # Further filter skills here if necessary
    return [skill.lower() for skill in skills if len(skill) > 2]  # Remove short/irrelevant words