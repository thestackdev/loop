"""Data Access Object for learning system."""
import uuid
from datetime import datetime, timedelta
from typing import Any, Sequence

from sqlalchemy import and_, delete, desc, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from loop.db.models.learning import (
    DailyFeed,
    FlashcardAttempt,
    GeneratedContent,
    LearningSession,
    MasteryLevel,
    QuizAttempt,
    Subtopic,
    Topic,
    UserSubtopicProgress,
    UserTopic,
)


class TopicDAO:
    """Data access object for Topic operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_topic(self, **kwargs: Any) -> Topic:
        """Create a new topic."""
        topic = Topic(**kwargs)
        self.session.add(topic)
        await self.session.commit()
        await self.session.refresh(topic)
        return topic
    
    async def get_topic(self, topic_id: uuid.UUID) -> Topic | None:
        """Get a topic by ID."""
        result = await self.session.execute(
            select(Topic).where(Topic.id == topic_id)
        )
        return result.scalar_one_or_none()
    
    async def get_topics(
        self,
        category: str | None = None,
        is_active: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Topic]:
        """Get all topics with optional filters."""
        query = select(Topic)
        
        if category:
            query = query.where(Topic.category == category)
        if is_active is not None:
            query = query.where(Topic.is_active == is_active)
        
        query = query.limit(limit).offset(offset).order_by(Topic.name)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update_topic(self, topic_id: uuid.UUID, **kwargs: Any) -> Topic | None:
        """Update a topic."""
        result = await self.session.execute(
            update(Topic)
            .where(Topic.id == topic_id)
            .values(**kwargs, updated_at=datetime.utcnow())
            .returning(Topic)
        )
        topic = result.scalar_one_or_none()
        if topic:
            await self.session.commit()
        return topic
    
    async def delete_topic(self, topic_id: uuid.UUID) -> bool:
        """Delete a topic."""
        topic = await self.get_topic(topic_id)
        if topic:
            await self.session.delete(topic)
            await self.session.commit()
            return True
        return False


class SubtopicDAO:
    """Data access object for Subtopic operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_subtopic(self, **kwargs: Any) -> Subtopic:
        """Create a new subtopic."""
        subtopic = Subtopic(**kwargs)
        self.session.add(subtopic)
        await self.session.commit()
        await self.session.refresh(subtopic)
        return subtopic
    
    async def get_subtopic(self, subtopic_id: uuid.UUID) -> Subtopic | None:
        """Get a subtopic by ID."""
        result = await self.session.execute(
            select(Subtopic)
            .options(joinedload(Subtopic.topic))
            .where(Subtopic.id == subtopic_id)
        )
        return result.scalar_one_or_none()
    
    async def get_subtopics_by_topic(
        self,
        topic_id: uuid.UUID,
        is_active: bool | None = None,
    ) -> Sequence[Subtopic]:
        """Get all subtopics for a topic."""
        query = select(Subtopic).where(Subtopic.topic_id == topic_id)
        
        if is_active is not None:
            query = query.where(Subtopic.is_active == is_active)
        
        query = query.order_by(Subtopic.order_index)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update_subtopic(self, subtopic_id: uuid.UUID, **kwargs: Any) -> Subtopic | None:
        """Update a subtopic."""
        result = await self.session.execute(
            update(Subtopic)
            .where(Subtopic.id == subtopic_id)
            .values(**kwargs)
            .returning(Subtopic)
        )
        subtopic = result.scalar_one_or_none()
        if subtopic:
            await self.session.commit()
        return subtopic
    
    async def delete_subtopic(self, subtopic_id: uuid.UUID) -> bool:
        """Delete a subtopic."""
        result = await self.session.execute(
            delete(Subtopic)
            .where(Subtopic.id == subtopic_id)
        )
        if result.rowcount > 0:
            await self.session.commit()
            return True
        return False


