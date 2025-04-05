import streamlit as st
import requests
import speech_recognition as sr
import tempfile

# LanguageTool API endpoint
API_URL = "https://api.languagetool.org/v2/check"

# Grammar checker
def get_grammar_score(text):
    if not text.strip():
        return 0, []
    try:
        response = requests.post(API_URL, data={'text': text, 'language': 'en-US'})
        matches = response.json().get("matches", [])
        error_count = len(matches)
        word_count = len(text.split())
        score = max(0, 100 - (error_count / word_count) * 100) if word_count else 0
        suggestions = [m.get("message", "") for m in matches]
        return round(score, 2), suggestions
    except Exception as e:
        return 0, [f"API Error: {e}"]

# Transcribe audio to English text
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_file.flush()
        with sr.AudioFile(tmp_file.name) as source:
            audio = recognizer.record(source)
            try:
                # Force language to English
                return recognizer.recognize_google(audio, language="en-US")
            except sr.UnknownValueError:
                return "❗ Could not understand the audio."
            except sr.RequestError as e:
                return f"❗ Speech recognition error: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Grammar Scoring Engine", layout="centered")
st.title("📝 Grammar Scoring Engine")
st.markdown("Check grammar from typed or spoken input (WAV only)")

# --- Text Input ---
st.subheader("✍️ Type your sentence:")
user_text = st.text_area("Enter sentence:", height=150)

if st.button("Check Grammar (Text)"):
    score, suggestions = get_grammar_score(user_text)
    st.markdown(f"### 📊 Score: `{score}/100`")
    if suggestions:
        st.markdown("### 📌 Suggestions:")
        for s in suggestions:
            st.write(f"• {s}")
    else:
        st.success("✅ No grammar issues found.")

# --- Voice Input ---
st.subheader("🎤 Upload a voice note (WAV format only):")
audio_file = st.file_uploader("Choose a .wav file", type=["wav"])

if audio_file:
    with st.spinner("Transcribing to English..."):
        transcribed = transcribe_audio(audio_file)
        st.markdown(f"### 🗣️ Transcribed Text:\n`{transcribed}`")

        if not transcribed.startswith("❗"):
            score, suggestions = get_grammar_score(transcribed)
            st.markdown(f"### 📊 Score: `{score}/100`")
            if suggestions:
                st.markdown("### 📌 Suggestions:")
                for s in suggestions:
                    st.write(f"• {s}")
            else:
                st.success("✅ No grammar issues found.")
        else:
            st.error(transcribed)

st.caption("Built with 💙 using Streamlit + Google Speech Recognition + LanguageTool API")
