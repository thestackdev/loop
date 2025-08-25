"""Mock content generators for development and fallback."""
import json
import uuid
from typing import Dict, List

from loop.db.models.learning import Subtopic


class MockContentGenerator:
    """Generate mock content when AI service is unavailable or returns empty responses."""

    def generate_mock_article(self, subtopic: Subtopic) -> Dict:
        """Generate a mock article."""
        return {
            "title": f"Mastering {subtopic.name}",
            "content": f"""
# Understanding {subtopic.name}

{subtopic.description}

## Introduction

{subtopic.name} is a fundamental concept that every developer should master. This comprehensive guide will walk you through the essential aspects and practical applications.

## Key Concepts

1. **Fundamentals**: Understanding the basic principles
2. **Implementation**: How to apply these concepts in practice
3. **Best Practices**: Industry-standard approaches
4. **Common Pitfalls**: What to avoid and how to troubleshoot

## Practical Examples

Let's explore some real-world examples that demonstrate the concepts in action:

```example
// Sample code or concept demonstration
const example = "This shows how {subtopic.name} works in practice";
```

## Advanced Topics

Once you've mastered the basics, consider exploring:
- Advanced patterns and techniques
- Performance optimization
- Integration with other systems
- Troubleshooting common issues

## Summary

{subtopic.name} is essential for modern development. Key takeaways:
- Start with the fundamentals
- Practice with real examples
- Follow best practices
- Continuously refine your understanding

## Next Steps

Continue your learning journey by exploring related concepts and applying what you've learned in real projects.
            """.strip(),
            "estimated_read_time": 8,
            "key_concepts": [
                "Fundamentals",
                "Implementation",
                "Best Practices",
                "Performance",
                "Integration"
            ],
            "generated_at": str(uuid.uuid4()),
        }

    def generate_mock_flashcards(self, subtopic: Subtopic, count: int = 10) -> Dict:
        """Generate mock flashcards."""
        base_questions = [
            {
                "id": 1,
                "question": f"What is {subtopic.name}?",
                "answer": f"{subtopic.name} is {subtopic.description.lower()}",
                "difficulty": "easy",
                "tags": ["definition", "basic"]
            },
            {
                "id": 2,
                "question": f"When would you use {subtopic.name}?",
                "answer": f"You would use {subtopic.name} when you need to implement solutions that require its specific capabilities and benefits.",
                "difficulty": "medium",
                "tags": ["application", "practical"]
            },
            {
                "id": 3,
                "question": f"What are the key benefits of {subtopic.name}?",
                "answer": "Key benefits include improved code quality, better maintainability, enhanced performance, and easier debugging.",
                "difficulty": "medium", 
                "tags": ["benefits", "advantages"]
            },
            {
                "id": 4,
                "question": f"What are common mistakes when working with {subtopic.name}?",
                "answer": "Common mistakes include not following best practices, ignoring performance implications, and failing to handle edge cases properly.",
                "difficulty": "hard",
                "tags": ["pitfalls", "troubleshooting"]
            },
            {
                "id": 5,
                "question": f"How does {subtopic.name} compare to alternatives?",
                "answer": f"{subtopic.name} offers specific advantages in terms of functionality, performance, or ease of use compared to alternative approaches.",
                "difficulty": "hard",
                "tags": ["comparison", "alternatives"]
            }
        ]

        # Generate additional questions if needed
        flashcards = base_questions[:count]
        while len(flashcards) < count:
            additional_id = len(flashcards) + 1
            flashcards.append({
                "id": additional_id,
                "question": f"Advanced question {additional_id - 5} about {subtopic.name}?",
                "answer": f"This is an advanced concept related to {subtopic.name} that requires deeper understanding and practical experience.",
                "difficulty": "hard",
                "tags": ["advanced", "complex"]
            })

        return {"flashcards": flashcards}

    def generate_mock_quiz(self, subtopic: Subtopic, question_count: int = 5) -> Dict:
        """Generate mock quiz questions."""
        questions = [
            {
                "id": 1,
                "question": f"Which of the following best describes {subtopic.name}?",
                "type": "multiple_choice",
                "options": [
                    {"id": "a", "text": subtopic.description},
                    {"id": "b", "text": "An unrelated concept"},
                    {"id": "c", "text": "A deprecated feature"},
                    {"id": "d", "text": "A future specification"}
                ],
                "correct_answer": "a",
                "explanation": f"Option A correctly describes {subtopic.name} as: {subtopic.description}",
                "difficulty": "easy",
                "tags": ["definition", "basic"]
            },
            {
                "id": 2,
                "question": f"What is the primary use case for {subtopic.name}?",
                "type": "multiple_choice",
                "options": [
                    {"id": "a", "text": "Entertainment purposes"},
                    {"id": "b", "text": "Solving specific technical challenges"},
                    {"id": "c", "text": "Decorative functionality"},
                    {"id": "d", "text": "Legacy compatibility only"}
                ],
                "correct_answer": "b",
                "explanation": f"{subtopic.name} is primarily used for solving specific technical challenges in software development.",
                "difficulty": "medium",
                "tags": ["application", "use-case"]
            },
            {
                "id": 3,
                "question": f"When implementing {subtopic.name}, what should you prioritize?",
                "type": "multiple_choice",
                "options": [
                    {"id": "a", "text": "Speed over accuracy"},
                    {"id": "b", "text": "Complexity over simplicity"},
                    {"id": "c", "text": "Best practices and maintainability"},
                    {"id": "d", "text": "Latest trends over stability"}
                ],
                "correct_answer": "c",
                "explanation": "Following best practices and ensuring maintainability should be prioritized for long-term success.",
                "difficulty": "medium",
                "tags": ["best-practices", "implementation"]
            }
        ]

        # Add more questions if needed
        while len(questions) < question_count:
            question_id = len(questions) + 1
            questions.append({
                "id": question_id,
                "question": f"Advanced question {question_id - 3} about {subtopic.name}?",
                "type": "multiple_choice",
                "options": [
                    {"id": "a", "text": "Correct advanced answer"},
                    {"id": "b", "text": "Incorrect option 1"},
                    {"id": "c", "text": "Incorrect option 2"},
                    {"id": "d", "text": "Incorrect option 3"}
                ],
                "correct_answer": "a",
                "explanation": f"This tests advanced understanding of {subtopic.name} concepts.",
                "difficulty": "hard",
                "tags": ["advanced", "complex"]
            })

        return {"questions": questions[:question_count]}

    def generate_mock_mnemonics(self, subtopic: Subtopic, concepts: List[str]) -> Dict:
        """Generate mock mnemonics."""
        mnemonics = []
        
        for i, concept in enumerate(concepts[:5]):  # Limit to 5 concepts
            mnemonics.append({
                "id": i + 1,
                "concept": concept,
                "mnemonic": f"Remember {concept} by thinking: '{concept[0]}' stands for {concept}",
                "technique": "Acronym",
                "explanation": f"Use the first letter of {concept} to remember its key characteristics and applications.",
                "example": f"When you see '{concept[0]}', think '{concept}'"
            })

        # Add a general mnemonic for the subtopic
        mnemonics.append({
            "id": len(mnemonics) + 1,
            "concept": subtopic.name,
            "mnemonic": f"Master {subtopic.name} with the memory phrase: '{subtopic.name} Makes Programming Perfect'",
            "technique": "Alliteration",
            "explanation": f"Use alliteration to remember that {subtopic.name} improves your programming skills.",
            "example": f"'{subtopic.name} Makes Programming Perfect' - remember this when studying"
        })

        return {"mnemonics": mnemonics}