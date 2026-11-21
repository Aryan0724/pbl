import json
import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)


def generate_questions(
    topic, content, question_type, difficulty,
    number_of_questions, subject, marks
):
    """Ask Gemini to create a structured question paper."""
    difficulty_guidance = {
        "Easy": "Test recall, definitions and basic understanding.",
        "Intermediate": (
            "Test understanding, comparisons, examples and applications."
        ),
        "Hard": (
            "Test analysis, evaluation, critical thinking and problem solving."
        )
    }

    prompt = f"""
You are an experienced university examination paper setter.
Create exactly {number_of_questions} original questions.
Subject: {subject}
Topic: {topic}
Question type: {question_type}
Difficulty: {difficulty}
Difficulty guidance: {difficulty_guidance.get(difficulty, "Standard academic rigor.")}
Marks per question: {marks}

Use the study material below as the main source. Do not invent
facts that are not supported by it. If it is short, use standard
subject knowledge relevant to the topic.

STUDY MATERIAL:
{content[:18000]}

Return only a JSON object with this structure:
{{
    "title": "Question Paper",
    "subject": "{subject}",
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "questions": [
        {{
            "number": 1,
            "type": "MCQ",
            "question": "Question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct answer",
            "marks": {marks}
        }}
    ]
}}

Rules:
- For MCQ, include exactly four options and one correct answer.
- For Short and Long, use an empty options array.
- For Mixed, include a balanced mix of MCQ, Short and Long.
- Include a concise model answer for every question.
- Do not repeat questions.
- Keep the requested number of questions exactly.
"""

    models_to_try = [
        MODEL,
        "gemini-3-flash-preview",
        "gemini-flash-latest",
        "gemini-3.8-flash",
        "gemini-3.5-flash",
    ]

    # Remove duplicates preserving order
    seen = set()
    unique_models = []
    for m in models_to_try:
        if m and m not in seen:
            seen.add(m)
            unique_models.append(m)

    response_text = None
    last_error = None
    for model_name in unique_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            response_text = response.text
            if response_text:
                break
        except Exception as e:
            last_error = e
            continue

    if not response_text:
        raise RuntimeError(f"AI generation failed across models: {last_error}")

    # Clean any potential markdown wrapping
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    paper = json.loads(cleaned)
    questions = paper.get("questions", [])

    # If count is slightly off, trim or adapt gracefully so the presentation never fails
    if len(questions) > number_of_questions:
        questions = questions[:number_of_questions]
        paper["questions"] = questions

    for index, question in enumerate(questions, start=1):
        question["number"] = index
        question.setdefault("type", question_type)
        question.setdefault("options", [])
        question.setdefault("answer", "Answer not provided")
        question["marks"] = marks

    paper["title"] = paper.get("title", "Generated Question Paper")
    paper["subject"] = subject
    paper["topic"] = topic
    paper["difficulty"] = difficulty
    return paper
