# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from PyPDF2 import PdfReader
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# # ------------------- CORS -------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------- GLOBAL VARIABLES -------------------
# TEMP_FILE_PATH = "uploaded_text.txt"
# GROK_API_KEY = os.getenv("GROK_API_KEY")
# GROK_API_URL = os.getenv("GROK_API_URL", "https://api.x.ai/v1/chat/completions")

# # ------------------- ROUTES -------------------
# @app.get("/")
# def root():
#     return {"message": "AI HealthCare Chatbot Backend Running Successfully"}

# # ---------- UPLOAD PDF ----------
# @app.post("/upload_pdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     try:
#         pdf_reader = PdfReader(file.file)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text() or ""

#         text = text.strip()
#         if text:
#             with open(TEMP_FILE_PATH, "w", encoding="utf-8") as f:
#                 f.write(text)
#             return {"message": "PDF uploaded and text extracted successfully"}
#         else:
#             return {"message": "PDF uploaded but no text extracted"}
#     except Exception as e:
#         return {"error": str(e)}

# # ---------- ASK QUESTION ----------
# @app.post("/ask/")
# async def ask_question(message: str = Form(...)):
#     if not os.path.exists(TEMP_FILE_PATH):
#         return {"response": "Please upload a PDF first."}

#     with open(TEMP_FILE_PATH, "r", encoding="utf-8") as f:
#         uploaded_text = f.read()

#     if not uploaded_text:
#         return {"response": "Uploaded PDF is empty or not processed."}

#     prompt = f"You are a medical expert. The user uploaded this medical report:\n\n{uploaded_text}\n\nQuestion: {message}\n\nGive a clear, short, and helpful answer."

#     headers = {
#         "Authorization": f"Bearer {GROK_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "grok-beta",
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": 0.5
#     }

#     try:
#         response = requests.post(GROK_API_URL, headers=headers, json=data)
#         if response.status_code == 200:
#             result = response.json()
#             ai_reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
#             return {"response": ai_reply or "No response from Grok."}
#         else:
#             return {"response": f"Error: {response.text}"}
#     except Exception as e:
#         return {"response": f"Request failed: {e}"}


###########################################################################

# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import fitz  # PyMuPDF
# import os
# import requests
# from dotenv import load_dotenv

# ------------------- LOAD ENV -------------------
# load_dotenv()

# app = FastAPI()

# # ------------------- CORS -------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------- GLOBAL VARIABLES -------------------
# GROK_API_KEY = os.getenv("GROK_API_KEY") or "YOUR_GROK_API_KEY_HERE"
# GROK_API_URL = "https://api.x.ai/v1/chat/completions"
# UPLOAD_FILE_PATH = os.path.join(os.path.dirname(__file__), "uploaded_text.txt")

# # ------------------- ROUTES -------------------

# @app.get("/")
# def root():
#     return {"message": "✅ AI HealthCare Chatbot Backend Running Successfully"}


# @app.post("/upload_pdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     """Extract text from uploaded PDF and save to uploaded_text.txt"""
#     try:
#         pdf_path = os.path.join(os.path.dirname(__file__), file.filename)

#         # Save the uploaded PDF temporarily
#         with open(pdf_path, "wb") as f:
#             f.write(await file.read())

#         # Extract text using PyMuPDF
#         text = ""
#         with fitz.open(pdf_path) as doc:
#             for page in doc:
#                 text += page.get_text("text")

#         # Clean up temporary file
#         os.remove(pdf_path)

#         # Save extracted text to a file
#         with open(UPLOAD_FILE_PATH, "w", encoding="utf-8") as f:
#             f.write(text)

#         print("✅ Extracted text saved to:", UPLOAD_FILE_PATH)
#         print("📄 Text Preview:", text[:300])  # first 300 chars

#         if len(text.strip()) == 0:
#             return {"message": "⚠️ No readable text found in the PDF."}

    #     return {"message": "✅ PDF uploaded and text extracted successfully!"}

    # except Exception as e:
    #     print("❌ PDF processing error:", str(e))
    #     return {"error": f"PDF processing failed: {str(e)}"}




