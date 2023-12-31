# Text for the two features
feature1_text = "Helping you efficiently find PhD studentship opportunities in the UK."
feature2_text = "Helping you efficiently find academic job opportunities in the UK."

# Expanded Introductory text
intro_text = """
Welcome to the DGendooLab Career Finder, a web application led by [Dr Deena Gendoo](https://www.birmingham.ac.uk/staff/profiles/cancer-genomic/gendoo-deena.aspx), and developed by the intern team at DGendoo Lab. Career Finder is designed for our students, to be a one-stop destination for academic and research opportunities. Whether you are a student looking for Ph.D. studentships or a professional seeking academic jobs, Career Finder has got you covered.

Explore the word cloud generated from the latest academic listings and gain insights into the trending research areas and disciplines. Our application empowers you with an efficient and intuitive interface, making your search process seamless.

Join us on [GitHub](https://github.com/DGendooLab/Emerging-STEM) to contribute to the project and improve the Career Finder for the academic community.

So, what are you waiting for? Start your journey towards a successful academic career with Career Finder!
"""

dev_team_text = """
Dr. Deena Gendoo is an Associate Professor of Computational Biology at the University of Birmingham in the United Kingdom. She also serves as the Program Director for the MSc Bioinformatics program at the university.

The Gendoo Lab specializes in translational bioinformatics and integrative approaches to characterizing patients and preclinical models across various cancer types and diseases. To address fundamental questions in biology and medicine, the lab employs a diverse array of machine learning, artificial intelligence methods, data science techniques, and integrative analyses of biological 'omics data and health data. This rich diversity has inspired the creation of this platform to assist individuals in exploring their career potential across these interdisciplinary fields.

For more information about the Gendoo Lab and our work:
- [University Profile](https://www.birmingham.ac.uk/staff/profiles/cancer-genomic/gendoo-deena.aspx)
- Twitter: @DGendoo
- LinkedIn: [Deena Mohamad Gendoo](http://ca.linkedin.com/in/deena-mohamad-gendoo-b4979b50)
- Google Scholar: [Deena Gendoo on Google Scholar](https://scholar.google.co.uk/citations?user=GedTo_AAAAAJ&hl=en&oi=ao)

Intern Team:

[Xiangyi Zhou](https://www.linkedin.com/in/xiangyi-zhou-code/), MSc student in Computer Science at the University of Birmingham

[Hanqing Zhao](https://www.linkedin.com/in/hanqing-zhao-a1a88b250/), MSc student in Data Science at the University of Birmingham

[Aliyu Suleiman](https://www.linkedin.com/in/ausuleiman99/), BSc student in Computer Science at the University of Birmingham

We welcome your feedback, comments, and suggestions. Feel free to reach out to Dr. Gendoo at d.gendoo@bham.ac.uk.
"""

default_parameters_job_page = {
    'search_keywords': '',
    'academic_discipline': 'biological-sciences',
    'ordered_keywords': "Junior, Assistant, Research, Data",
    'exclude_keywords': "Lecturer",
}

heading_job_page = """
- Are you looking for exciting job opportunities in your field? Use our search tool to find the perfect job that matches your skills and interests. Whether you're searching by job title, company, or location, our platform will help you discover the right fit.

- Simply enter relevant keywords to narrow down your search, or explore job opportunities.

- Start your journey towards a fulfilling career today! Click the "Find Jobs" button below to begin your job search.
"""

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
    'search_keywords': '',
    'academic_discipline': 'computer-sciences',
    'hours_type': 'full-time',
    'funding_type': 'international-students',
    'ordered_keywords': "Artificial, Machine, Robot, Automation, Simulation",
    'exclude_keywords': "Data",
}

heading_phd_page = """
- Are you ready to explore exciting PhD opportunities? Use our search tool to find the perfect PhD program that aligns with your interests and academic goals. Whether you're interested in a specific academic discipline, funding type, or research hours, our platform will help you discover the right fit.

- Simply enter relevant keywords to narrow down your search, or choose from the available academic disciplines, funding types, and hours options. You can even filter PhDs that include specific keywords in their titles.

- Start your journey towards a rewarding research career today! Click the "Find PhDs" button below to begin your search.
"""

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

recommended_keywords = [
    "Bioinformatician",
    "Bioinformatics",
    "Computational biologist",
    "Computational biology",
    "Data Scientist",
    "Data Science",
    "Data Analyst",
    "Research Assistant",
    "PhD Studentship",
    "Biomedical",
    "Machine learning",
    "Biotechnology",
    "Software",
    "Data Coordinator",
    "Health Informatics",
    "Medical Informatics",
    "Early career",
    "Informatics",
    "Omics",
    "Genomic",
    "NGS",
    "Systems Biology"
]
