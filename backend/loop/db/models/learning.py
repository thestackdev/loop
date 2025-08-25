"""Core learning system database models."""
import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loop.db.base import Base

if TYPE_CHECKING:
    from loop.db.models.users import User


class MasteryLevel(enum.Enum):
    """Mastery level for a subtopic."""
    
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    NEEDS_REVIEW = "needs_review"
    MASTERED = "mastered"
    EXPERT = "expert"


class ContentType(enum.Enum):
    """Type of learning content."""
    
    ARTICLE = "article"
    FLASHCARD = "flashcard"
    QUIZ = "quiz"
    MNEMONIC = "mnemonic"


class LearningSessionType(enum.Enum):
    """Type of learning session."""
    
    READING = "reading"
    FLASHCARD_PRACTICE = "flashcard_practice"
    QUIZ_ATTEMPT = "quiz_attempt"
    REVIEW = "review"


class Topic(Base):
    """Main topic/domain for learning."""
    
    __tablename__ = "topics"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    importance_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="medium",
    )
    estimated_subtopics: Mapped[int] = mapped_column(Integer, default=10)
    icon_emoji: Mapped[str | None] = mapped_column(String(10))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    
    # Relationships
    subtopics: Mapped[list["Subtopic"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
    )
    user_topics: Mapped[list["UserTopic"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
    )


class Subtopic(Base):
    """Subtopic within a main topic."""
    
    __tablename__ = "subtopics"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_time_minutes: Mapped[int] = mapped_column(Integer, default=15)
    prerequisites: Mapped[list[uuid.UUID] | None] = mapped_column(
        JSON,
        default=list,
    )
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    
    # Relationships
    topic: Mapped["Topic"] = relationship(back_populates="subtopics")
    user_progress: Mapped[list["UserSubtopicProgress"]] = relationship(
        back_populates="subtopic",
        cascade="all, delete-orphan",
    )
    content: Mapped[list["GeneratedContent"]] = relationship(
        back_populates="subtopic",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        UniqueConstraint("topic_id", "name", name="uq_topic_subtopic_name"),
        UniqueConstraint("topic_id", "order_index", name="uq_topic_subtopic_order"),
    )


class UserTopic(Base):
    """User's selected topics and preferences."""
    
    __tablename__ = "user_topics"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
    )
    priority_order: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    current_subtopic_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subtopics.id", ondelete="SET NULL"),
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    
    # Relationships
    user: Mapped["User"] = relationship()
    topic: Mapped["Topic"] = relationship(back_populates="user_topics")
    current_subtopic: Mapped["Subtopic | None"] = relationship()
    
    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="uq_user_topic"),
    )


class UserSubtopicProgress(Base):
    """Track user's progress on each subtopic."""
    
    __tablename__ = "user_subtopic_progress"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    subtopic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        nullable=False,
    )
    mastery_level: Mapped[MasteryLevel] = mapped_column(
        Enum(MasteryLevel),
        default=MasteryLevel.NOT_STARTED,
    )
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0)
    article_read: Mapped[bool] = mapped_column(Boolean, default=False)
    flashcard_success_rate: Mapped[float] = mapped_column(Float, default=0.0)
    quiz_best_score: Mapped[float] = mapped_column(Float, default=0.0)
    quiz_attempts: Mapped[int] = mapped_column(Integer, default=0)
    total_time_spent_minutes: Mapped[int] = mapped_column(Integer, default=0)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    next_review_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    
    # Spaced repetition fields
    repetition_interval_days: Mapped[int] = mapped_column(Integer, default=1)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    consecutive_correct: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    user: Mapped["User"] = relationship()
    subtopic: Mapped["Subtopic"] = relationship(back_populates="user_progress")
    sessions: Mapped[list["LearningSession"]] = relationship(
        back_populates="progress",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        UniqueConstraint("user_id", "subtopic_id", name="uq_user_subtopic"),
    )


class GeneratedContent(Base):
    """AI-generated content for learning."""
    
    __tablename__ = "generated_content"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    subtopic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        nullable=False,
    )
    content_type: Mapped[ContentType] = mapped_column(
        Enum(ContentType),
        nullable=False,
    )
    content_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)
    version: Mapped[int] = mapped_column(Integer, default=1)
    ai_model: Mapped[str] = mapped_column(String(100))
    prompt_template: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    
    # Relationships
    subtopic: Mapped["Subtopic"] = relationship(back_populates="content")


class LearningSession(Base):
    """Track individual learning sessions."""
    
    __tablename__ = "learning_sessions"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    progress_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_subtopic_progress.id", ondelete="CASCADE"),
        nullable=False,
    )
    session_type: Mapped[LearningSessionType] = mapped_column(
        Enum(LearningSessionType),
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    performance_data: Mapped[dict | None] = mapped_column(JSON)
    
    # Relationships
    user: Mapped["User"] = relationship()
    progress: Mapped["UserSubtopicProgress"] = relationship(back_populates="sessions")
    flashcard_attempts: Mapped[list["FlashcardAttempt"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


class FlashcardAttempt(Base):
    """Track flashcard practice attempts."""
    
    __tablename__ = "flashcard_attempts"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learning_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    content_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("generated_content.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    response_time_seconds: Mapped[int | None] = mapped_column(Integer)
    user_answer: Mapped[str | None] = mapped_column(Text)
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    
    # Relationships
    session: Mapped["LearningSession"] = relationship(back_populates="flashcard_attempts")
    content: Mapped["GeneratedContent"] = relationship()


class QuizAttempt(Base):
    """Track quiz attempts."""
    
    __tablename__ = "quiz_attempts"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learning_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    content_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("generated_content.id", ondelete="CASCADE"),
        nullable=False,
    )
    score: Mapped[float] = mapped_column(Float, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False)
    time_taken_minutes: Mapped[int | None] = mapped_column(Integer)
    answers_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    
    # Relationships
    session: Mapped["LearningSession"] = relationship(back_populates="quiz_attempts")
    content: Mapped["GeneratedContent"] = relationship()


class DailyFeed(Base):
    """Daily learning feed for users."""
    
    __tablename__ = "daily_feeds"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    subtopic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        nullable=False,
    )
    feed_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    
    # Relationships
    user: Mapped["User"] = relationship()
    subtopic: Mapped["Subtopic"] = relationship()
    
    __table_args__ = (
        UniqueConstraint("user_id", "feed_date", name="uq_user_feed_date"),
    )