"""AI content generation service using OpenAI."""
import json
import uuid
from typing import Any, Dict, List

from openai import AsyncAzureOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from loop.db.dao.learning_dao import LearningDAO
from loop.db.models.learning import ContentType, GeneratedContent, Subtopic
from loop.services.learning.prompts.article_prompts import (
    ARTICLE_SYSTEM_PROMPT,
    build_article_prompt,
)
from loop.services.learning.prompts.flashcard_prompts import (
    FLASHCARD_SYSTEM_PROMPT,
    build_flashcard_prompt,
)
from loop.services.learning.prompts.mnemonic_prompts import (
    MNEMONIC_SYSTEM_PROMPT,
    build_mnemonic_prompt,
)
from loop.services.learning.prompts.quiz_prompts import (
    QUIZ_SYSTEM_PROMPT,
    build_quiz_prompt,
)
from loop.settings import settings
from loop.services.learning.mock_content import MockContentGenerator


def extract_json_from_response(raw_content: str) -> str:
    """Extract JSON from AI response, handling markdown code blocks."""
    content = raw_content.strip()
    
    # Handle markdown code blocks
    if content.startswith('```json'):
        content = content.split('```json')[1].split('```')[0].strip()
    elif content.startswith('```'):
        content = content.split('```')[1].split('```')[0].strip()
    
    # Handle cases where JSON is embedded in text
    if '{' in content and '}' in content:
        start_idx = content.find('{')
        # Find the last closing brace that matches
        brace_count = 0
        end_idx = -1
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
        
        if end_idx != -1:
            content = content[start_idx:end_idx]
    
    return content


