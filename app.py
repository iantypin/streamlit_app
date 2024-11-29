import json

import streamlit as st
from openai import OpenAI
import os
from pdf2image import convert_from_path
from esco import EscoExtractor

st.title("Candidate Matching App with ESCO Validation")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

esco_extractor = EscoExtractor()

job_skills = None

candidates = [
    {
        "name": "Ben Walsh",
        "text": "Senior Partnerships Manager",
        "skills": [
            {"skill": "project management", "types": ["soft skills"], "level": 4},
            {"skill": "client services", "types": ["soft skills"], "level": 4},
            {"skill": "strategy development", "types": ["soft skills"], "level": 4},
            {"skill": "communication", "types": ["soft skills"], "level": 4},
            {"skill": "critical thinking", "types": ["soft skills"], "level": 4},
            {"skill": "presentation", "types": ["soft skills"], "level": 4},
            {"skill": "pitch development", "types": ["soft skills"], "level": 4},
            {"skill": "presentation", "types": ["soft skills"], "level": 4},
        ],
        "cv_file": "/mount/src/streamlit_app/cvs/Ben Walsh CV.pdf",
        # "cv_file": "cvs/Ben Walsh CV.pdf",
    },
    {
        "name": "Hasan Savas",
        "text": "IT Systems/Data Engineer",
        "skills": [
            {"skill": "data science", "types": ["technical skills"], "level": 4},
            {"skill": "predictive modeling", "types": ["technical skills", "data science"], "level": 3},
            {"skill": "data visualization", "types": ["technical skills", "data science"], "level": 3},
            {"skill": "machine learning", "types": ["technical skills", "data science"], "level": 4},
            {"skill": "data wrangling", "types": ["technical skills", "data science"], "level": 3},
            {"skill": "database management", "types": ["technical skills"], "level": 3},
            {"skill": "python", "types": ["technical skills", "programming language"], "level": 4},
            {"skill": "sql", "types": ["technical skills", "programming language", "database querying"], "level": 4},
            {"skill": "bash shell scripting", "types": ["technical skills", "scripting"], "level": 3},
            {"skill": "scikit-learn", "types": ["tool", "python library"], "level": 3},
            {"skill": "pandas", "types": ["tool", "python library"], "level": 4},
            {"skill": "numpy", "types": ["tool", "python library"], "level": 4},
            {"skill": "scipy", "types": ["tool", "python library"], "level": 3},
            {"skill": "statsmodels", "types": ["tool", "python library"], "level": 3},
            {"skill": "anaconda", "types": ["tool", "development environment"], "level": 3},
            {"skill": "keras", "types": ["tool", "machine learning framework"], "level": 3},
            {"skill": "aws", "types": ["cloud computing", "platform"], "level": 3},
            {"skill": "aws s3", "types": ["cloud storage", "aws service"], "level": 3},
            {"skill": "aws athena", "types": ["cloud analytics", "aws service"], "level": 3},
            {"skill": "xgboost", "types": ["machine learning", "algorithm"], "level": 3},
            {"skill": "problem-solving", "types": ["soft skills"], "level": 3},
            {"skill": "continuous learning", "types": ["soft skills"], "level": 3},
            {"skill": "statistical modeling", "types": ["technical skills", "data science"], "level": 3}
        ],
        "cv_file": "/mount/src/streamlit_app/cvs/HasanSavas_Resume.pdf",
        # "cv_file": "cvs/HasanSavas_Resume.pdf",
    },
    {
        "name": "David N. Silverstein",
        "text": "Machine Learning and Computational Neuroscience Specialist",
        "skills": [
            {"skill": "machine learning", "types": ["technical skills"], "level": 4},
            {"skill": "deep learning", "types": ["technical skills", "machine learning"], "level": 4},
            {"skill": "recurrent neural networks", "types": ["technical skills", "machine learning"], "level": 3},
            {"skill": "unsupervised learning", "types": ["technical skills", "machine learning"], "level": 3},
            {"skill": "classifiers", "types": ["technical skills", "machine learning"], "level": 3},
            {"skill": "probabilistic reasoning", "types": ["technical skills", "machine learning"], "level": 3},
            {"skill": "time-series prediction", "types": ["technical skills", "data science"], "level": 3},
            {"skill": "inference engines", "types": ["technical skills"], "level": 3},
            {"skill": "genetic algorithms", "types": ["technical skills", "machine learning"], "level": 3},
            {"skill": "natural language processing", "types": ["technical skills", "machine learning"], "level": 4},
            {"skill": "computational neuroscience", "types": ["technical skills", "data science"], "level": 4},
            {"skill": "NeuroAI", "types": ["technical skills", "artificial intelligence"], "level": 3},
            {"skill": "AGI", "types": ["technical skills", "artificial intelligence"], "level": 2},
            {"skill": "data visualization", "types": ["technical skills"], "level": 3},
            {"skill": "cloud platforms", "types": ["technical skills", "deployment"], "level": 3},
            {"skill": "supercomputing", "types": ["technical skills", "deployment"], "level": 3},
            {"skill": "Python", "types": ["programming language"], "level": 4},
            {"skill": "Java", "types": ["programming language"], "level": 3},
            {"skill": "SQL", "types": ["programming language"], "level": 3},
            {"skill": "MATLAB/Octave", "types": ["programming language"], "level": 3},
            {"skill": "R", "types": ["programming language"], "level": 3},
            {"skill": "C/C++", "types": ["programming language"], "level": 3},
            {"skill": "Pytorch", "types": ["tool", "machine learning framework"], "level": 3},
            {"skill": "scikit-learn", "types": ["tool", "machine learning library"], "level": 3},
            {"skill": "pandas", "types": ["tool", "data analysis"], "level": 3},
            {"skill": "numpy", "types": ["tool", "data analysis"], "level": 3},
            {"skill": "networkx", "types": ["tool", "network analysis"], "level": 3},
            {"skill": "sqlite3", "types": ["tool", "database"], "level": 3},
            {"skill": "gensim", "types": ["tool", "NLP"], "level": 3},
            {"skill": "LLMs", "types": ["technical skills", "machine learning"], "level": 3},
            {"skill": "MySQL", "types": ["database"], "level": 3},
            {"skill": "MariaDB", "types": ["database"], "level": 3},
            {"skill": "PostgreSQL", "types": ["database"], "level": 3},
            {"skill": "Oracle", "types": ["database"], "level": 3},
            {"skill": "SQL Server", "types": ["database"], "level": 3},
            {"skill": "SQLite", "types": ["database"], "level": 3},
            {"skill": "Neo4j", "types": ["database"], "level": 3},
            {"skill": "Linux", "types": ["environment"], "level": 4},
            {"skill": "Docker", "types": ["environment", "containerization"], "level": 3},
            {"skill": "Slurm", "types": ["environment", "scheduler"], "level": 3},
            {"skill": "PyCharm", "types": ["environment", "IDE"], "level": 3},
            {"skill": "Git", "types": ["version control"], "level": 3},
            {"skill": "GCP", "types": ["cloud platform"], "level": 3},
            {"skill": "AWS", "types": ["cloud platform"], "level": 3},
            {"skill": "Runpod", "types": ["cloud platform"], "level": 2},
            {"skill": "IoT", "types": ["deployment"], "level": 2},
            {"skill": "finance modeling", "types": ["domain expertise"], "level": 3},
            {"skill": "neuroscience modeling", "types": ["domain expertise"], "level": 3},
            {"skill": "bioinformatics", "types": ["domain expertise"], "level": 3},
            {"skill": "climate modeling", "types": ["domain expertise"], "level": 3}
        ],
        # "cv_file": "cvs/Resume-DS.pdf",
        "cv_file": "/mount/src/streamlit_app/cvs/Resume-DS.pdf",
    }
]

