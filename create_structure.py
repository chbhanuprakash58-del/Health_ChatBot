import os

# -------------------------------
# Folder structure
# -------------------------------
structure = {
    "backend": {
        "models": {},
        "utils": {},
    },
    "frontend": {},
}

def create_structure(base_path, tree):
    for name, subtree in tree.items():
        path = os.path.join(base_path, name)
        os.makedirs(path, exist_ok=True)
        create_structure(path, subtree)

create_structure(".", structure)

# -------------------------------
# Backend: FastAPI (app.py)
# -------------------------------
backend_app = """\
from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
import pickle
import io
from PyPDF2 import PdfReader

app = FastAPI()

# Load ML model (placeholder)
try:
    with open("backend/models/diabetes_model.pkl", "rb") as f:
        model = pickle.load(f)
except:
    model = None

class DiabetesInput(BaseModel):
    glucose: float
    bmi: float
    age: int
    bloodpressure: float

@app.get("/")
def home():
    return {"message": "Welcome to the AI Health Assistant API"}

@app.post("/predict_diabetes")
def predict_diabetes(data: DiabetesInput):
    if model is None:
        # Dummy result for now
        risk = (data.glucose * 0.2 + data.bmi * 0.3 + data.age * 0.1 + data.bloodpressure * 0.4) / 2
    else:
        features = [[data.glucose, data.bmi, data.age, data.bloodpressure]]
        risk = model.predict_proba(features)[0][1] * 100
    return {"risk_percentage": round(risk, 2)}

@app.post("/summarize_report")
async def summarize_report(file: UploadFile):
    pdf = PdfReader(io.BytesIO(await file.read()))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    summary = text[:400] + "..." if len(text) > 400 else text
    return {"summary": "Summary: " + summary}

@app.post("/chat")
def chat_with_ai(message: str = Form(...)):
    msg = message.lower()
    if "sugar" in msg or "glucose" in msg:
        return {"response": "Your symptoms may be linked to blood sugar levels. Please monitor and stay hydrated."}
    elif "tired" in msg or "fatigue" in msg:
        return {"response": "Feeling tired could be due to low energy or dehydration. Ensure proper nutrition and rest."}
    elif "diet" in msg:
        return {"response": "Include more fiber, vegetables, and reduce refined sugar intake."}
    else:
        return {"response": "I'm here to help. Please describe your symptoms or upload a report."}
"""

# -------------------------------
# Frontend: Streamlit App
# -------------------------------
frontend_app = """\
import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Health Assistant", page_icon="🩺")
st.title("🩺 AI Health Assistant Chatbot")

# ---------------- Chatbot ----------------
st.subheader("💬 Chat with Health Assistant")
user_input = st.text_input("Type your message:")
if st.button("Send"):
    res = requests.post(f"{FASTAPI_URL}/chat", data={"message": user_input})
    st.write("🤖:", res.json()["response"])

# ---------------- Diabetes Risk ----------------
st.subheader("📊 Diabetes Risk Prediction")
glucose = st.number_input("Glucose Level", min_value=0.0)
bmi = st.number_input("BMI", min_value=0.0)
age = st.number_input("Age", min_value=0)
bp = st.number_input("Blood Pressure", min_value=0.0)
if st.button("Predict Diabetes Risk"):
    payload = {"glucose": glucose, "bmi": bmi, "age": age, "bloodpressure": bp}
    res = requests.post(f"{FASTAPI_URL}/predict_diabetes", json=payload)
    st.success(f"Predicted Diabetes Risk: {res.json()['risk_percentage']}%")

# ---------------- Report Summarizer ----------------
st.subheader("📄 Upload Health Report (PDF)")
uploaded = st.file_uploader("Upload your health report", type=["pdf"])
if uploaded:
    res = requests.post(f"{FASTAPI_URL}/summarize_report", files={"file": uploaded})
    st.info(res.json()["summary"])
"""

# -------------------------------
# Other supporting files
# -------------------------------
requirements = """\
fastapi
uvicorn
streamlit
scikit-learn
pypdf2
requests
"""

readme = """\
# 🩺 AI Health Assistant Chatbot

This project combines **FastAPI (backend)** and **Streamlit (frontend)** to create a smart AI Health Chatbot that:
- Predicts diabetes risk
- Summarizes uploaded PDF health reports
- Answers health-related questions

### 🚀 Run Backend
```bash
uvicorn backend.app:app --reload
