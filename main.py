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