job_description = st.text_area("Enter Job Description")


def extract_skills(job_description):
    example_job_skills = {
        "skills": [
            {"skill": "python", "types": ["technical skills"], "level": 4},
            {"skill": "data manipulation", "types": ["technical skills"], "level": 4},
            {"skill": "statistical analysis", "types": ["technical skills"], "level": 3},
            {"skill": "data visualization", "types": ["technical skills"], "level": 3},
            {"skill": "pandas", "types": ["tool", "python library"], "level": 4},
            {"skill": "numpy", "types": ["tool", "python library"], "level": 4},
            {"skill": "sql", "types": ["technical skills", "database querying"], "level": 3},
            {"skill": "matplotlib", "types": ["tool", "visualization"], "level": 3},
            {"skill": "seaborn", "types": ["tool", "visualization"], "level": 3},
            {"skill": "problem-solving", "types": ["soft skills"], "level": 3},
            {"skill": "independent work", "types": ["soft skills"], "level": 3},
            {"skill": "communication", "types": ["soft skills"], "level": 3}
        ]
    }
    prompt = f"""
    Extract the skills from the following job description in JSON format.
    Please include the skill name, types and proficiency level for each skill based on the information in the job description.
    Format the response strictly as JSON, with no additional text or explanations.

    **Skill Annotation Details:**
    - All skill names and types must be in lowercase. For example, use "skill" not "SKILL".
    - Skills may be multi-word phrases, separated by spaces (e.g., "software engineering").
    - Each skill may be associated with multiple categories or types, such as "technical skills" or "soft skills."
    - Nested skills are allowed, where one skill may contain another.
    - Each skill will have a corresponding proficiency level based on the candidate’s experience.

    Job Description:\n{job_description}

    Example JSON format:\n{example_job_skills}

    Only output the JSON, without any additional text.
    """
    response = client.chat.completions.create(
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        model="gpt-3.5-turbo",
    )
    return json.loads(response.choices[0].message.content)


