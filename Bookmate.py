import streamlit as st
import pandas as pd
import google.generativeai as genai
import requests

# Configure Google Gemini API key
genai.configure(api_key="YOUR_API_KEY_HERE")  # Replace with st.secrets or secure method

# GitHub raw URL to CSV
csv_url = "https://raw.githubusercontent.com/Saranya-97-d/Bookmate-Chatbot-/main/engineering_books_web_prog.csv"

# Function to read CSV from GitHub
def read_csv_from_github(url):
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_csv(pd.compat.StringIO(response.text))
    return df

# Function to query Gemini LLM
def query_with_context(context: str, query: str) -> str:
    prompt = f"Context:\n{context}\n\nQuery: {query}\nAnswer:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit App
st.title("BookMate - by BrandTech")
st.header("Ask Questions Based on Engineering Book Data (CSV)")

# Load CSV and create context
try:
    df = read_csv_from_github(csv_url)
    csv_text = df.to_string(index=False)
    st.text_area("CSV Content Preview", value=csv_text[:1000], height=200)
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# Question input
query = st.text_input("Ask a question based on the book data:")

# Generate response
if query:
    response = query_with_context(csv_text, query)
    st.session_state.setdefault("qa_history", []).append((query, response))

    st.subheader("Answer:")
    st.write(response)

# Show Q&A history
if "qa_history" in st.session_state:
    st.subheader("Question & Answer History:")
    for i, (q, a) in enumerate(st.session_state.qa_history, 1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"**A{i}:** {a}")
        st.write("---")
