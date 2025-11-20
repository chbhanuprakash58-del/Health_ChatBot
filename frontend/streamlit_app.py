# import streamlit as st
# import requests

# BACKEND_URL = "http://127.0.0.1:8000"

# st.set_page_config(page_title="🩺 HealthCare Chatbot", layout="centered")
# st.title("🩺 AI HealthCare Chatbot")
# st.write("Upload a health-related PDF and ask any question!")

# # -------------------- PDF Upload --------------------
# uploaded_file = st.file_uploader("Upload your health PDF", type=["pdf"])

# if uploaded_file:
#     st.success(f"✅ Uploaded: {uploaded_file.name}")
#     files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
#     with st.spinner("Uploading and processing..."):
#         try:
#             res = requests.post(f"{BACKEND_URL}/upload_pdf/", files=files)
#             if res.status_code == 200:
#                 st.success("✅ PDF uploaded successfully! You can now ask questions related to it.")
#             else:
#                 st.error(f"❌ Upload failed: {res.text}")
#         except Exception as e:
#             st.error(f"❌ Error: {e}")

# st.markdown("---")

# # -------------------- Chat Section --------------------
# st.subheader("💬 Ask your health-related question:")
# query = st.text_input("Enter your question")

# if st.button("Ask"):
#     if not query:
#         st.warning("Please enter a question.")
#     else:
#         with st.spinner("🤖 Thinking..."):
#             try:
#                 res = requests.post(f"{BACKEND_URL}/ask/", data={"message": query})
#                 if res.status_code == 200:
#                     answer = res.json().get("response", "No answer found.")
#                     st.success(f"🤖 Bot: {answer}")
#                 else:
#                     st.error(f"❌ Error: {res.text}")
#             except Exception as e:
#                 st.error(f"❌ Error: {e}")






import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="🩺 HealthCare Chatbot", layout="centered")
st.title("🩺 AI HealthCare Chatbot")
st.write("Upload your health report (PDF) and ask health-related questions!")

# -------------------- PDF Upload --------------------
uploaded_file = st.file_uploader("📄 Upload your health PDF", type=["pdf"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    with st.spinner("⏳ Uploading and reading your PDF..."):
        res = requests.post(f"{BACKEND_URL}/upload_pdf/", files=files)
        if res.status_code == 200:
            st.success("✅ PDF uploaded successfully! Now ask your questions below.")
        else:
            st.error(f"❌ Upload failed: {res.text}")

st.markdown("---")

# -------------------- Chat Section --------------------
st.subheader("💬 Ask your health-related question:")
query = st.text_input("Enter your question")

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("🤖 Thinking..."):
            res = requests.post(f"{BACKEND_URL}/ask/", data={"message": query})
            if res.status_code == 200:
                answer = res.json().get("answer", "⚠️ No answer found.")
                st.success(f"🤖 Bot: {answer}")
            else:
                st.error(f"❌ Error: {res.text}")