def validate_job_desc_skills(job_skills, esco_extractor):
    job_skill_names = [skill["skill"] for skill in job_skills['skills']]

    validated_skills = esco_extractor.validate_skills(job_skill_names)

    updated_skills = []
    for skill in job_skills['skills']:
        not_ver_skill = skill['skill']
        if not_ver_skill in validated_skills:
            updated_skill = skill.copy()
            updated_skill["skill"] = validated_skills[not_ver_skill]
            updated_skills.append(updated_skill)

    return {"skills": updated_skills}


def match_candidates(job_skills, candidates):
    matched_candidates = []
    updated_skills = []

    job_skill_levels = {skill["skill"]: skill["level"] for skill in job_skills['skills']}
    for candidate in candidates:
        score = 0
        matched_skills = []
        unmatched_skills = []

        candidate_skills = [skill["skill"] for skill in candidate["skills"]]
        validated_skills = esco_extractor.validate_skills(candidate_skills)

        for skill in candidate["skills"]:
            not_ver_skill = skill['skill']
            if not_ver_skill in validated_skills:
                updated_skill = skill.copy()
                updated_skill["skill"] = validated_skills[not_ver_skill]
                updated_skills.append(updated_skill)

        for skill in updated_skills:
            job_level = job_skill_levels.get(skill["skill"])
            if job_level is not None:
                match_level = min(job_level, skill["level"])
                score += match_level
                matched_skills.append(
                    {"skill": skill["skill"], "candidate_level": skill["level"], "job_level": job_level}
                )
            else:
                unmatched_skills.append({"skill": skill["skill"], "candidate_level": skill["level"]})

        matched_candidates.append((candidate, score, matched_skills, unmatched_skills))

    matched_candidates.sort(key=lambda x: x[1], reverse=True)
    return matched_candidates


def display_pdf_as_images(pdf_path):
    images = convert_from_path(pdf_path)
    for image in images:
        st.image(image, caption="PDF Preview", use_container_width=True)


if "job_skills" not in st.session_state:
    st.session_state.job_skills = None

if st.button("Extract Skills"):
    st.session_state.job_skills = extract_skills(job_description)
    st.json(st.session_state.job_skills)

if st.button("Approve Job Description Skills by ESCO"):
    if st.session_state.job_skills:
        st.session_state.job_skills = validate_job_desc_skills(st.session_state.job_skills, esco_extractor)
        st.success("Job description skills have been validated and updated!")
        st.json(st.session_state.job_skills)
    else:
        st.write("Please extract skills from the job description first.")

if st.button("Find Best Matches"):
    if not st.session_state.job_skills:
        st.write("Please extract skills in order to find the best matches.")

    matched_candidates = match_candidates(st.session_state.job_skills, candidates)
    for candidate, score, matched_skills, unmatched_skills in matched_candidates[:3]:
        st.write(f"**{candidate['name']}** - Match Score: {score}")

        st.write("Matched Skills:")
        for match in matched_skills:
            st.write(
                f"- {match['skill'].capitalize()} (Candidate Level: {match['candidate_level']}, Job Level: {match['job_level']})")

        if unmatched_skills:
            st.write("Unmatched Skills:")
            for unmatched in unmatched_skills:
                st.write(f"- {unmatched['skill'].capitalize()} (Candidate Level: {unmatched['candidate_level']})")

        if candidate["cv_file"]:
            st.write("Candidate CV Preview:")
            display_pdf_as_images(candidate["cv_file"])
            with open(candidate["cv_file"], "rb") as pdf_file:
                st.download_button(
                    label=f"Download {candidate['name']}'s CV as PDF",
                    data=pdf_file,
                    file_name=f"{candidate['name']}_CV.pdf",
                    mime="application/pdf"
                )
