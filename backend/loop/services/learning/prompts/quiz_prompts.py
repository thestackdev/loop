"""Quiz generation prompts."""
from typing import List

from loop.db.models.learning import Subtopic


def build_quiz_prompt(
    subtopic: Subtopic, 
    exclude_questions: List[str] | None, 
    count: int
) -> str:
    """Build prompt for quiz generation."""
    exclusions = ""
    if exclude_questions:
        exclusions = f"\nAvoid these question topics: {', '.join(exclude_questions)}"
    
    return f"""
Create {count} challenging quiz questions for "{subtopic.name}".

Topic: {subtopic.description}{exclusions}

Requirements:
1. Test deep understanding and application
2. Include multiple choice, true/false, and scenario-based questions
3. Make questions that differentiate between levels of mastery
4. Include realistic scenarios a backend engineer would face
5. Provide detailed explanations for correct answers

Return as JSON in this exact format:
{{
    "questions": [
        {{
            "id": 1,
            "type": "multiple_choice|true_false|scenario",
            "question": "Question text",
            "options": ["A", "B", "C", "D"] (for multiple choice),
            "correct_answer": "A" or true/false,
            "explanation": "Why this is correct and others wrong",
            "difficulty": "easy|medium|hard",
            "points": 1-5
        }}
    ]
}}

Focus on practical application and critical thinking.
"""


QUIZ_SYSTEM_PROMPT = """
You are an expert at creating challenging technical quizzes that test deep understanding 
and application of concepts. Create questions that go beyond memorization to test 
problem-solving ability, critical thinking, and practical application in real-world 
backend engineering scenarios.
"""