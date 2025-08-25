"""Learning system Pydantic schemas."""
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from loop.db.models.learning import (
    ContentType,
    LearningSessionType,
    MasteryLevel,
)


# Topic schemas
class TopicBase(BaseModel):
    """Base topic schema."""
    
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=100)
    importance_level: str = Field(default="medium", max_length=50)
    estimated_subtopics: int = Field(default=10, ge=1)
    icon_emoji: str | None = Field(None, max_length=10)
    is_active: bool = True


class TopicCreate(TopicBase):
    """Schema for creating a topic."""
    pass


class TopicUpdate(BaseModel):
    """Schema for updating a topic."""
    
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, min_length=1)
    category: str | None = Field(None, min_length=1, max_length=100)
    importance_level: str | None = Field(None, max_length=50)
    estimated_subtopics: int | None = Field(None, ge=1)
    icon_emoji: str | None = Field(None, max_length=10)
    is_active: bool | None = None


class TopicRead(TopicBase):
    """Schema for reading a topic."""
    
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Subtopic schemas
class SubtopicBase(BaseModel):
    """Base subtopic schema."""
    
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    order_index: int = Field(..., ge=0)
    estimated_time_minutes: int = Field(default=15, ge=1, le=240)
    prerequisites: list[uuid.UUID] = Field(default_factory=list)
    difficulty_level: int = Field(default=1, ge=1, le=5)
    is_active: bool = True


class SubtopicCreate(SubtopicBase):
    """Schema for creating a subtopic."""
    pass


class SubtopicUpdate(BaseModel):
    """Schema for updating a subtopic."""
    
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, min_length=1)
    order_index: int | None = Field(None, ge=0)
    estimated_time_minutes: int | None = Field(None, ge=1, le=240)
    prerequisites: list[uuid.UUID] | None = None
    difficulty_level: int | None = Field(None, ge=1, le=5)
    is_active: bool | None = None


class SubtopicRead(SubtopicBase):
    """Schema for reading a subtopic."""
    
    id: uuid.UUID
    topic_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


# User topic schemas
class UserTopicBase(BaseModel):
    """Base user topic schema."""
    
    priority_order: int = Field(default=1, ge=1)
    is_active: bool = True


class UserTopicCreate(UserTopicBase):
    """Schema for creating a user topic."""
    
    topic_id: uuid.UUID


class UserTopicUpdate(BaseModel):
    """Schema for updating a user topic."""
    
    priority_order: int | None = Field(None, ge=1)
    is_active: bool | None = None
    current_subtopic_id: uuid.UUID | None = None


class UserTopicRead(UserTopicBase):
    """Schema for reading a user topic."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    topic_id: uuid.UUID
    current_subtopic_id: uuid.UUID | None
    started_at: datetime
    completed_at: datetime | None
    topic: TopicRead
    
    class Config:
        from_attributes = True


# Progress schemas
class UserSubtopicProgressBase(BaseModel):
    """Base user subtopic progress schema."""
    
    mastery_level: MasteryLevel = MasteryLevel.NOT_STARTED
    mastery_score: float = Field(default=0.0, ge=0.0, le=1.0)
    article_read: bool = False
    flashcard_success_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    quiz_best_score: float = Field(default=0.0, ge=0.0, le=1.0)
    quiz_attempts: int = Field(default=0, ge=0)
    total_time_spent_minutes: int = Field(default=0, ge=0)


class UserSubtopicProgressCreate(UserSubtopicProgressBase):
    """Schema for creating user subtopic progress."""
    
    subtopic_id: uuid.UUID


class UserSubtopicProgressUpdate(BaseModel):
    """Schema for updating user subtopic progress."""
    
    mastery_level: MasteryLevel | None = None
    mastery_score: float | None = Field(None, ge=0.0, le=1.0)
    article_read: bool | None = None
    flashcard_success_rate: float | None = Field(None, ge=0.0, le=1.0)
    quiz_best_score: float | None = Field(None, ge=0.0, le=1.0)
    quiz_attempts: int | None = Field(None, ge=0)
    total_time_spent_minutes: int | None = Field(None, ge=0)
    last_reviewed_at: datetime | None = None
    next_review_at: datetime | None = None


class UserSubtopicProgressRead(UserSubtopicProgressBase):
    """Schema for reading user subtopic progress."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    subtopic_id: uuid.UUID
    last_reviewed_at: datetime | None
    next_review_at: datetime | None
    started_at: datetime
    completed_at: datetime | None
    repetition_interval_days: int
    ease_factor: float
    consecutive_correct: int
    subtopic: SubtopicRead
    
    class Config:
        from_attributes = True


