# This holds the system prompt and the JSON schema for the Gemini agent.
# This follows Steps 3 & 4 from the PDF, but combines them for one efficient API call.

SYSTEM_PROMPT = """You are an autonomous study workflow agent. Based on the provided text, generate:
1.  A list of the 5-7 main topics found in the text.
2.  5 detailed question-answer flashcards.
3.  5 challenging multiple-choice questions (each with 4 options and one correct answer).

You must return *only* a valid JSON object matching the provided schema.
Ensure questions are relevant and answers are accurate based on the text."""

# This is the JSON schema we will ask Gemini to follow.
RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "topics": {
            "type": "ARRAY",
            "items": { "type": "STRING" },
            "description": "A list of 5-7 main topics from the text."
        },
        "flashcards": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "question": { "type": "STRING" },
                    "answer": { "type": "STRING" }
                },
                "required": ["question", "answer"]
            },
            "description": "A list of 5 question-answer flashcards."
        },
        "quiz": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "question": { "type": "STRING" },
                    "options": {
                        "type": "ARRAY",
                        "items": { "type": "STRING" },
                        "description": "A list of 4 options for the multiple-choice question."
                        # "minItems": 4,  <-- THIS WAS THE ERROR
                        # "maxItems": 4   <-- THIS WAS THE ERROR
                    },
                    "answer": { "type": "STRING" }
                },
                "required": ["question", "options", "answer"]
            },
            "description": "A list of 5 multiple-choice questions."
        }
    },
    "required": ["topics", "flashcards", "quiz"]
}