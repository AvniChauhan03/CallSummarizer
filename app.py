# app.py
import os
import csv
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

app = FastAPI()
CSV_FILE = "call_analysis.csv"

# Initialize Groq client (it will read GROQ_API_KEY from env)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Create CSV header if missing
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Transcript", "Summary", "Sentiment"])

class TranscriptIn(BaseModel):
    transcript: str

@app.post("/analyze")
def analyze(inp: TranscriptIn):
    transcript = inp.transcript.strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript is empty")

    # Prompt: ask Groq to return JSON with summary & sentiment
    system_msg = (
    "You are an assistant that summarizes a customer call. "
    "Respond ONLY with a JSON object and nothing else. "
    "The JSON must have two fields: "
    "\"summary\" (2-3 sentences) and \"sentiment\" (one of: positive, neutral, negative)."
    )


    user_msg = f"Transcript:\n\"\"\"\n{transcript}\n\"\"\"\n\nRespond with JSON."

    try:
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            model="llama-3.3-70b-versatile",
            max_completion_tokens=300,
            temperature=0.0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {e}")

    content = chat.choices[0].message.content.strip()

    # Try parse JSON (Groq usually can return strict JSON if asked)
    try:
        j = json.loads(content)
        summary = j.get("summary", "").strip()
        sentiment = j.get("sentiment", "").strip().lower()
    except json.JSONDecodeError:
        # Fallback: simple split heuristics if not valid JSON
        summary = "Could not parse summary from model response."
        sentiment = "unknown"

    # Save row to CSV
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([f"Transcript: {transcript}"])
        writer.writerow([f"Summary: {summary}"])
        writer.writerow([f"Sentiment: {sentiment}"])
        writer.writerow([]) 

    return {"transcript": transcript, "summary": summary, "sentiment": sentiment}
