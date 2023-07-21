default_parameters_job_page = {
    'search_keywords': '',
    'academic_discipline': 'biology-sciences',
    'ordered_keywords': "Junior, Assistant, Research, Data",
    'exclude_keywords': "Lecturer",
}

heading_job_page = '''
## Welcome to EmergingSTEM-Job

**How to use the app:**

- Input search keywords and select your preferred academic discipline from the dropdown menus.
- Enter keywords in the "Keywords in Title" field to filter the results based on specific criteria.
- Use the "Keywords to Exclude" field to exclude certain keywords from the results.
- Adjust the range slider to refine the search based on the relevance of the keywords.
- Click the "Find Jobs" button to retrieve the matching Job listings.
- Explore the results, download the data, and generate a word cloud for the titles.

**Note: Parsing through all data can take some time.**

'''
academic_discipline_options = [
    {"label": "Agriculture, Food & Veterinary",
        "value": "agriculture-food-and-veterinary"},
    {"label": "Biological Sciences", "value": "biological-sciences"},
    {"label": "Computer Sciences", "value": "computer-sciences"},
    {"label": "Engineering & Technology", "value": "engineering-and-technology"},
    {"label": "Health & Medical", "value": "health-and-medical"},
    {"label": "Mathematics & Statistics", "value": "mathematics-and-statistics"},
    {"label": "Physical & Environmental Sciences",
        "value": "physical-and-environmental-sciences"}
]

default_parameters_phd_page = {
    'academic_discipline': 'computer-sciences',
    'hours_type': 'full-time',
    'funding_type': 'international-students',
    'ordered_keywords': "Artificial, Machine, Robot, Automation, Simulation",
    'exclude_keywords': "Data",
}

heading_phd_page = '''
## Welcome to EmergingSTEM-PhD

**How to use the app:**

- Select your preferred academic discipline, hours type, and funding type from the dropdown menus.
- Enter keywords in the "Keywords in Title" field to filter the results based on specific criteria.
- Use the "Keywords to Exclude" field to exclude certain keywords from the results.
- Adjust the range slider to refine the search based on the relevance of the keywords.
- Click the "Find PhDs" button to retrieve the matching PhD listings.
- Explore the results, download the data, and generate a word cloud for the titles.

**Note: Parsing through all data can take some time.**

'''

funding_type_options = [
    {"label": "EU Students", "value": "eu-students"},
    {"label": "International Students", "value": "international-students"},
    {"label": "Self-funded Students", "value": "self-funded-students"},
    {"label": "UK Students", "value": "uk-students"},
]

hours_type_options = [
    {"label": "Full-time", "value": "full-time"},
    {"label": "Part-time", "value": "part-time"},
]