# @app.post("/ask/")
# async def ask_question(message: str = Form(...)):
#     """Answer health questions based on extracted text using Grok API."""
#     try:
#         print("\n🚀 Received question:", message)

#         if not os.path.exists(UPLOAD_FILE_PATH):
#             print("⚠️ No uploaded text file found.")
#             return {"error": "⚠️ Please upload a PDF first."}

#         with open(UPLOAD_FILE_PATH, "r", encoding="utf-8") as f:
#             context = f.read()

#         if not context.strip():
#             print("⚠️ Extracted text is empty.")
#             return {"error": "⚠️ Uploaded PDF text is empty."}

#         prompt = f"Here is a health report:\n\n{context}\n\nQuestion: {message}\nAnswer clearly and in simple terms."

#         headers = {
#             "Authorization": f"Bearer {GROK_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "model": "grok-beta",
#             "messages": [
#                 {"role": "system", "content": "You are a helpful health assistant that analyzes medical reports."},
#                 {"role": "user", "content": prompt}
#             ]
#         }

#         print("📡 Sending request to GROK API...")
#         print("🔑 URL:", GROK_API_URL)
#         print("🧾 Payload:", payload)

#         response = requests.post(GROK_API_URL, headers=headers, json=payload)

#         print("\n==================== GROK DEBUG ====================")
#         print("🔹 STATUS CODE:", response.status_code)
#         print("🔹 RAW TEXT RESPONSE:\n", response.text)
#         print("====================================================\n")

#         if response.status_code != 200:
#             return {"error": f"API error: {response.text}"}

#         data = response.json()

#         ai_response = None
#         if "choices" in data:
#             ai_response = (
#                 data["choices"][0].get("message", {}).get("content")
#                 or data["choices"][0].get("text")
#             )
#         elif "output" in data:
#             ai_response = data["output"]
#         elif "response" in data:
#             ai_response = data["response"]

#         if not ai_response:
#             return {"response": "🤖 No answer found."}

#         print("✅ Parsed AI Response:", ai_response)
#         return {"response": ai_response.strip()}

#     except Exception as e:
#         print("❌ Error while answering:", str(e))
#         return {"error": f"Internal server error: {str(e)}"}





###############################################




# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import os
# import requests
# import pdfplumber
# import pytesseract
# from pdf2image import convert_from_path

# # ------------------- APP CONFIG -------------------
# app = FastAPI()
# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------- GLOBAL VARIABLES -------------------
# GROK_API_KEY = os.getenv("GROK_API_KEY") or "YOUR_GROK_API_KEY_HERE"
# GROK_API_URL = os.getenv("GROK_API_URL") or "https://api.x.ai/v1/chat/completions"
# UPLOAD_FOLDER = "uploaded_pdfs"
# TEXT_FILE_PATH = "uploaded_text.txt"

# # 👇 If you’re on Windows, set the Tesseract path here

# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\aravi\Documents\tesseract.exe"

# # ------------------- ROUTES -------------------
# @app.get("/")
# def root():
#     return {"message": "✅ AI HealthCare Chatbot Backend Running Successfully"}


# # ------------------- UPLOAD PDF ROUTE -------------------
# @app.post("/upload_pdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     # Save uploaded PDF
#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     # Step 1: Try extracting text normally
#     extracted_text = ""
#     try:
#         with pdfplumber.open(file_path) as pdf:
#             for page in pdf.pages:
#                 text = page.extract_text()
#                 print("text+3445",text)
#                 if text:
#                     extracted_text += text
#     except Exception as e:
#         print(f"Error during pdfplumber extraction: {e}")

#     # Step 2: If no text found → perform OCR
#     if not extracted_text.strip():
#         try:
#             pages = convert_from_path(file_path, 300)
#             for page in pages:
#                 extracted_text += pytesseract.image_to_string(page)
#         except Exception as e:
#             print(f"Error during OCR extraction: {e}")

