import streamlit as st
import pandas as pd
import requests

# Load CSV
df = pd.read_csv("Grammar Correction.csv")

# API Endpoint for LanguageTool
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

st.title("📝 Grammar Scoring Engine (Streamlit + API)")

for index, row in df.iterrows():
    original = row["Ungrammatical Statement"]
    corrected = row["Correct Sentence"]

    score, suggestions = get_grammar_score(original)

    with st.expander(f"🔸 Statement {index + 1}: {original}"):
        st.markdown(f"**Corrected Sentence:** {corrected}")
        st.markdown(f"**Grammar Score:** `{score}/100`")
        if suggestions:
            st.markdown("**Grammar Suggestions:**")
            for s in suggestions:
                st.write(f"• {s}")
        else:
            st.success("✅ No grammar issues found!")

st.markdown("---")
st.caption("Powered by LanguageTool Public API 🌐")
