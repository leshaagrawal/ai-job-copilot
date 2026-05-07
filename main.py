from fastapi import FastAPI, UploadFile, File
from groq import Groq
import os
from dotenv import load_dotenv
import PyPDF2
import docx
import requests
# 🔥 RAG imports
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

load_dotenv()

app = FastAPI()

# ✅ Groq setup
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ LLM call
def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ safe working model
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# =========================
# 🔥 RAG SETUP
# =========================

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def create_chunks(text, chunk_size=200):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def create_vector_db(chunks):
    embeddings = embed_model.encode(chunks)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index, embeddings

def retrieve_chunks(query, chunks, index, embeddings):
    query_embedding = embed_model.encode([query])
    D, I = index.search(np.array(query_embedding), k=3)

    return [chunks[i] for i in I[0]]


# =========================
# 🚀 APIs
# =========================

@app.get("/")
def home():
    return {"message": "AI Job Copilot Running 🚀"}


# ✅ Ask AI
@app.get("/ask")
def ask_ai(question: str):
    answer = ask_groq(question)
    return {"answer": answer}


# ✅ Upload + RAG analyze
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        resume_text = extract_text(file)

        if not resume_text:
            return {"analysis": "No text found in resume"}

        # 🔥 RAG logic
        chunks = create_chunks(resume_text)
        index, embeddings = create_vector_db(chunks)

        relevant_chunks = retrieve_chunks(
            "Give resume improvements",
            chunks,
            index,
            embeddings
        )

        context = "\n".join(relevant_chunks)

        prompt = f"""
        Act as a senior technical recruiter.

        Use the resume context below:
        {context}

        Give:
        1. Improvements
        2. Missing skills
        3. ATS optimization tips
        """

        answer = ask_groq(prompt)

        return {"analysis": answer}

    except Exception as e:
        return {"error": str(e)}


# ✅ Chat with resume (FIXED 🔥)
@app.post("/chat")
async def chat_with_resume(file: UploadFile = File(...), question: str = ""):
    try:
        resume_text = extract_text(file)

        chunks = create_chunks(resume_text)
        index, embeddings = create_vector_db(chunks)

        relevant = retrieve_chunks(question, chunks, index, embeddings)

        context = "\n".join(relevant)

        prompt = f"""
        Answer the question using resume context:

        {context}

        Question: {question}
        """

        answer = ask_groq(prompt)

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}


# =========================
# 📄 Extract text
# =========================

def extract_text(file: UploadFile):
    if file.filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text

    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join([para.text for para in doc.paragraphs])

    return ""

# =========================
# ✅ ATS SCORE (NEW)
# =========================
@app.post("/ats-score")
async def ats_score(file: UploadFile = File(...)):
    try:
        resume_text = extract_text(file)

        if not resume_text:
            return {"ats": "No text found"}

        prompt = f"""
        You are an ATS (Applicant Tracking System).

        Analyze this resume and give:

        1. ATS Score out of 100
        2. Why this score
        3. How to improve it

        Resume:
        {resume_text}
        """

        answer = ask_groq(prompt)

        return {"ats": answer}

    except Exception as e:
        return {"error": str(e)}


# =========================
# ✅ JOB MATCHING (NEW)
# =========================
@app.post("/job-matches")
async def job_matches(file: UploadFile = File(...)):
    try:
        resume_text = extract_text(file)

        if not resume_text:
            return {"jobs": "No text found"}

        prompt = f"""
        Based on this resume, suggest 5 job roles.

        For each job:
        - Title
        - Skills required
        - Why suitable
        - Direct apply link (use LinkedIn search links)

        Resume:
        {resume_text}
        """

        answer = ask_groq(prompt)

        return {"jobs": answer}

    except Exception as e:
        return {"error": str(e)}


@app.get("/find-jobs")
def find_jobs(role: str = "python developer"):
    try:
        url = "https://serpapi.com/search.json"

        params = {
            "engine": "google_jobs",
            "q": role,
            "location": "India",
            "api_key": os.getenv("SERPAPI_KEY")
        }

        response = requests.get(url, params=params)
        data = response.json()

        jobs = []

        for job in data.get("jobs_results", [])[:5]:

            # ✅ FIXED LINK EXTRACTION
            apply_link = "Apply via Google Jobs"

            if "related_links" in job and len(job["related_links"]) > 0:
                apply_link = job["related_links"][0].get("link", apply_link)

            elif "apply_options" in job and len(job["apply_options"]) > 0:
                apply_link = job["apply_options"][0].get("link", apply_link)

            elif "job_id" in job:
                # fallback to Google jobs page
                apply_link = f"https://www.google.com/search?q={job['title'].replace(' ', '+')}+jobs"

            jobs.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "link": apply_link
            })

        return {"jobs": jobs}

    except Exception as e:
        return {"error": str(e)}