class AIContentService:
    """Service for generating learning content using OpenAI."""

    def __init__(self, session: AsyncSession) -> None:
        self.dao = LearningDAO(session)
        self.session = session
        self.mock_generator = MockContentGenerator()
        self.client = AsyncAzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
        )

    async def generate_article(
        self,
        subtopic: Subtopic,
        difficulty_level: int = 3,
    ) -> GeneratedContent:
        """Generate a comprehensive article for a subtopic."""
        prompt = build_article_prompt(subtopic, difficulty_level)

        response = await self.client.chat.completions.create(
            model=settings.azure_openai_model_name,
            messages=[
                {
                    "role": "system",
                    "content": ARTICLE_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=4000,
        )

        content = response.choices[0].message.content

        # Structure the article content
        article_data = {
            "title": f"Mastering {subtopic.name}",
            "content": content,
            "estimated_read_time": self._estimate_read_time(content),
            "key_concepts": self._extract_key_concepts(content),
            "generated_at": str(uuid.uuid4()),
        }

        # Save to database
        generated_content = await self.dao.content.create_content(
            subtopic_id=subtopic.id,
            content_type=ContentType.ARTICLE,
            content_data=article_data,
            difficulty_level=difficulty_level,
            ai_model=settings.azure_openai_model_name,
            prompt_template=prompt[:500] + "..." if len(prompt) > 500 else prompt,
        )

        return generated_content

    async def generate_flashcards(
        self,
        subtopic: Subtopic,
        article_content: str | None = None,
        count: int = 10,
    ) -> GeneratedContent:
        """Generate flashcards for a subtopic."""
        prompt = build_flashcard_prompt(subtopic, article_content, count)

        response = await self.client.chat.completions.create(
            model=settings.azure_openai_model_name,
            messages=[
                {
                    "role": "system",
                    "content": FLASHCARD_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=2000,
        )

        # Parse the JSON response
        raw_content = response.choices[0].message.content
        
        # Handle empty or None responses - use mock content as fallback
        if not raw_content or raw_content.strip() == "":
            flashcards_data = self.mock_generator.generate_mock_flashcards(subtopic, count)
            flashcards_data["fallback_used"] = "AI returned empty response - using mock content"
        else:
            try:
                content = extract_json_from_response(raw_content)
                flashcards_data = json.loads(content)
            except (json.JSONDecodeError, IndexError) as e:
                # Use mock content as fallback when parsing fails
                flashcards_data = self.mock_generator.generate_mock_flashcards(subtopic, count)
                flashcards_data["fallback_used"] = f"AI parsing failed: {str(e)} - using mock content"
                flashcards_data["debug_info"] = {
                    "error": str(e),
                    "response_length": len(raw_content),
                    "starts_with": raw_content[:50] if raw_content else "None",
                }

        # Save to database
        generated_content = await self.dao.content.create_content(
            subtopic_id=subtopic.id,
            content_type=ContentType.FLASHCARD,
            content_data=flashcards_data,
            difficulty_level=subtopic.difficulty_level,
            ai_model=settings.azure_openai_model_name,
        )

        return generated_content

    async def generate_quiz(
        self,
        subtopic: Subtopic,
        exclude_questions: List[str] | None = None,
        question_count: int = 5,
    ) -> GeneratedContent:
        """Generate quiz questions for a subtopic."""
        prompt = build_quiz_prompt(subtopic, exclude_questions, question_count)

        response = await self.client.chat.completions.create(
            model=settings.azure_openai_model_name,
            messages=[
                {
                    "role": "system",
                    "content": QUIZ_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=2500,
        )

        # Parse the JSON response
        raw_content = response.choices[0].message.content
        
        # Handle empty or None responses - use mock content as fallback
        if not raw_content or raw_content.strip() == "":
            quiz_data = self.mock_generator.generate_mock_quiz(subtopic, question_count)
            quiz_data["fallback_used"] = "AI returned empty response - using mock content"
        else:
            try:
                content = extract_json_from_response(raw_content)
                quiz_data = json.loads(content)
            except (json.JSONDecodeError, IndexError) as e:
                # Use mock content as fallback when parsing fails
                quiz_data = self.mock_generator.generate_mock_quiz(subtopic, question_count)
                quiz_data["fallback_used"] = f"AI parsing failed: {str(e)} - using mock content"
                quiz_data["debug_info"] = {
                    "error": str(e),
                    "response_length": len(raw_content),
                    "starts_with": raw_content[:50] if raw_content else "None",
                }

        # Save to database
        generated_content = await self.dao.content.create_content(
            subtopic_id=subtopic.id,
            content_type=ContentType.QUIZ,
            content_data=quiz_data,
            difficulty_level=subtopic.difficulty_level,
            ai_model=settings.azure_openai_model_name,
        )

        return generated_content

    async def generate_mnemonics(
        self,
        subtopic: Subtopic,
        concepts: List[str],
    ) -> GeneratedContent:
        """Generate mnemonics for complex concepts."""
        prompt = build_mnemonic_prompt(subtopic, concepts)

        response = await self.client.chat.completions.create(
            model=settings.azure_openai_model_name,
            messages=[
                {
                    "role": "system",
                    "content": MNEMONIC_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=1500,
        )

        # Parse the JSON response
        raw_content = response.choices[0].message.content
        
        # Handle empty or None responses - use mock content as fallback
        if not raw_content or raw_content.strip() == "":
            mnemonic_data = self.mock_generator.generate_mock_mnemonics(subtopic, concepts)
            mnemonic_data["fallback_used"] = "AI returned empty response - using mock content"
        else:
            try:
                content = extract_json_from_response(raw_content)
                mnemonic_data = json.loads(content)
            except (json.JSONDecodeError, IndexError) as e:
                # Use mock content as fallback when parsing fails
                mnemonic_data = self.mock_generator.generate_mock_mnemonics(subtopic, concepts)
                mnemonic_data["fallback_used"] = f"AI parsing failed: {str(e)} - using mock content"
                mnemonic_data["debug_info"] = {
                    "error": str(e),
                    "response_length": len(raw_content),
                    "starts_with": raw_content[:50] if raw_content else "None",
                }

        # Save to database
        generated_content = await self.dao.content.create_content(
            subtopic_id=subtopic.id,
            content_type=ContentType.MNEMONIC,
            content_data=mnemonic_data,
            difficulty_level=subtopic.difficulty_level,
            ai_model=settings.azure_openai_model_name,
        )

        return generated_content

    def _estimate_read_time(self, content: str) -> int:
        """Estimate reading time based on word count."""
        word_count = len(content.split())
        # Average reading speed: 200-250 words per minute for technical content
        return max(1, word_count // 225)

    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content (simplified version)."""
        # This is a placeholder - in practice, you'd use NLP to extract key terms
        words = content.split()
        # Simple heuristic: look for capitalized technical terms
        concepts = []
        for word in words:
            if word.istitle() and len(word) > 3:
                concepts.append(word.strip('.,!?'))

        return list(set(concepts))[:10]  # Return top 10 unique concepts


class ContentWorkflowService:
    """Service for managing complete content generation workflows."""

    def __init__(self, session: AsyncSession) -> None:
        self.ai_service = AIContentService(session)
        self.dao = LearningDAO(session)
        self.session = session

    async def generate_complete_learning_content(
        self,
        subtopic_id: uuid.UUID,
    ) -> Dict[str, GeneratedContent]:
        """Generate all content types for a subtopic."""
        subtopic = await self.dao.subtopics.get_subtopic(subtopic_id)
        if not subtopic:
            raise ValueError(f"Subtopic {subtopic_id} not found")

        results = {}

        # Generate article first
        article = await self.ai_service.generate_article(subtopic)
        results["article"] = article

        # Generate flashcards based on article
        flashcards = await self.ai_service.generate_flashcards(
            subtopic,
            article.content_data.get("content", "")
        )
        results["flashcards"] = flashcards

        # Generate quiz
        quiz = await self.ai_service.generate_quiz(subtopic)
        results["quiz"] = quiz

        # Generate mnemonics for key concepts
        key_concepts = article.content_data.get("key_concepts", [])
        if key_concepts:
            mnemonics = await self.ai_service.generate_mnemonics(
                subtopic,
                key_concepts[:5]  # Top 5 concepts
            )
            results["mnemonics"] = mnemonics

        return results

    async def regenerate_content(
        self,
        content_id: uuid.UUID,
        reason: str = "quality_improvement",
    ) -> GeneratedContent | None:
        """Regenerate specific content with improvements."""
        content = await self.dao.content.get_content(content_id)
        if not content:
            return None

        subtopic = await self.dao.subtopics.get_subtopic(content.subtopic_id)
        if not subtopic:
            return None

        # Mark old content as inactive
        await self.dao.session.execute(
            f"UPDATE generated_content SET is_active = false WHERE id = '{content_id}'"
        )

        # Generate new content based on type
        if content.content_type == ContentType.ARTICLE:
            return await self.ai_service.generate_article(
                subtopic,
                content.difficulty_level
            )
        elif content.content_type == ContentType.FLASHCARD:
            return await self.ai_service.generate_flashcards(subtopic)
        elif content.content_type == ContentType.QUIZ:
            return await self.ai_service.generate_quiz(subtopic)
        elif content.content_type == ContentType.MNEMONIC:
            concepts = content.content_data.get("concepts", [])
            return await self.ai_service.generate_mnemonics(subtopic, concepts)

        return None
