import pandas as pd
import streamlit as st
import google.generativeai as genai
import requests

# Configure Google Gemini API key (Use Streamlit secrets for security)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Function to load CSV from GitHub
@st.cache_data
def load_csv_from_github(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        return None

# Function to query Gemini LLM with context
def query_with_cag(context: str, query: str) -> str:
    """Query the Gemini LLM with preloaded context."""
    prompt = f"Context:\n{context}\n\nQuery: {query}\nAnswer:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.title("BookMate - by BrandTech")
st.header("Ask Questions related to Web Programming CSV")

csv_url = "https://raw.githubusercontent.com/Saranya-97-d/Bookmate-Chatbot-/main/engineering_books_web_prog.csv"
df = load_csv_from_github(csv_url)

if df is not None:
    st.dataframe(df.head())

    # Combine all rows as context (not scalable for very large files)
    csv_text = df.to_string(index=False)

    query = st.text_input("Ask a question based on the CSV content:")
    if query:
        response = query_with_cag(csv_text, query)
        st.subheader("Answer:")
        st.write(response)

        st.session_state.setdefault("qa_history", []).append((query, response))

    # Show history
    if "qa_history" in st.session_state:
        st.subheader("Q&A History")
        for i, (q, a) in enumerate(st.session_state.qa_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.write("---")
