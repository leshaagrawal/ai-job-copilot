# 🚀 AI Job Copilot

An AI-powered Resume Analyzer & Job Search Assistant built using **FastAPI, Streamlit, RAG, FAISS, and Groq LLM**.

This application helps users:
- Analyze resumes using AI
- Calculate ATS score
- Chat with resume context using RAG
- Find relevant jobs in real-time
- Get AI-based job recommendations

---

# ✨ Features

## ✅ Resume Analysis
Upload PDF/DOCX resumes and receive:
- Resume improvements
- Missing skills
- ATS optimization tips

---

## ✅ ATS Score Generator
AI evaluates the resume and provides:
- ATS score out of 100
- Keyword optimization suggestions
- Formatting improvements

---

## ✅ Resume Chat (RAG-based)
Users can ask questions like:
- “What skills are missing?”
- “Which role suits me best?”
- “Summarize my experience”

Implemented using:
- Sentence Transformers
- FAISS vector search
- Retrieval-Augmented Generation (RAG)

---

## ✅ Real-Time Job Search
Fetches latest jobs using external APIs:
- Python jobs
- Full Stack jobs
- Django/FastAPI roles
- Location-based search

---

## ✅ AI Job Matching
Analyzes resume and suggests:
- Suitable job roles
- Required skills
- Career recommendations

---

# 🧠 Tech Stack

| Technology | Usage |
|---|---|
| Python | Core Language |
| FastAPI | Backend APIs |
| Streamlit | Frontend UI |
| Groq LLM | AI Responses |
| FAISS | Vector Search |
| Sentence Transformers | Embeddings |
| PyPDF2 | PDF Parsing |
| python-docx | DOCX Parsing |
| SerpAPI | Job Search API |

---

# 🏗️ System Architecture

```text
User Uploads Resume
        ↓
Text Extraction
        ↓
Chunking
        ↓
Embeddings Generation
        ↓
FAISS Vector Store
        ↓
User Query
        ↓
Top-K Semantic Retrieval
        ↓
Groq LLM
        ↓
AI Response
```

---

# 🔥 RAG Pipeline

This project uses **Retrieval-Augmented Generation (RAG)**:

1. Resume is split into chunks
2. Embeddings are generated
3. FAISS stores embeddings
4. Relevant chunks are retrieved
5. Context is sent to LLM
6. LLM generates accurate response

This improves:
- Context accuracy
- Response relevance
- Token efficiency

---

# 📸 Screenshots

## Home Page
<img width="1193" height="755" alt="image" src="https://github.com/user-attachments/assets/4f851916-713b-4933-baf0-5eede32947ef" />


## Resume Analysis
<img width="920" height="802" alt="image" src="https://github.com/user-attachments/assets/ce277282-278f-41dc-bdc6-0c39d679cef2" />


## ATS Score
<img width="926" height="802" alt="image" src="https://github.com/user-attachments/assets/92cd53a1-6bf5-40e3-8c3e-0f4f1127cb3d" />

## Job Search
<img width="990" height="828" alt="image" src="https://github.com/user-attachments/assets/dc61de13-c134-4b47-a8cc-7899a75acacb" />

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-job-copilot.git
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Add Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_key
SERPAPI_KEY=your_key
```

---

# ▶️ Run Backend

```bash
uvicorn main:app --reload
```

---

# ▶️ Run Frontend

```bash
streamlit run app.py
```

---

# 🚀 Future Improvements

- JWT Authentication
- Resume Tailoring based on Job Description
- Cloud Deployment
- Vector Database Integration (Pinecone/Weaviate)
- Docker Support
- AI Mock Interviews

---

# 📚 Key Learnings

- Retrieval-Augmented Generation (RAG)
- Vector Databases & Embeddings
- LLM Integration
- Prompt Engineering
- FastAPI Backend Development
- AI-powered Search Systems

---

# ⭐ If you liked this project

Give it a star ⭐ on GitHub!
