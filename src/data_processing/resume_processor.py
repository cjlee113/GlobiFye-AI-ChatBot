from pyresparser import ResumeParser

def process_resume(resume_path):
    """Parses the resume to extract structured data."""
    data = ResumeParser(resume_path).get_extracted_data()
    return {
        'skills': data.get('skills', []),
        'industry': data.get('industry', 'unknown'),
        'experience': data.get('total_experience', 0)
    }