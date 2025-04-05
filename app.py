# app.py
import streamlit as st
import torch
import torchaudio
import torchaudio.transforms as T
import torch.nn as nn
import torch.nn.functional as F
import os

# Model definition
class AudioRegressor(nn.Module):
    def __init__(self, input_dim):
        super(AudioRegressor, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x.squeeze(1)

# Load model
@st.cache_resource
def load_model(path="trained_model.pth"):
    model = AudioRegressor(input_dim=40)
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    model.eval()
    return model

# Preprocess audio
def preprocess_audio(audio_bytes, sr=16000, n_mfcc=40):
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes.read())
    waveform, sample_rate = torchaudio.load("temp.wav")

    if sample_rate != sr:
        resampler = T.Resample(orig_freq=sample_rate, new_freq=sr)
        waveform = resampler(waveform)

    mfcc = T.MFCC(sample_rate=sr, n_mfcc=n_mfcc)(waveform)
    mfcc_mean = mfcc.mean(dim=0)  # shape: [n_mfcc]
    return mfcc_mean.unsqueeze(0)  # add batch dimension

# Streamlit UI
st.title("🗣 Grammar Scoring Engine")
st.markdown("Upload a .wav file (45–60 seconds) to get a grammar score between **0 and 5**.")

uploaded_file = st.file_uploader("Choose a .wav audio file", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    with st.spinner("Analyzing grammar..."):
        model = load_model()
        features = preprocess_audio(uploaded_file)
        with torch.no_grad():
            prediction = model(features)
        score = prediction.item()
        st.success(f"🎯 **Predicted Grammar Score:** {score:.2f}")


















# import streamlit as st
# import requests
# import speech_recognition as sr
# import tempfile

# # LanguageTool API endpoint
# API_URL = "https://api.languagetool.org/v2/check"

# # Grammar checker
# def get_grammar_score(text):
#     if not text.strip():
#         return 0, []
#     try:
#         response = requests.post(API_URL, data={'text': text, 'language': 'en-US'})
#         matches = response.json().get("matches", [])
#         error_count = len(matches)
#         word_count = len(text.split())
#         score = max(0, 100 - (error_count / word_count) * 100) if word_count else 0
#         suggestions = [m.get("message", "") for m in matches]
#         return round(score, 2), suggestions
#     except Exception as e:
#         return 0, [f"API Error: {e}"]

# # Transcribe audio to English text
# def transcribe_audio(audio_file):
#     recognizer = sr.Recognizer()
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
#         tmp_file.write(audio_file.read())
#         tmp_file.flush()
#         with sr.AudioFile(tmp_file.name) as source:
#             audio = recognizer.record(source)
#             try:
#                 # Force language to English
#                 return recognizer.recognize_google(audio, language="en-US")
#             except sr.UnknownValueError:
#                 return "❗ Could not understand the audio."
#             except sr.RequestError as e:
#                 return f"❗ Speech recognition error: {e}"

# # --- Streamlit UI ---
# st.set_page_config(page_title="Grammar Scoring Engine", layout="centered")
# st.title("📝 Grammar Scoring Engine")
# st.markdown("Check grammar from typed or spoken input (WAV only)")

# # --- Text Input ---
# st.subheader("✍️ Type your sentence:")
# user_text = st.text_area("Enter sentence:", height=150)

# if st.button("Check Grammar (Text)"):
#     score, suggestions = get_grammar_score(user_text)
#     st.markdown(f"### 📊 Score: `{score}/100`")
#     if suggestions:
#         st.markdown("### 📌 Suggestions:")
#         for s in suggestions:
#             st.write(f"• {s}")
#     else:
#         st.success("✅ No grammar issues found.")

# # --- Voice Input ---
# st.subheader("🎤 Upload a voice note (WAV format only):")
# audio_file = st.file_uploader("Choose a .wav file", type=["wav"])

# if audio_file:
#     with st.spinner("Transcribing to English..."):
#         transcribed = transcribe_audio(audio_file)
#         st.markdown(f"### 🗣️ Transcribed Text:\n`{transcribed}`")

#         if not transcribed.startswith("❗"):
#             score, suggestions = get_grammar_score(transcribed)
#             st.markdown(f"### 📊 Score: `{score}/100`")
#             if suggestions:
#                 st.markdown("### 📌 Suggestions:")
#                 for s in suggestions:
#                     st.write(f"• {s}")
#             else:
#                 st.success("✅ No grammar issues found.")
#         else:
#             st.error(transcribed)

# st.caption("Built with 💙 using Streamlit + Google Speech Recognition + LanguageTool API")
