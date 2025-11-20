🩺 AI HealthCare ChatBot

A FastAPI + Streamlit based AI medical report assistant that reads uploaded PDFs (including scanned reports using OCR), extracts important health information, and answers user questions using Groq’s LLaMA model.

🚀 Features
✅ 1. Upload Medical Reports (PDF)

Supports normal PDFs (with selectable text)

Supports scanned PDFs (image-based)

Uses:

pdfplumber for digital text extraction

Tesseract OCR for scanned images

pdf2image for PDF → Image conversion

✅ 2. Ask Health Questions

After uploading PDF, user can ask questions like:

“What does this blood report say?”

“Is my cholesterol high?”

“Explain my liver test results.”

✅ 3. Uses Groq LLaMA Model

Fast & accurate responses using:

llama-3.1-8b-instant


The backend sends:

Extracted OCR text

User’s question
to Groq API for a clear health explanation.

✅ 4. Frontend Built With Streamlit

Simple, clean UI

Upload PDF

Ask questions

See answers instantly

✅ 5. Backend Built With FastAPI

/upload_pdf/ → Upload & extract text

/ask/ → Ask question & get AI answer

CORS enabled for frontend communication

🧠 How It Works (Architecture)
Streamlit UI
    ↓ upload PDF
FastAPI Backend
    ↓ extract text using pdfplumber OR pytesseract
Save to uploaded_text.txt
    ↓ user asks question
Groq LLaMA Model
    ↓ analyze report + question
FastAPI returns answer
    ↓ show in Streamlit

🗂 Project Structure
Health_ChatBot/
│
├── backend/
│   ├── app.py                # FastAPI backend
│
├── frontend/
│   ├── app.py                # Streamlit frontend UI
│
├── uploaded_pdfs/            # Uploaded PDFs
├── uploaded_text.txt         # Extracted text storage
│
├── .env                      # API Key (Not in GitHub)
├── .gitignore
└── README.md

🔑 Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_api_key_here


⚠️ IMPORTANT
Your .env must not be pushed to GitHub.
Add this in .gitignore:

.env

🔧 Installation & Setup
1️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

2️⃣ Install Dependencies
pip install fastapi uvicorn streamlit requests pdfplumber pytesseract pdf2image groq python-dotenv

Install Tesseract (Windows)

Download and install:
https://github.com/UB-Mannheim/tesseract/wiki

Set path in backend:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

Install Poppler (for pdf2image)

Download:
https://github.com/oschwartz10612/poppler-windows/releases/

Add poppler /bin to PATH.

▶️ Running the Project
1️⃣ Start Backend (FastAPI)
uvicorn backend.app:app --reload


Backend runs at:

http://127.0.0.1:8000

2️⃣ Start Frontend (Streamlit)
streamlit run frontend/app.py


Open UI at:

http://localhost:8501

🙌 Credits

Built using:

FastAPI

Streamlit

Groq LLaMA

Tesseract OCR

pdfplumber

pdf2image