# Generated content schemas
class GeneratedContentBase(BaseModel):
    """Base generated content schema."""
    
    content_type: ContentType
    content_data: dict[str, Any]
    difficulty_level: int = Field(default=1, ge=1, le=5)
    version: int = Field(default=1, ge=1)
    ai_model: str | None = None
    prompt_template: str | None = None
    is_active: bool = True


class GeneratedContentCreate(GeneratedContentBase):
    """Schema for creating generated content."""
    
    subtopic_id: uuid.UUID


class GeneratedContentUpdate(BaseModel):
    """Schema for updating generated content."""
    
    content_data: dict[str, Any] | None = None
    difficulty_level: int | None = Field(None, ge=1, le=5)
    ai_model: str | None = None
    prompt_template: str | None = None
    is_active: bool | None = None


class GeneratedContentRead(GeneratedContentBase):
    """Schema for reading generated content."""
    
    id: uuid.UUID
    subtopic_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


# Learning session schemas
class LearningSessionBase(BaseModel):
    """Base learning session schema."""
    
    session_type: LearningSessionType
    duration_minutes: int | None = Field(None, ge=1)
    performance_data: dict[str, Any] | None = None


class LearningSessionCreate(LearningSessionBase):
    """Schema for creating a learning session."""
    
    progress_id: uuid.UUID


class LearningSessionUpdate(BaseModel):
    """Schema for updating a learning session."""
    
    completed_at: datetime | None = None
    duration_minutes: int | None = Field(None, ge=1)
    performance_data: dict[str, Any] | None = None


class LearningSessionRead(LearningSessionBase):
    """Schema for reading a learning session."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    progress_id: uuid.UUID
    started_at: datetime
    completed_at: datetime | None
    
    class Config:
        from_attributes = True


# Flashcard attempt schemas
class FlashcardAttemptBase(BaseModel):
    """Base flashcard attempt schema."""
    
    is_correct: bool
    response_time_seconds: int | None = Field(None, ge=1)
    user_answer: str | None = None


class FlashcardAttemptCreate(FlashcardAttemptBase):
    """Schema for creating a flashcard attempt."""
    
    session_id: uuid.UUID
    content_id: uuid.UUID


class FlashcardAttemptRead(FlashcardAttemptBase):
    """Schema for reading a flashcard attempt."""
    
    id: uuid.UUID
    session_id: uuid.UUID
    content_id: uuid.UUID
    attempted_at: datetime
    
    class Config:
        from_attributes = True


# Quiz attempt schemas
class QuizAttemptBase(BaseModel):
    """Base quiz attempt schema."""
    
    score: float = Field(..., ge=0.0, le=1.0)
    total_questions: int = Field(..., ge=1)
    correct_answers: int = Field(..., ge=0)
    time_taken_minutes: int | None = Field(None, ge=1)
    answers_data: dict[str, Any]
    attempt_number: int = Field(default=1, ge=1)


class QuizAttemptCreate(QuizAttemptBase):
    """Schema for creating a quiz attempt."""
    
    session_id: uuid.UUID
    content_id: uuid.UUID


class QuizAttemptRead(QuizAttemptBase):
    """Schema for reading a quiz attempt."""
    
    id: uuid.UUID
    session_id: uuid.UUID
    content_id: uuid.UUID
    completed_at: datetime
    
    class Config:
        from_attributes = True


# Daily feed schemas
class DailyFeedBase(BaseModel):
    """Base daily feed schema."""
    
    feed_date: datetime
    is_completed: bool = False


class DailyFeedCreate(DailyFeedBase):
    """Schema for creating a daily feed."""
    
    subtopic_id: uuid.UUID


class DailyFeedUpdate(BaseModel):
    """Schema for updating a daily feed."""
    
    is_completed: bool | None = None
    completed_at: datetime | None = None


class DailyFeedRead(DailyFeedBase):
    """Schema for reading a daily feed."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    subtopic_id: uuid.UUID
    completed_at: datetime | None
    created_at: datetime
    subtopic: SubtopicRead
    
    class Config:
        from_attributes = True


# Aggregated schemas for dashboard
class UserDashboard(BaseModel):
    """User dashboard data."""
    
    active_topics: list[UserTopicRead]
    today_feed: DailyFeedRead | None
    streak_days: int
    total_mastered_subtopics: int
    total_time_spent_hours: float
    recent_sessions: list[LearningSessionRead]


class TopicProgress(BaseModel):
    """Topic progress summary."""
    
    topic: TopicRead
    total_subtopics: int
    completed_subtopics: int
    mastered_subtopics: int
    current_subtopic: SubtopicRead | None
    progress_percentage: float
    estimated_completion_days: int | None