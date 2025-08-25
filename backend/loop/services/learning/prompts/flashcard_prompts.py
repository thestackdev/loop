"""Flashcard generation prompts."""
from loop.db.models.learning import Subtopic


def build_flashcard_prompt(
    subtopic: Subtopic, 
    article_content: str | None, 
    count: int
) -> str:
    """Build prompt for flashcard generation."""
    content_context = ""
    if article_content:
        content_context = f"\nArticle Content Reference:\n{article_content[:1000]}..."
    
    return f"""
Create {count} high-quality flashcards for the topic "{subtopic.name}".

Topic: {subtopic.description}{content_context}

Requirements:
1. Focus on active recall - test understanding, not memorization
2. Include mnemonics where helpful for complex concepts
3. Vary question types: definitions, applications, comparisons, scenarios
4. Make questions specific and practical
5. Include brief explanations in answers

Return as JSON in this exact format:
{{
    "flashcards": [
        {{
            "id": 1,
            "question": "Question text here",
            "answer": "Answer with explanation",
            "mnemonic": "Memory aid if applicable (optional)",
            "difficulty": "easy|medium|hard",
            "tags": ["tag1", "tag2"]
        }}
    ]
}}

Make flashcards that would help a senior engineer master this topic through spaced repetition.
"""


FLASHCARD_SYSTEM_PROMPT = """
You are an expert at creating effective flashcards for spaced repetition learning. 
Focus on active recall and memory techniques. Create questions that test deep understanding 
rather than simple memorization. Use mnemonics and memory aids to help engineers 
remember complex technical concepts.
"""