#     # Step 3: Save extracted text
#     with open(TEXT_FILE_PATH, "w", encoding="utf-8") as f:
#         f.write(extracted_text)

#     # Step 4: Return response
#     if not extracted_text.strip():
#         return {"message": "⚠️ No readable text found. Try uploading a clearer scan."}

#     print(f"✅ Extracted text saved to: {os.path.abspath(TEXT_FILE_PATH)}")
#     print(f"📄 Text Preview (first 300 chars): {extracted_text[:300]}")

#     return {"message": "✅ PDF uploaded and text extracted successfully!"}


# # ------------------- ASK QUESTION ROUTE -------------------
# @app.post("/ask/")
# async def ask_question(message: str = Form(...)):
#     print(f"\n🚀 Received question: {message}")

#     # Load extracted text
#     if not os.path.exists(TEXT_FILE_PATH):
#         return {"answer": "⚠️ Please upload a PDF first."}

#     with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
#         extracted_text = f.read()

#     if not extracted_text.strip():
#         return {"answer": "⚠️ Uploaded PDF had no readable text."}

#     # Combine extracted text + question
#     prompt = f"Here is a medical report:\n{extracted_text}\n\nQuestion: {message}\nAnswer in simple terms:"

#     # Prepare request to Grok API
#     headers = {
#         "Authorization": f"Bearer {GROK_API_KEY}",
#         "Content-Type": "application/json",
#     }
#     data = {
#         "model": "grok-beta",
#         "messages": [{"role": "user", "content": prompt}],
#     }

#     try:
#         response = requests.post(GROK_API_URL, headers=headers, json=data)
#         response_data = response.json()
#         print("🧠 Grok API Response:", response_data)

#         answer = (
#             response_data.get("choices", [{}])[0]
#             .get("message", {})
#             .get("content", "No answer found.")
#         )

#         return {"answer": answer}

#     except Exception as e:
#         print(f"❌ Error calling Grok API: {e}")
#         return {"answer": f"❌ Error: {e}"}




# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import os
# import pdfplumber
# import pytesseract
# from pdf2image import convert_from_path
# from groq import Groq

# # ------------------- APP CONFIG -------------------
# app = FastAPI()
# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------- GLOBAL VARIABLES -------------------
# GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "YOUR_GROQ_API_KEY_HERE"
# client = Groq(api_key=GROQ_API_KEY)

# UPLOAD_FOLDER = "uploaded_pdfs"
# TEXT_FILE_PATH = "uploaded_text.txt"

# # 👇 If you’re on Windows, set the Tesseract path here
# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\aravi\Documents\tesseract.exe"


# # ------------------- ROUTES -------------------
# @app.get("/")
# def root():
#     return {"message": "✅ AI HealthCare Chatbot Backend Running Successfully"}


# # ------------------- UPLOAD PDF -------------------
# @app.post("/upload_pdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     # Save uploaded PDF
#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     # Step 1: Try extracting text normally
#     extracted_text = ""
#     try:
#         with pdfplumber.open(file_path) as pdf:
#             for page in pdf.pages:
#                 text = page.extract_text()
#                 if text:
#                     extracted_text += text
#     except Exception as e:
#         print(f"Error during pdfplumber extraction: {e}")

#     # Step 2: If no text found → perform OCR
#     if not extracted_text.strip():
#         try:
#             pages = convert_from_path(file_path, 300)
#             for page in pages:
#                 extracted_text += pytesseract.image_to_string(page)
#         except Exception as e:
#             print(f"Error during OCR extraction: {e}")

#     # Step 3: Save extracted text
#     with open(TEXT_FILE_PATH, "w", encoding="utf-8") as f:
#         f.write(extracted_text)

#     if not extracted_text.strip():
#         return {"message": "⚠️ No readable text found. Try uploading a clearer scan."}

