import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Google Gemini API key (Use Streamlit secrets for security)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to read the PDF file
def read_pdf(file_path):
    """Reads the text from a PDF file."""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = "".join(page.extract_text() or "" for page in reader.pages)
    return text

# Function to query Gemini LLM with CAG
def query_with_cag(context: str, query: str) -> str:
    """Query the Gemini LLM with preloaded context."""
    prompt = f"Context:\n{context}\n\nQuery: {query}\nAnswer:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit app interface
st.title("RAG Application with Google Gemini - by Nirmal Gaud")
st.header("Upload a PDF and Ask Multiple Questions")

# Session state for file upload and storing Q&A history
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
    st.session_state.pdf_text = None
    st.session_state.qa_history = []  # Store Q&A pairs

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Ensure the directory exists
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    # Save uploaded file
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text from PDF
    pdf_text = read_pdf(temp_file_path)
    st.session_state.uploaded_file = uploaded_file
    st.session_state.pdf_text = pdf_text

    # Display PDF content preview
    st.text_area("PDF Content Preview", value=pdf_text[:1000], height=150)

    # User question input
    query = st.text_input("Ask a question based on the PDF:")

    if query:
        response = query_with_cag(st.session_state.pdf_text, query)
        st.session_state.qa_history.append((query, response))  # Store question-answer pair

    # Display previous questions and answers
    if st.session_state.qa_history:
        st.subheader("Question & Answer History:")
        for i, (q, a) in enumerate(st.session_state.qa_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.write("---")  # Separator
