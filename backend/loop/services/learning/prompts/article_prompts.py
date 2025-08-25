"""Article generation prompts."""
from typing import Dict

from loop.db.models.learning import Subtopic


def build_article_prompt(subtopic: Subtopic, difficulty_level: int) -> str:
    """Build prompt for article generation."""
    difficulty_map: Dict[int, str] = {
        1: "beginner",
        2: "intermediate",
        3: "advanced",
        4: "expert",
        5: "architect-level"
    }
    
    difficulty_desc = difficulty_map.get(difficulty_level, "advanced")
    
    return f"""
Create a comprehensive technical article about "{subtopic.name}" for {difficulty_desc} backend engineers.

Topic Context: {subtopic.description}
Estimated Reading Time: {subtopic.estimated_time_minutes} minutes

Requirements:
1. Write at senior backend engineer level with practical depth
2. Include real-world examples and use cases
3. Cover implementation details and best practices
4. Add code snippets where relevant
5. Explain the "why" behind concepts, not just the "what"
6. Include potential pitfalls and how to avoid them
7. Connect to broader system design concepts where applicable

Structure:
- Brief introduction (why this matters)
- Core concepts and theory
- Practical implementation details
- Real-world examples
- Best practices and patterns
- Common mistakes to avoid
- Summary of key takeaways

Make it engaging, practical, and immediately applicable to daily work.
"""


ARTICLE_SYSTEM_PROMPT = """
You are an expert technical educator creating content for senior backend engineers. 
Create comprehensive, practical, and engaging technical articles that combine theoretical depth 
with real-world application. Focus on actionable insights and best practices that engineers 
can immediately apply in their work.
"""