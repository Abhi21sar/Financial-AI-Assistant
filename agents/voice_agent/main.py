from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import whisper
import pyttsx3
import uuid
import os

app = FastAPI()

# Ensure output directory exists
AUDIO_DIR = "shared_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Load Whisper model
model = whisper.load_model("base")  # Can be 'tiny', 'small', etc.

@app.get("/")
def root():
    return {"message": "Voice Agent is running"}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    temp_path = os.path.join(AUDIO_DIR, f"temp_audio_{uuid.uuid4().hex}.wav")
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        result = model.transcribe(temp_path)
        return {"transcript": result["text"]}
    finally:
        os.remove(temp_path)

class SpeakRequest(BaseModel):
    text: str

@app.post("/speak")
def speak(req: SpeakRequest):
    text = req.text
    filename = f"output_{uuid.uuid4().hex}.mp3"
    output_path = os.path.join(AUDIO_DIR, filename)

    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, output_path)
        engine.runAndWait()

        # Wait a moment to ensure file is written
        import time
        timeout = 5  # seconds
        while timeout > 0:
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1024:
                break
            time.sleep(0.2)
            timeout -= 0.2

        if not os.path.exists(output_path) or os.path.getsize(output_path) < 1024:
            return {"error": "Audio file generation failed or incomplete"}

        return {"audio_file": output_path}

    except Exception as e:
        return {"error": f"TTS failed: {str(e)}"}

