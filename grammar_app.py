import streamlit as st
import pandas as pd
import nltk
nltk.download('punkt')
from nltk.metrics import edit_distance
# Grammar scoring function
def grammar_score_edit_distance(original, corrected):
    distance = edit_distance(str(original), str(corrected))
    max_len = max(len(original), len(corrected))
    if max_len == 0: return 100.0
    score = (1 - distance / max_len) * 100
    return round(score, 2)

def interpret_score(score):
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Fair"
    elif score >= 40:
        return "Poor"
    else:
        return "Very Poor"

# App UI
st.title("Grammar Scoring Engine")
st.markdown("Upload a dataset or input sentences manually to get grammar scores.")

# Option 1: Upload CSV
st.header("Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(Grammar Correction.csv)
    if "Incorrect Sentence" in df.columns and "Correct Sentence" in df.columns:
        df["Grammar_Score"] = df.apply(
            lambda row: grammar_score_edit_distance(row["Incorrect Sentence"], row["Correct Sentence"]), axis=1
        )
        df["Grammar_Category"] = df["Grammar_Score"].apply(interpret_score)
        st.success("Scoring complete!")
        st.dataframe(df[["Incorrect Sentence", "Correct Sentence", "Grammar_Score", "Grammar_Category"]])
        st.download_button("Download Scored CSV", df.to_csv(index=False), "scored_grammar.csv", "text/csv")
    else:
        st.error("CSV must contain 'Incorrect Sentence' and 'Correct Sentence' columns.")

# Option 2: Manual Input
st.header("Try it Manually")
incorrect = st.text_input("Enter the sentence with grammar issues:")
corrected = st.text_input("Enter the corrected sentence:")

if st.button("Score Sentence"):
    if incorrect and corrected:
        score = grammar_score_edit_distance(incorrect, corrected)
        category = interpret_score(score)
        st.write(f"**Grammar Score:** {score}")
        st.write(f"**Category:** {category}")
    else:
        st.warning("Please enter both sentences.")
