from fastapi import FastAPI, UploadFile, File, Body
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Service URLs
RETRIEVAL_URL = os.getenv("RETRIEVAL_AGENT_URL", "http://retrieval_agent:8003")
LLM_URL = os.getenv("LLM_AGENT_URL", "http://llm_agent:8004")
VOICE_URL = os.getenv("VOICE_AGENT_URL", "http://localhost:8005")


@app.get("/")
def root():
    return {"message": "Orchestrator is running"}


@app.post("/ask_audio")
async def ask_from_audio(file: UploadFile = File(...)):
    # Step 1: Transcribe
    transcript_resp = requests.post(f"{VOICE_URL}/transcribe", files={"file": file.file})
    query = transcript_resp.json().get("transcript")

    # Step 2: Retrieve
    retrieval_resp = requests.get(f"{RETRIEVAL_URL}/query", params={"query": query, "k": 3})
    context_docs = retrieval_resp.json().get("results", [])

    # Step 3: LLM generation
    llm_resp = requests.post(f"{LLM_URL}/generate_brief", json={"question": query, "context_docs": context_docs})
    response_text = llm_resp.json().get("brief")

    # Step 4: Text-to-Speech
    tts_resp = requests.post(f"{VOICE_URL}/speak", json={"text": response_text})
    audio_file_name = tts_resp.json().get("audio_file")
    audio_path = f"shared_audio/{audio_file_name}"

    return {
        "query": query,
        "response_text": response_text,
        "audio_file": audio_path
    }


class TextRequest(BaseModel):
    text: str


@app.post("/ask_text")
def ask_from_text(payload: TextRequest):
    text = payload.text
    print(f"▶ TEXT RECEIVED: {text}")

    try:
        retrieval_resp = requests.get(f"{RETRIEVAL_URL}/query", params={"query": text, "k": 3})
        print(f"▶ Retrieval Status: {retrieval_resp.status_code}")
        print(f"▶ Retrieval Content: {retrieval_resp.text}")
        context_docs = retrieval_resp.json().get("results", [])

        llm_resp = requests.post(f"{LLM_URL}/generate_brief", json={"question": text, "context_docs": context_docs})
        print(f"▶ LLM Status: {llm_resp.status_code}")
        print(f"▶ LLM Content: {llm_resp.text}")
        response_text = llm_resp.json().get("brief")

        tts_resp = requests.post(f"{VOICE_URL}/speak", json={"text": response_text})
        print(f"▶ TTS Status: {tts_resp.status_code}")
        print(f"▶ TTS Content: {tts_resp.text}")
        audio_file = tts_resp.json().get("audio_file")

        return {
            "query": text,
            "response_text": response_text,
            "audio_file": audio_file
        }

    except Exception as e:
        print(f"❌ ERROR in ask_text: {e}")
        return {"error": str(e)}