class UserTopicDAO:
    """Data access object for UserTopic operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_user_topic(self, **kwargs: Any) -> UserTopic:
        """Create a new user topic."""
        user_topic = UserTopic(**kwargs)
        self.session.add(user_topic)
        await self.session.commit()
        await self.session.refresh(user_topic)
        
        # Fetch with relationship loaded
        result = await self.session.execute(
            select(UserTopic)
            .options(joinedload(UserTopic.topic))
            .where(UserTopic.id == user_topic.id)
        )
        return result.scalar_one()
    
    async def get_user_topics(
        self,
        user_id: uuid.UUID,
        is_active: bool | None = None,
    ) -> Sequence[UserTopic]:
        """Get all topics for a user."""
        query = (
            select(UserTopic)
            .options(joinedload(UserTopic.topic))
            .where(UserTopic.user_id == user_id)
        )
        
        if is_active is not None:
            query = query.where(UserTopic.is_active == is_active)
        
        query = query.order_by(UserTopic.priority_order)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_user_topic(
        self,
        user_id: uuid.UUID,
        topic_id: uuid.UUID,
    ) -> UserTopic | None:
        """Get a specific user topic."""
        result = await self.session.execute(
            select(UserTopic)
            .options(joinedload(UserTopic.topic))
            .where(
                and_(
                    UserTopic.user_id == user_id,
                    UserTopic.topic_id == topic_id,
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def update_user_topic(
        self,
        user_id: uuid.UUID,
        topic_id: uuid.UUID,
        **kwargs: Any,
    ) -> UserTopic | None:
        """Update a user topic."""
        result = await self.session.execute(
            update(UserTopic)
            .where(
                and_(
                    UserTopic.user_id == user_id,
                    UserTopic.topic_id == topic_id,
                )
            )
            .values(**kwargs)
            .returning(UserTopic)
        )
        user_topic = result.scalar_one_or_none()
        if user_topic:
            await self.session.commit()
            
            # Fetch with relationship loaded
            result = await self.session.execute(
                select(UserTopic)
                .options(joinedload(UserTopic.topic))
                .where(UserTopic.id == user_topic.id)
            )
            return result.scalar_one()
        return user_topic


class UserProgressDAO:
    """Data access object for UserSubtopicProgress operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_progress(self, **kwargs: Any) -> UserSubtopicProgress:
        """Create new user progress."""
        progress = UserSubtopicProgress(**kwargs)
        self.session.add(progress)
        await self.session.commit()
        await self.session.refresh(progress)
        return progress
    
    async def get_progress(
        self,
        user_id: uuid.UUID,
        subtopic_id: uuid.UUID,
    ) -> UserSubtopicProgress | None:
        """Get user progress for a subtopic."""
        result = await self.session.execute(
            select(UserSubtopicProgress)
            .options(joinedload(UserSubtopicProgress.subtopic))
            .where(
                and_(
                    UserSubtopicProgress.user_id == user_id,
                    UserSubtopicProgress.subtopic_id == subtopic_id,
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_progress_by_topic(
        self,
        user_id: uuid.UUID,
        topic_id: uuid.UUID,
    ) -> Sequence[UserSubtopicProgress]:
        """Get all user progress for subtopics in a topic."""
        result = await self.session.execute(
            select(UserSubtopicProgress)
            .options(joinedload(UserSubtopicProgress.subtopic))
            .join(Subtopic, UserSubtopicProgress.subtopic_id == Subtopic.id)
            .where(
                and_(
                    UserSubtopicProgress.user_id == user_id,
                    Subtopic.topic_id == topic_id,
                )
            )
            .order_by(Subtopic.order_index)
        )
        return result.scalars().all()
    
    async def update_progress(
        self,
        user_id: uuid.UUID,
        subtopic_id: uuid.UUID,
        **kwargs: Any,
    ) -> UserSubtopicProgress | None:
        """Update user progress."""
        result = await self.session.execute(
            update(UserSubtopicProgress)
            .where(
                and_(
                    UserSubtopicProgress.user_id == user_id,
                    UserSubtopicProgress.subtopic_id == subtopic_id,
                )
            )
            .values(**kwargs)
            .returning(UserSubtopicProgress)
        )
        progress = result.scalar_one_or_none()
        if progress:
            await self.session.commit()
        return progress
    
    async def get_due_reviews(
        self,
        user_id: uuid.UUID,
        limit: int = 10,
    ) -> Sequence[UserSubtopicProgress]:
        """Get subtopics due for review."""
        now = datetime.utcnow()
        result = await self.session.execute(
            select(UserSubtopicProgress)
            .options(joinedload(UserSubtopicProgress.subtopic))
            .where(
                and_(
                    UserSubtopicProgress.user_id == user_id,
                    UserSubtopicProgress.next_review_at <= now,
                    UserSubtopicProgress.mastery_level.in_([
                        MasteryLevel.IN_PROGRESS,
                        MasteryLevel.NEEDS_REVIEW,
                    ])
                )
            )
            .order_by(UserSubtopicProgress.next_review_at)
            .limit(limit)
        )
        return result.scalars().all()


class LearningSessionDAO:
    """Data access object for LearningSession operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_session(self, **kwargs: Any) -> LearningSession:
        """Create a new learning session."""
        session = LearningSession(**kwargs)
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return session
    
    async def get_session(self, session_id: uuid.UUID) -> LearningSession | None:
        """Get a learning session by ID."""
        result = await self.session.execute(
            select(LearningSession).where(LearningSession.id == session_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_sessions(
        self,
        user_id: uuid.UUID,
        limit: int = 20,
    ) -> Sequence[LearningSession]:
        """Get recent learning sessions for a user."""
        result = await self.session.execute(
            select(LearningSession)
            .where(LearningSession.user_id == user_id)
            .order_by(desc(LearningSession.started_at))
            .limit(limit)
        )
        return result.scalars().all()
    
    async def update_session(
        self,
        session_id: uuid.UUID,
        **kwargs: Any,
    ) -> LearningSession | None:
        """Update a learning session."""
        result = await self.session.execute(
            update(LearningSession)
            .where(LearningSession.id == session_id)
            .values(**kwargs)
            .returning(LearningSession)
        )
        session = result.scalar_one_or_none()
        if session:
            await self.session.commit()
        return session


class DailyFeedDAO:
    """Data access object for DailyFeed operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_feed(self, **kwargs: Any) -> DailyFeed:
        """Create a new daily feed entry."""
        feed = DailyFeed(**kwargs)
        self.session.add(feed)
        await self.session.commit()
        await self.session.refresh(feed)
        return feed
    
    async def get_user_feed_for_date(
        self,
        user_id: uuid.UUID,
        feed_date: datetime,
    ) -> DailyFeed | None:
        """Get user's feed for a specific date."""
        result = await self.session.execute(
            select(DailyFeed)
            .options(joinedload(DailyFeed.subtopic))
            .where(
                and_(
                    DailyFeed.user_id == user_id,
                    func.date(DailyFeed.feed_date) == feed_date.date(),
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_feed_history(
        self,
        user_id: uuid.UUID,
        days: int = 30,
    ) -> Sequence[DailyFeed]:
        """Get user's feed history."""
        start_date = datetime.utcnow() - timedelta(days=days)
        result = await self.session.execute(
            select(DailyFeed)
            .options(joinedload(DailyFeed.subtopic))
            .where(
                and_(
                    DailyFeed.user_id == user_id,
                    DailyFeed.feed_date >= start_date,
                )
            )
            .order_by(desc(DailyFeed.feed_date))
        )
        return result.scalars().all()
    
    async def update_feed(
        self,
        feed_id: uuid.UUID,
        **kwargs: Any,
    ) -> DailyFeed | None:
        """Update a daily feed entry."""
        result = await self.session.execute(
            update(DailyFeed)
            .where(DailyFeed.id == feed_id)
            .values(**kwargs)
            .returning(DailyFeed)
        )
        feed = result.scalar_one_or_none()
        if feed:
            await self.session.commit()
        return feed
    
    async def get_user_streak(self, user_id: uuid.UUID) -> int:
        """Calculate user's current learning streak."""
        result = await self.session.execute(
            text("""
                WITH RECURSIVE streak_calc AS (
                    SELECT 
                        feed_date::date as date,
                        is_completed,
                        ROW_NUMBER() OVER (ORDER BY feed_date::date DESC) as rn
                    FROM daily_feeds 
                    WHERE user_id = :user_id 
                        AND feed_date::date <= CURRENT_DATE
                    ORDER BY feed_date::date DESC
                ),
                consecutive_days AS (
                    SELECT 
                        date,
                        is_completed,
                        rn,
                        CASE WHEN is_completed THEN 1 ELSE 0 END as streak_day
                    FROM streak_calc
                    WHERE rn = 1 AND is_completed
                    
                    UNION ALL
                    
                    SELECT 
                        s.date,
                        s.is_completed,
                        s.rn,
                        CASE WHEN s.is_completed AND s.date = c.date - INTERVAL '1 day'
                             THEN c.streak_day + 1 
                             ELSE 0 END
                    FROM streak_calc s
                    JOIN consecutive_days c ON s.rn = c.rn + 1
                    WHERE s.is_completed AND s.date = c.date - INTERVAL '1 day'
                )
                SELECT COALESCE(MAX(streak_day), 0) as streak
                FROM consecutive_days
            """),
            {"user_id": user_id}
        )
        return result.scalar() or 0


class GeneratedContentDAO:
    """Data access object for GeneratedContent operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def create_content(self, **kwargs: Any) -> GeneratedContent:
        """Create new generated content."""
        content = GeneratedContent(**kwargs)
        self.session.add(content)
        await self.session.commit()
        await self.session.refresh(content)
        return content
    
    async def get_content_by_subtopic(
        self,
        subtopic_id: uuid.UUID,
        content_type: str | None = None,
        is_active: bool = True,
    ) -> Sequence[GeneratedContent]:
        """Get generated content for a subtopic."""
        query = select(GeneratedContent).where(
            GeneratedContent.subtopic_id == subtopic_id
        )
        
        if content_type:
            query = query.where(GeneratedContent.content_type == content_type)
        if is_active is not None:
            query = query.where(GeneratedContent.is_active == is_active)
        
        query = query.order_by(desc(GeneratedContent.created_at))
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_content(self, content_id: uuid.UUID) -> GeneratedContent | None:
        """Get generated content by ID."""
        result = await self.session.execute(
            select(GeneratedContent).where(GeneratedContent.id == content_id)
        )
        return result.scalar_one_or_none()


class LearningDAO:
    """Combined DAO for all learning operations."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.topics = TopicDAO(session)
        self.subtopics = SubtopicDAO(session)
        self.user_topics = UserTopicDAO(session)
        self.progress = UserProgressDAO(session)
        self.sessions = LearningSessionDAO(session)
        self.feeds = DailyFeedDAO(session)
        self.content = GeneratedContentDAO(session)
        self.session = session