#     print(f"✅ Extracted text saved to: {os.path.abspath(TEXT_FILE_PATH)}")
#     print(f"📄 Text Preview (first 300 chars): {extracted_text[:300]}")

#     return {"message": "✅ PDF uploaded and text extracted successfully!"}


# # ------------------- ASK QUESTION -------------------
# @app.post("/ask/")
# async def ask_question(message: str = Form(...)):
#     print(f"\n🚀 Received question: {message}")

#     # Load extracted text
#     if not os.path.exists(TEXT_FILE_PATH):
#         return {"answer": "⚠️ Please upload a PDF first."}

#     with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
#         extracted_text = f.read()

#     if not extracted_text.strip():
#         return {"answer": "⚠️ Uploaded PDF had no readable text."}

#     # Build prompt
#     prompt = f"""
#     You are a medical assistant. Analyze the following health report
#     and answer the user's question clearly and simply.

#     Health Report:
#     {extracted_text}

#     Question:
#     {message}
#     """

#     try:
#         # Ask Groq
#         response = client.chat.completions.create(
#             model="llama-3.1-70b-versatile",
#             messages=[
#                 {"role": "system", "content": "You are a helpful medical assistant."},
#                 {"role": "user", "content": prompt},
#             ],
#         )

#         answer = response.choices[0].message.content
#         return {"answer": answer}

#     except Exception as e:
#         print(f"❌ Error calling Groq API: {e}")
#         return {"answer": f"❌ Error: {e}"}



from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os   
import requests
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from groq import Groq
from dotenv import load_dotenv
load_dotenv()  # Load .env file


# ------------------- APP CONFIG -------------------
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- GLOBAL VARIABLES -------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

UPLOAD_FOLDER = "uploaded_pdfs"
TEXT_FILE_PATH = "uploaded_text.txt"

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


# 👇 If you’re on Windows, set the Tesseract path here
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\aravi\Documents\tesseract.exe"


# ------------------- ROUTES -------------------
@app.get("/")
def root():
    return {"message": "✅ AI HealthCare Chatbot Backend Running Successfully"}


# ------------------- UPLOAD PDF ROUTE -------------------
@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded PDF
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step 1: Try extracting text normally
    extracted_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text
    except Exception as e:
        print(f"Error during pdfplumber extraction: {e}")

    # Step 2: If no text found → perform OCR
    if not extracted_text.strip():
        try:
            pages = convert_from_path(file_path, 300)
            for page in pages:
                extracted_text += pytesseract.image_to_string(page)
        except Exception as e:
            print(f"Error during OCR extraction: {e}")

    # Step 3: Save extracted text
    with open(TEXT_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    # Step 4: Return response
    if not extracted_text.strip():
        return {"message": "⚠️ No readable text found. Try uploading a clearer scan."}

    print(f"✅ Extracted text saved to: {os.path.abspath(TEXT_FILE_PATH)}")
    print(f"📄 Text Preview (first 300 chars): {extracted_text[:300]}")

    return {"message": "✅ PDF uploaded and text extracted successfully!"}


# ------------------- ASK QUESTION ROUTE -------------------
@app.post("/ask/")
async def ask_question(message: str = Form(...)):
    print(f"\n🚀 Received question: {message}")

    # Load extracted text
    if not os.path.exists(TEXT_FILE_PATH):
        return {"answer": "⚠️ Please upload a PDF first."}

    with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
        extracted_text = f.read()

    if not extracted_text.strip():
        return {"answer": "⚠️ Uploaded PDF had no readable text."}

    # Combine extracted text + user question
    prompt = f"Here is a medical report:\n\n{extracted_text}\n\nQuestion: {message}\nAnswer clearly in simple health terms:"

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ UPDATED MODEL
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert medical assistant that analyzes health reports and explains results clearly.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        answer = completion.choices[0].message.content.strip()
        return {"answer": answer}

    except Exception as e:
        print(f"❌ Error calling Groq API: {e}")
        return {"answer": f"Error processing your request: {e}"}
