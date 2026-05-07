import streamlit as st
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Job Copilot",
    layout="centered"
)

# =========================
# CLEAN DARK STYLE
# =========================
st.markdown("""
<style>
.block-container {
    max-width: 750px;
    padding-top: 2rem;
}

h1 {
    text-align: center;
    font-weight: 500;
}

.stChatMessage {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("AI Job Copilot")
st.caption("Upload your resume and interact with it using AI")

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_data" not in st.session_state:
    st.session_state.file_data = None
# =========================
# FILE UPLOAD + ACTION BUTTONS
# =========================
file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

col1, col2, col3 = st.columns(3)

# =========================
# ANALYZE
# =========================
if file and col1.button("Analyze Resume"):

    with st.spinner("Analyzing resume..."):

        response = requests.post(
            "http://127.0.0.1:8000/upload-resume",
            files={"file": (file.name, file, file.type)}
        )

        if response.status_code == 200:
            data = response.json()

            st.session_state.file_data = file.getvalue()
            st.session_state.file_name = file.name
            st.session_state.file_type = file.type

            st.session_state.messages.append({
                "role": "assistant",
                "content": data.get("analysis", "No response")
            })

st.divider()
st.subheader("🔍 Find Jobs")

job_role = st.text_input("Enter role (e.g. Python Developer)")

if st.button("Find Jobs"):

    response = requests.get(
        "http://127.0.0.1:8000/find-jobs",
        params={"role": job_role}
    )

    if response.status_code == 200:
        data = response.json()

        for job in data.get("jobs", []):
            st.markdown(f"""
            **{job['title']}**  
            {job['company']} • {job['location']}  
            [Apply Here]({job['link']})
            """)
            st.markdown("---")

    else:
        st.error("Failed to fetch jobs")
# =========================
# ATS SCORE
# =========================
if file and col2.button("ATS Score"):

    with st.spinner("Calculating ATS score..."):

        response = requests.post(
            "http://127.0.0.1:8000/ats-score",
            files={"file": (file.name, file, file.type)}
        )

        if response.status_code == 200:
            data = response.json()

            st.session_state.messages.append({
                "role": "assistant",
                "content": data.get("ats", "No response")
            })


# =========================
# JOB MATCHING
# =========================
if file and col3.button("Find Jobs"):

    with st.spinner("Finding jobs..."):

        response = requests.post(
            "http://127.0.0.1:8000/job-matches",
            files={"file": (file.name, file, file.type)}
        )

        if response.status_code == 200:
            data = response.json()

            # st.session_state.messages.append({
            #     "role": "assistant",
            #     "content": data.get("jobs", "No response")
            # })
            st.write(data)

# =========================
# CHAT DISPLAY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# CHAT INPUT (BOTTOM like ChatGPT)
# =========================
if st.session_state.file_data:

    prompt = st.chat_input("Ask something about your resume...")

    if prompt:

        # user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    params={"question": prompt},
                    files={
                        "file": (
                            st.session_state.file_name,
                            st.session_state.file_data,
                            st.session_state.file_type
                        )
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No response")

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                else:
                    st.error("API error")