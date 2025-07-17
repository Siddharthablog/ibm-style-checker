from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TextInput(BaseModel):
    text: str

class Suggestion(BaseModel):
    issue_type: str  # "grammar" or "style"
    message: str
    offset_start: int
    offset_end: int
    suggestion: str

class Output(BaseModel):
    original_text: str
    suggestions: List[Suggestion]

@app.post("/check-style", response_model=Output)
async def check_style(input_text: TextInput):
    text = input_text.text.strip()
    suggestions = []

    if not text.endswith("."):
        suggestions.append({
            "issue_type": "grammar",
            "message": "Sentence may be incomplete or missing punctuation.",
            "offset_start": max(0, len(text) - 1),
            "offset_end": len(text),
            "suggestion": text + "."
        })

    if "is being" in text or "was done" in text:
        phrase = "is being" if "is being" in text else "was done"
        suggestions.append({
            "issue_type": "style",
            "message": "Possible passive voice. Prefer active voice in IBM style.",
            "offset_start": text.find(phrase),
            "offset_end": text.find(phrase) + len(phrase),
            "suggestion": "reword using active voice"
        })

    return {"original_text": text, "suggestions": suggestions}

@app.post("/check-passive-voice")
async def check_passive_voice(input_text: TextInput):
    passive_phrases = ["was done", "is being", "has been", "will be"]
    issues = []

    for phrase in passive_phrases:
        if phrase in input_text.text:
            issues.append({
                "sentence": input_text.text,
                "issue": f"Passive voice detected: '{phrase}'",
                "suggestion": "Consider rewording to active voice."
            })

    return {"original_text": input_text.text, "passive_issues": issues}

@app.post("/check-tone")
async def check_tone(input_text: TextInput):
    tone_issues = []
    if "ASAP" in input_text.text or "you must" in input_text.text.lower():
        tone_issues.append({
            "issue": "Tone may sound too aggressive or demanding.",
            "suggestion": "Use polite or collaborative language.",
            "explanation": "IBM style prefers professional and respectful tone."
        })

    return {"original_text": input_text.text, "tone_issues": tone_issues}

@app.post("/check-clarity")
async def check_clarity(input_text: TextInput):
    issues = []
    if len(input_text.text.split()) > 30:
        issues.append({
            "sentence": input_text.text,
            "issue": "Sentence may be too long or complex.",
            "suggestion": "Break it into shorter sentences for clarity."
        })

    return {"original_text": input_text.text, "clarity_issues": issues}
