# IBM Style & Grammar Checker

A simple FastAPI service to check grammar issues and IBM-style guide compliance.

## Endpoints

### POST /check-style
Request:
```json
{ "text": "Your text here" }


{
  "original_text": "...",
  "suggestions": [
    {
      "issue_type": "grammar",
      "message": "...",
      "offset_start": 0,
      "offset_end": 10,
      "suggestion": "..."
    }
  ]
}
