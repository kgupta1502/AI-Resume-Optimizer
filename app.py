import streamlit as st
from ResumeGenie import call_openrouter
from PyPDF2 import PdfReader
import docx

st.set_page_config(page_title=" ResumeGenie–AI", layout="centered")
st.title(" ResumeGenie–AI (Boost Your Resume with AI)")

resume_file = st.file_uploader("&#128228; Upload your resume", type=["pdf", "docx", "txt"])
job_desc = st.text_area("&#128204; Paste Job Description here")

def extract_text(file):
    if file.name.endswith(".pdf"):
        pdf = PdfReader(file)
        return "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif file.name.endswith(".docx"):
        document = docx.Document(file)
        return "\n".join([para.text for para in document.paragraphs])
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""

if st.button("&#128640; Optimize Resume"):
    if not resume_file or not job_desc:
        st.error("Please upload a resume and paste a job description.")
    else:
        resume_text = extract_text(resume_file)
        prompt = f"""
        You are simulating an advanced Applicant Tracking System (ATS) used by top tech companies.

        Evaluate how well the following resume matches the given job description.

        Job Description:
        {job_desc}

        My Resume:
        {resume_text}

        Please analyze how well my resume matches the job description.
        Give the following:
        - An ATS match score out of 100
        - List of missing skills or keywords
        - Suggestions to improve the resume
        - Summary of how my profile fits the role
        """

        with st.spinner("Analyzing your resume..."):
            result = call_openrouter(prompt, model="openai/gpt-3.5-turbo")

        st.subheader("&#128202; Optimization Results")
        st.markdown(result)
