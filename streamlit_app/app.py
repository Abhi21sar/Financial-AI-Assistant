import streamlit as st
import requests
import os

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8000")

st.set_page_config(page_title="Multi-Agent Finance Assistant", layout="centered")
st.title("📈🗣️ Morning Market Brief (Voice + Text Assistant)")

st.markdown("Ask your question by **typing** or **uploading your voice**.")

# TEXT INPUT SECTION
with st.form("text_query_form"):
    query = st.text_input("Ask a question:", placeholder="e.g. What’s our risk exposure in Asia tech stocks today?")
    submit_text = st.form_submit_button("Submit (Text)")

if submit_text and query:
    with st.spinner("Thinking..."):
        try:
            resp = requests.post(f"{ORCHESTRATOR_URL}/ask_text", json={"text": query})
            st.write("🔍 Raw response from orchestrator:", resp.text)
            data = resp.json()

            st.markdown(f"**Response:** {data['response_text']}")

            audio_path = data.get("audio_file")
            if audio_path and os.path.exists(audio_path):
                audio_bytes = open(audio_path, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.warning(f"⚠️ Audio file not found: {audio_path}")

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.write("🔍 Raw response (text):", getattr(resp, "text", "No response"))


# AUDIO UPLOAD SECTION
st.markdown("---")
st.markdown("### 🎙️ Or upload your voice:")

audio_file = st.file_uploader("Upload .wav file", type=["wav"])
if audio_file and st.button("Submit (Voice)"):
    with st.spinner("Transcribing and thinking..."):
        try:
            resp = requests.post(
                f"{ORCHESTRATOR_URL}/ask_audio",
                files={"file": (audio_file.name, audio_file, "audio/wav")}
            )
            st.write("🔍 Raw response from orchestrator:", resp.text)
            data = resp.json()

            st.markdown(f"**Transcribed Query**: {data['query']}")
            st.markdown(f"**Response**: {data['response_text']}")

            audio_path = data.get("audio_file")
            if audio_path and os.path.exists(audio_path):
                audio_bytes = open(audio_path, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.warning(f"⚠️ Audio file not found: {audio_path}")

        except Exception as e:
            st.error(f"❌ Error during voice submission: {e}")
            st.write("🔍 Raw response (text):", getattr(resp, "text", "No response"))
