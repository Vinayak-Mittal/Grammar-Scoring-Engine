import streamlit as st
import pandas as pd
import requests

# LanguageTool Public API endpoint
API_URL = "https://api.languagetool.org/v2/check"

def get_grammar_score(text):
    if not text.strip():
        return 0, []
    
    data = {
        'text': text,
        'language': 'en-US'
    }

    response = requests.post(API_URL, data=data)
    result = response.json()

    matches = result.get("matches", [])
    error_count = len(matches)
    word_count = len(text.split())
    
    score = max(0, 100 - (error_count / word_count) * 100) if word_count else 0
    suggestions = [m["message"] for m in matches]

    return round(score, 2), suggestions

# Streamlit App UI
st.title("📝 Grammar Scoring Engine")

st.markdown("### 🔹 Enter your sentence to get grammar score:")

user_input = st.text_area("Type your sentence here:", height=150)

if st.button("Check Grammar Score"):
    score, suggestions = get_grammar_score(user_input)

    st.markdown(f"### ✅ Grammar Score: `{score}/100`")

    if suggestions:
        st.markdown("### 📌 Suggestions:")
        for s in suggestions:
            st.write(f"• {s}")
    else:
        st.success("🎉 No grammar issues found!")

st.markdown("---")
st.markdown("You can also upload and score multiple sentences from a file below.")

# Optionally: Process your dataset
uploaded_file = st.file_uploader("Upload a CSV file with a column named 'Ungrammatical Statement'", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.markdown("### 📊 Results from uploaded file:")
    for index, row in df.iterrows():
        statement = row.get("Ungrammatical Statement", "")
        score, suggestions = get_grammar_score(statement)

        with st.expander(f"🔸 Statement {index + 1}: {statement}"):
            st.markdown(f"**Grammar Score:** `{score}/100`")
            if suggestions:
                st.markdown("**Suggestions:**")
                for s in suggestions:
                    st.write(f"• {s}")
            else:
                st.success("✅ No grammar issues found.")
