"""Daily feed generation service."""
import uuid
from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from loop.db.dao.learning_dao import LearningDAO
from loop.db.models.learning import (
    DailyFeed,
    MasteryLevel,
    Subtopic,
    UserSubtopicProgress,
    UserTopic,
)


class FeedGenerationService:
    """Service for generating daily learning feeds."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.dao = LearningDAO(session)
        self.session = session
    
    async def generate_daily_feed(self, user_id: uuid.UUID) -> DailyFeed | None:
        """Generate today's learning feed for a user."""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Check if feed already exists for today
        existing_feed = await self.dao.feeds.get_user_feed_for_date(user_id, today)
        if existing_feed:
            return existing_feed
        
        # Get user's active topics
        user_topics = await self.dao.user_topics.get_user_topics(
            user_id, is_active=True
        )
        
        if not user_topics:
            return None
        
        # Select next subtopic using intelligent algorithm
        next_subtopic = await self._select_next_subtopic(user_id, user_topics)
        
        if not next_subtopic:
            return None
        
        # Create daily feed
        feed = await self.dao.feeds.create_feed(
            user_id=user_id,
            subtopic_id=next_subtopic.id,
            feed_date=today,
        )
        
        # Create or update progress tracking
        progress = await self.dao.progress.get_progress(user_id, next_subtopic.id)
        if not progress:
            await self.dao.progress.create_progress(
                user_id=user_id,
                subtopic_id=next_subtopic.id,
            )
        
        return feed
    
    async def _select_next_subtopic(
        self,
        user_id: uuid.UUID,
        user_topics: Sequence[UserTopic],
    ) -> Subtopic | None:
        """Intelligently select the next subtopic for learning."""
        # Priority 1: Check for due reviews
        due_reviews = await self.dao.progress.get_due_reviews(user_id, limit=5)
        if due_reviews:
            # Select the most overdue review
            most_overdue = min(
                due_reviews,
                key=lambda p: p.next_review_at or datetime.utcnow(),
            )
            return most_overdue.subtopic
        
        # Priority 2: Continue current topic progression
        for user_topic in user_topics:
            current_subtopic = await self._get_next_subtopic_in_topic(
                user_id, user_topic.topic_id
            )
            if current_subtopic:
                return current_subtopic
        
        return None
    
    async def _get_next_subtopic_in_topic(
        self,
        user_id: uuid.UUID,
        topic_id: uuid.UUID,
    ) -> Subtopic | None:
        """Get the next subtopic to learn in a specific topic."""
        # Get all subtopics for the topic
        subtopics = await self.dao.subtopics.get_subtopics_by_topic(
            topic_id, is_active=True
        )
        
        if not subtopics:
            return None
        
        # Get user's progress for all subtopics in this topic
        progress_list = await self.dao.progress.get_user_progress_by_topic(
            user_id, topic_id
        )
        
        # Create a map of subtopic_id to progress
        progress_map = {p.subtopic_id: p for p in progress_list}
        
        # Find the first incomplete subtopic
        for subtopic in subtopics:
            progress = progress_map.get(subtopic.id)
            
            # If no progress exists, this is the next subtopic
            if not progress:
                # Check prerequisites
                if await self._check_prerequisites(
                    user_id, subtopic, progress_map
                ):
                    return subtopic
            
            # If progress exists but not completed, continue with this subtopic
            elif (
                progress.mastery_level in [
                    MasteryLevel.NOT_STARTED,
                    MasteryLevel.IN_PROGRESS,
                    MasteryLevel.NEEDS_REVIEW,
                ]
                and not progress.completed_at
            ):
                return subtopic
        
        return None
    
    async def _check_prerequisites(
        self,
        user_id: uuid.UUID,
        subtopic: Subtopic,
        progress_map: dict[uuid.UUID, UserSubtopicProgress],
    ) -> bool:
        """Check if prerequisites are met for a subtopic."""
        if not subtopic.prerequisites:
            return True
        
        for prereq_id in subtopic.prerequisites:
            progress = progress_map.get(prereq_id)
            
            # Prerequisite not started or not mastered
            if (
                not progress
                or progress.mastery_level
                not in [MasteryLevel.MASTERED, MasteryLevel.EXPERT]
            ):
                return False
        
        return True
    
    async def generate_feeds_for_all_users(self) -> dict[str, int]:
        """Generate daily feeds for all active users."""
        # This would typically be called by a background job
        stats = {"generated": 0, "skipped": 0, "errors": 0}
        
        # Get all users with active topics
        # This is a simplified version - in practice, you'd batch process users
        
        return stats
    
    async def mark_feed_completed(
        self,
        user_id: uuid.UUID,
        feed_id: uuid.UUID,
    ) -> bool:
        """Mark a daily feed as completed."""
        feed = await self.dao.feeds.update_feed(
            feed_id,
            is_completed=True,
            completed_at=datetime.utcnow(),
        )
        return feed is not None


