import pandas as pd
import streamlit as st
import google.generativeai as genai

# Set Gemini API Key (replace this with your actual key for testing)
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
st.title("📚 BookMate - by BrandTech")
st.header("🔍 Ask Questions Related to Web Programming Books")

# Load CSV
csv_url = "https://raw.githubusercontent.com/Saranya-97-d/Bookmate-Chatbot-/main/engineering_books_web_prog.csv"
df = load_csv_from_github(csv_url)

if df is not None:
    st.subheader("Books Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Show unique authors and topics
    with st.expander("📌 Book Authors & Topics"):
        if "Author" in df.columns:
            authors = df["Author"].dropna().unique()
            st.markdown("**👩‍🏫 Authors:**")
            st.write(", ".join(authors))
        if "Topics" in df.columns:
            topics = df["Topics"].dropna().unique()
            st.markdown("**🧠 Topics:**")
            st.write(", ".join(topics))

    # Build context and ask Gemini
    csv_text = df.to_string(index=False)

    query = st.text_input("Ask a question based on the CSV content:")
    if query:
        response = query_with_cag(csv_text, query)
        st.subheader("📖 Answer:")
        st.write(response)

        st.session_state.setdefault("qa_history", []).append((query, response))

    # History
    if "qa_history" in st.session_state:
        st.subheader("🕑 Q&A History")
        for i, (q, a) in enumerate(st.session_state.qa_history, 1):
            st.markdown(f"**Q{i}:** {q}")
            st.markdown(f"**A{i}:** {a}")
            st.write("---")
