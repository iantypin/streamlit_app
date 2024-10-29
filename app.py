import streamlit as st
import openai
from fpdf import FPDF

st.title("Candidate Matching App")

job_description = st.text_area("Enter Job Description")

candidates = [
   {"name": "Alice", "skills": {"python": 4, "data analysis": 3}},
   {"name": "Bob", "skills": {"python": 2, "project management": 4}},
]


def extract_skills(job_description):
    prompt = f"Extract skills and proficiency from the job description:\n{job_description}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
    )
    return response.choices[0].text.strip()


def match_candidates(job_skills, candidates):
    matched_candidates = []
    for candidate in candidates:
        score = sum([
            min(job_skills.get(skill, 0), candidate["skills"].get(skill, 0))
            for skill in job_skills
        ])
        matched_candidates.append((candidate, score))
    matched_candidates.sort(key=lambda x: x[1], reverse=True)
    return matched_candidates


def create_candidate_pdf(candidate):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Candidate: {candidate['name']}", ln=True)
    for skill, level in candidate["skills"].items():
        pdf.cell(200, 10, txt=f"{skill}: Proficiency Level {level}", ln=True)
    pdf.output(f"{candidate['name']}_match.pdf")


if st.button("Find Best Matches"):
    job_skills = extract_skills(job_description)
    matched_candidates = match_candidates(job_skills, candidates)
    for candidate, score in matched_candidates[:3]:
        create_candidate_pdf(candidate)
        st.write(f"{candidate['name']}: Match Score {score}")
