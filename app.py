import json

import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import tempfile
import os
from pdf2image import convert_from_path

st.title("Candidate Matching App")

job_description = st.text_area("Enter Job Description")

candidates = [
    {
        "name": "Alex Smith",
        "text": "Python Data Analyst",
        "skills": [
            {"skill": "python", "types": ["technical skills"], "level": 4},
            {"skill": "data manipulation", "types": ["technical skills"], "level": 4},
            {"skill": "statistical analysis", "types": ["technical skills"], "level": 4},
            {"skill": "data visualization", "types": ["technical skills"], "level": 4},
            {"skill": "pandas", "types": ["tool", "python library"], "level": 4},
            {"skill": "numpy", "types": ["tool", "python library"], "level": 4},
            {"skill": "sql", "types": ["technical skills", "database querying"], "level": 3},
            {"skill": "matplotlib", "types": ["tool", "visualization"], "level": 4},
            {"skill": "seaborn", "types": ["tool", "visualization"], "level": 4},
            {"skill": "problem-solving", "types": ["soft skills"], "level": 4},
            {"skill": "independent work", "types": ["soft skills"], "level": 4},
            {"skill": "communication", "types": ["soft skills"], "level": 4}
        ]
    },
    {
        "name": "Jamie Lee",
        "text": "Junior Data Analyst",
        "skills": [
            {"skill": "python", "types": ["technical skills"], "level": 2},
            {"skill": "data manipulation", "types": ["technical skills"], "level": 2},
            {"skill": "statistical analysis", "types": ["technical skills"], "level": 1},
            {"skill": "data visualization", "types": ["technical skills"], "level": 2},
            {"skill": "pandas", "types": ["tool", "python library"], "level": 2},
            {"skill": "numpy", "types": ["tool", "python library"], "level": 2},
            {"skill": "sql", "types": ["technical skills", "database querying"], "level": 2},
            {"skill": "matplotlib", "types": ["tool", "visualization"], "level": 1},
            {"skill": "seaborn", "types": ["tool", "visualization"], "level": 1},
            {"skill": "problem-solving", "types": ["soft skills"], "level": 2},
            {"skill": "independent work", "types": ["soft skills"], "level": 2},
            {"skill": "communication", "types": ["soft skills"], "level": 2}
        ]
    },
    {
        "name": "Taylor Brown",
        "text": "Node.js Backend Developer",
        "skills": [
            {"skill": "node.js", "types": ["technical skills"], "level": 4},
            {"skill": "javascript", "types": ["technical skills"], "level": 4},
            {"skill": "backend development", "types": ["technical skills"], "level": 4},
            {"skill": "data manipulation", "types": ["technical skills"], "level": 2},
            {"skill": "express.js", "types": ["tool", "javascript framework"], "level": 4},
            {"skill": "mongodb", "types": ["database querying"], "level": 3},
            {"skill": "react", "types": ["tool", "frontend library"], "level": 2},
            {"skill": "problem-solving", "types": ["soft skills"], "level": 4},
            {"skill": "independent work", "types": ["soft skills"], "level": 4},
            {"skill": "communication", "types": ["soft skills"], "level": 3}
        ]
    }
]

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


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


def match_candidates(job_skills, candidates):
    matched_candidates = []
    job_skill_levels = {skill["skill"]: skill["level"] for skill in job_skills['skills']}
    for candidate in candidates:
        score = sum(
            min(job_skill_levels.get(skill["skill"], 0), skill["level"])
            for skill in candidate["skills"]
        )
        matched_candidates.append((candidate, score))
    matched_candidates.sort(key=lambda x: x[1], reverse=True)
    return matched_candidates


def create_candidate_pdf(candidate):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(w=200, h=10, txt=f"Candidate: {candidate['name']}", ln=True)
    for candidate_skill in candidate["skills"]:
        pdf.cell(
            w=200,
            h=10,
            txt=f"{candidate_skill['skill'].capitalize()}: Proficiency Level {candidate_skill['level']}",
            ln=True
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name


def display_pdf_as_images(pdf_path):
    images = convert_from_path(pdf_path)
    for image in images:
        st.image(image, caption="PDF Preview", use_column_width=True)


if st.button("Extract Skills"):
    job_skills = extract_skills(job_description)
    st.json(job_skills)

if st.button("Find Best Matches"):
    job_skills = extract_skills(job_description)
    matched_candidates = match_candidates(job_skills, candidates)
    for candidate, score in matched_candidates[:3]:
        st.write(f"**{candidate['name']}** - Match Score: {score}")

        pdf_path = create_candidate_pdf(candidate)
        st.write("Candidate CV:")
        display_pdf_as_images(pdf_path)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label=f"Download {candidate['name']}'s CV as PDF",
                data=pdf_file,
                file_name=f"{candidate['name']}_match.pdf",
                mime="application/pdf"
            )