class SpacedRepetitionService:
    """Service for spaced repetition algorithm."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.dao = LearningDAO(session)
        self.session = session
    
    def calculate_next_review(
        self,
        progress: UserSubtopicProgress,
        performance_score: float,
    ) -> tuple[datetime, int, float]:
        """
        Calculate next review date using SM-2+ algorithm.
        
        Args:
            progress: Current user progress
            performance_score: Score from 0.0 to 1.0
        
        Returns:
            Tuple of (next_review_date, new_interval_days, new_ease_factor)
        """
        # Convert score to SM-2 grade (0-5)
        grade = min(5, max(0, int(performance_score * 5)))
        
        current_interval = progress.repetition_interval_days
        current_ease = progress.ease_factor
        consecutive_correct = progress.consecutive_correct
        
        if grade >= 3:  # Correct answer
            if consecutive_correct == 0:
                new_interval = 1
            elif consecutive_correct == 1:
                new_interval = 6
            else:
                new_interval = int(current_interval * current_ease)
            
            new_consecutive = consecutive_correct + 1
        else:  # Incorrect answer
            new_interval = 1
            new_consecutive = 0
        
        # Update ease factor
        new_ease = current_ease + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
        new_ease = max(1.3, new_ease)  # Minimum ease factor
        
        # Calculate next review date
        next_review = datetime.utcnow() + timedelta(days=new_interval)
        
        return next_review, new_interval, new_ease
    
    async def update_progress_with_performance(
        self,
        user_id: uuid.UUID,
        subtopic_id: uuid.UUID,
        performance_data: dict,
    ) -> UserSubtopicProgress | None:
        """Update progress based on learning session performance."""
        progress = await self.dao.progress.get_progress(user_id, subtopic_id)
        if not progress:
            return None
        
        # Calculate overall performance score
        performance_score = self._calculate_performance_score(performance_data)
        
        # Calculate next review using spaced repetition
        next_review, new_interval, new_ease = self.calculate_next_review(
            progress, performance_score
        )
        
        # Update mastery level based on performance
        new_mastery_level = self._calculate_mastery_level(
            progress, performance_score
        )
        
        # Update progress
        updated_progress = await self.dao.progress.update_progress(
            user_id,
            subtopic_id,
            last_reviewed_at=datetime.utcnow(),
            next_review_at=next_review,
            repetition_interval_days=new_interval,
            ease_factor=new_ease,
            consecutive_correct=progress.consecutive_correct + (1 if performance_score >= 0.8 else 0),
            mastery_level=new_mastery_level,
            mastery_score=performance_score,
        )
        
        return updated_progress
    
    def _calculate_performance_score(self, performance_data: dict) -> float:
        """Calculate overall performance score from session data."""
        scores = []
        
        # Article reading completion
        if performance_data.get("article_completed"):
            scores.append(0.3)  # Base score for reading
        
        # Flashcard performance
        flashcard_rate = performance_data.get("flashcard_success_rate", 0.0)
        scores.append(flashcard_rate * 0.4)
        
        # Quiz performance
        quiz_score = performance_data.get("quiz_score", 0.0)
        scores.append(quiz_score * 0.3)
        
        return sum(scores)
    
    def _calculate_mastery_level(
        self,
        progress: UserSubtopicProgress,
        performance_score: float,
    ) -> MasteryLevel:
        """Calculate new mastery level based on performance."""
        if performance_score >= 0.95:
            return MasteryLevel.EXPERT
        elif performance_score >= 0.85:
            return MasteryLevel.MASTERED
        elif performance_score >= 0.7:
            return MasteryLevel.IN_PROGRESS
        else:
            return MasteryLevel.NEEDS_REVIEW


class LearningAnalyticsService:
    """Service for learning analytics and insights."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.dao = LearningDAO(session)
        self.session = session
    
    async def get_weak_areas(
        self,
        user_id: uuid.UUID,
        limit: int = 5,
    ) -> list[dict]:
        """Identify user's weak areas that need attention."""
        # Get all progress with low mastery scores
        # This would involve more complex queries in practice
        weak_areas = []
        
        return weak_areas
    
    async def get_learning_velocity(
        self,
        user_id: uuid.UUID,
        days: int = 30,
    ) -> dict:
        """Calculate user's learning velocity metrics."""
        metrics = {
            "topics_per_week": 0.0,
            "avg_session_time": 0.0,
            "consistency_score": 0.0,
        }
        
        return metrics
    
    async def recommend_next_topics(
        self,
        user_id: uuid.UUID,
        limit: int = 3,
    ) -> list[dict]:
        """Recommend next topics based on user's learning patterns."""
        recommendations = []
        
        return recommendations