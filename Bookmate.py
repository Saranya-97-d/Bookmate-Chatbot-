import pandas as pd
import streamlit as st
import google.generativeai as genai

# Set Gemini API Key
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

# Gemini querying function
def query_with_cag(context: str, query: str) -> str:
    prompt = f"Context:\n{context}\n\nQuery: {query}\nAnswer:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.title("📚 **BookMate - by BrandTech**")
st.markdown("### 🔍 **Ask Questions Related to Web Programming Books**")

# Load CSV
csv_url = "https://raw.githubusercontent.com/Saranya-97-d/Bookmate-Chatbot-/main/engineering_books_web_prog.csv"
df = load_csv_from_github(csv_url)

if df is not None:
    st.markdown("### 📖 **Books Data Preview**")
    st.dataframe(df.head(), use_container_width=True)

    # Display authors and topics line by line
    with st.expander("📌 **Book Authors & Topics**", expanded=True):
        if "Author" in df.columns:
            authors = df["Author"].dropna().unique()
            st.markdown("#### 👩‍🏫 **Authors:**")
            for author in authors:
                st.markdown(f"- {author}")
        
        if "Topics" in df.columns:
            topics = df["Topics"].dropna().unique()
            st.markdown("#### 🧠 **Topics:**")
            for topic in topics:
                st.markdown(f"- {topic}")

    # Convert dataframe to text for model
    csv_text = df.to_string(index=False)

    st.markdown("### ✍️ **Enter Your Question Below**")
    query = st.text_input("")

    if query:
        response = query_with_cag(csv_text, query)
        st.markdown("### 📬 **Answer:**")
        st.write(response)

        # Save history
        st.session_state.setdefault("qa_history", []).append((query, response))

    # Show Q&A History
    if "qa_history" in st.session_state:
        st.markdown("### 🕑 **Q&A History**")
        for i, (q, a) in enumerate(st.session_state.qa_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.markdown("---")
