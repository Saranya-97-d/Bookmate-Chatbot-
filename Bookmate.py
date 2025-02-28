import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Google Gemini API key (Use Streamlit secrets for security)
genai.configure(api_key="YOUR_GOOGLE_GEMINI_API_KEY")

# Function to read the PDF file
def read_pdf(file_path):
    """Reads the text from a PDF file."""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = "".join(page.extract_text() or "" for page in reader.pages)
    return text

# Function to query Gemini LLM with context
def query_with_cag(context: str, query: str) -> str:
    """Query the Gemini LLM with preloaded context."""
    prompt = f"Context:\n{context}\n\nQuery: {query}\nAnswer:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit app interface
st.title("BookMate - by BrandTech")
st.header("Ask Questions Based on a Default PDF")

# Path to default PDF ()
default_pdf_path = "C:\Users\dalin\Downloads\engineering_books.pdf"

# Initialize session state for PDF processing
if "pdf_text" not in st.session_state:
    if os.path.exists():
        st.session_state.pdf_text = read_pdf(default_pdf_path)
    else:
        st.error("Default PDF file not found. Please check the file path.")
        st.stop()  # Stop execution if the file is missing

# Display PDF content preview if available
if st.session_state.pdf_text:
    st.text_area("PDF Content Preview", value=st.session_state.pdf_text[:1000], height=150)

    # User question input
    query = st.text_input("Ask a question based on the PDF:")

    if query:
        response = query_with_cag(st.session_state.pdf_text, query)
        st.session_state.setdefault("qa_history", []).append((query, response))

        st.subheader("Answer:")
        st.write(response)

    # Display previous Q&A history
    if "qa_history" in st.session_state and st.session_state.qa_history:
        st.subheader("Question & Answer History:")
        for i, (q, a) in enumerate(st.session_state.qa_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.write("---")  # Separator
