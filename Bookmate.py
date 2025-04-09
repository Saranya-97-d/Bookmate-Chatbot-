import pandas as pd
import streamlit as st
import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key="AIzaSyD9ZPsFRIDK5oaXbZriD_Ib1CjGzV0mejk") 



# Load CSV from GitHub
@st.cache_data
def load_csv_from_github(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")
        return None

# Gemini query function
def query_with_cag(context: str, query: str) -> str:
    prompt = f"""
You are an intelligent assistant. Use the context of the books below to answer the question. 
Include author names and topics in your response where relevant. 
Structure the output in clean lines, and use bold text for headings.

Context:
{context}

Question:
{query}

Answer:"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.title("📚 **BookMate - by BrandTech**")
st.markdown("### 🔍 **Ask Anything About Web Programming Books**")

# Load CSV
csv_url = "https://raw.githubusercontent.com/Saranya-97-d/Bookmate-Chatbot-/main/engineering_books_web_prog.csv"
df = load_csv_from_github(csv_url)

if df is not None:
    st.markdown("### 📖 **Books Preview**")
    st.dataframe(df.head(), use_container_width=True)

    csv_text = df.to_string(index=False)

    query = st.text_input("### ✍️ **Enter your question below:**")

    if query:
        response = query_with_cag(csv_text, query)
        st.markdown("### 📬 **Answer:**")
        st.markdown(response)

        # Save Q&A history
        st.session_state.setdefault("qa_history", []).append((query, response))

    if "qa_history" in st.session_state:
        st.markdown("### 🕑 **Q&A History**")
        for i, (q, a) in enumerate(st.session_state.qa_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.markdown("---")
