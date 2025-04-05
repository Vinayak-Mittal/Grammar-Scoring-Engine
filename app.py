import streamlit as st
import requests
import speech_recognition as sr
import tempfile
from pydub import AudioSegment

# Grammar Scoring Function
API_URL = "https://api.languagetool.org/v2/check"

def get_grammar_score(text):
    if not text.strip():
        return 0, []
    data = {
        'text': text,
        'language': 'en-US'
    }
    try:
        response = requests.post(API_URL, data=data)
        result = response.json()
        matches = result.get("matches", [])
    except Exception as e:
        return 0, [f"Error: {e}"]

    error_count = len(matches)
    word_count = len(text.split())
    score = max(0, 100 - (error_count / word_count) * 100) if word_count else 0
    suggestions = [m.get("message", "") for m in matches]
    return round(score, 2), suggestions


# Speech-to-Text from Uploaded Audio
def transcribe_audio(file):
    r = sr.Recognizer()

    # Convert mp3 to wav if needed
    audio = AudioSegment.from_file(file)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        audio.export(tmp_wav.name, format="wav")
        with sr.AudioFile(tmp_wav.name) as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                return "Could not understand audio."
            except sr.RequestError:
                return "Speech recognition service is unavailable."


# ----------------- Streamlit UI -------------------
st.set_page_config(page_title="Grammar Scoring Engine", layout="centered")
st.title("📝 Grammar Scoring Engine")
st.markdown("Check your grammar from text or voice 🎙️")

# Text Input
st.markdown("## ✍️ Type your sentence")
user_input = st.text_area("Enter your sentence here:", height=150)

if st.button("Check Text Grammar"):
    score, suggestions = get_grammar_score(user_input)
    st.markdown(f"### 📊 Grammar Score: `{score}/100`")
    if suggestions:
        st.markdown("### 📌 Suggestions:")
        for s in suggestions:
            st.write(f"• {s}")
    else:
        st.success("🎉 No grammar issues found!")

st.markdown("---")

# Voice Input
st.markdown("## 🎤 Upload a Voice Note (MP3/WAV)")
uploaded_audio = st.file_uploader("Upload audio", type=['wav', 'mp3'])

if uploaded_audio is not None:
    with st.spinner("Transcribing audio..."):
        transcribed_text = transcribe_audio(uploaded_audio)
        st.markdown(f"### 🗣️ Transcribed Text:\n`{transcribed_text}`")
        score, suggestions = get_grammar_score(transcribed_text)
        st.markdown(f"### 📊 Grammar Score: `{score}/100`")
        if suggestions:
            st.markdown("### 📌 Suggestions:")
            for s in suggestions:
                st.write(f"• {s}")
        else:
            st.success("🎉 No grammar issues found!")

st.caption("Built with 💙 using Streamlit, SpeechRecognition & LanguageTool API")










































# import streamlit as st
# import pandas as pd
# import requests

# # LanguageTool Public API endpoint
# API_URL = "https://api.languagetool.org/v2/check"

# def get_grammar_score(text):
#     if not text.strip():
#         return 0, []
    
#     data = {
#         'text': text,
#         'language': 'en-US'
#     }

#     response = requests.post(API_URL, data=data)
#     result = response.json()

#     matches = result.get("matches", [])
#     error_count = len(matches)
#     word_count = len(text.split())
    
#     score = max(0, 100 - (error_count / word_count) * 100) if word_count else 0
#     suggestions = [m["message"] for m in matches]

#     return round(score, 2), suggestions

# # Streamlit App UI
# st.title("📝 Grammar Scoring Engine")

# st.markdown("### 🔹 Enter your sentence to get grammar score:")

# user_input = st.text_area("Type your sentence here:", height=150)

# if st.button("Check Grammar Score"):
#     score, suggestions = get_grammar_score(user_input)

#     st.markdown(f"### ✅ Grammar Score: `{score}/100`")

#     if suggestions:
#         st.markdown("### 📌 Suggestions:")
#         for s in suggestions:
#             st.write(f"• {s}")
#     else:
#         st.success("🎉 No grammar issues found!")

# st.markdown("---")
# st.markdown("You can also upload and score multiple sentences from a file below.")

# # Optionally: Process your dataset
# uploaded_file = st.file_uploader("Upload a CSV file with a column named 'Ungrammatical Statement'", type=['csv'])

# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     st.markdown("### 📊 Results from uploaded file:")
#     for index, row in df.iterrows():
#         statement = row.get("Ungrammatical Statement", "")
#         score, suggestions = get_grammar_score(statement)

#         with st.expander(f"🔸 Statement {index + 1}: {statement}"):
#             st.markdown(f"**Grammar Score:** `{score}/100`")
#             if suggestions:
#                 st.markdown("**Suggestions:**")
#                 for s in suggestions:
#                     st.write(f"• {s}")
#             else:
#                 st.success("✅ No grammar issues found.")
