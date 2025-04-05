import streamlit as st
import pandas as pd
import language_tool_python

# Load the grammar correction tool
tool = language_tool_python.LanguageTool('en-US')

# Load your dataset
df = pd.read_csv("Grammar Correction.csv")

def score_grammar(statement):
    matches = tool.check(statement)
    error_count = len(matches)
    word_count = len(statement.split())
    score = max(0, 100 - (error_count / word_count) * 100) if word_count else 0
    suggestions = [match.message for match in matches]
    return round(score, 2), suggestions

st.title("📝 Grammar Scoring Engine")

st.markdown("This app scores the grammar quality of ungrammatical statements from your dataset.")

# Display each result
for index, row in df.iterrows():
    original = row['Ungrammatical Statement']
    corrected = row['Correct Sentence']
    
    score, suggestions = score_grammar(original)

    with st.expander(f"🔹 Statement {index + 1}: {original}"):
        st.markdown(f"**Corrected Sentence:** {corrected}")
        st.markdown(f"**Grammar Score:** `{score}/100`")
        if suggestions:
            st.markdown("**Suggestions:**")
            for s in suggestions:
                st.write(f"• {s}")
        else:
            st.success("✅ No grammar issues found!")

st.markdown("---")
st.caption("Developed for Grammar Correction Test - Streamlit Deployment")
