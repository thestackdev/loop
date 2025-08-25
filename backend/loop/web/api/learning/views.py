"""Learning system API views."""
import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from loop.db.dao.learning_dao import LearningDAO
from loop.db.dependencies import get_db_session
from loop.db.models.users import User, current_active_user
from loop.web.api.learning.schema import (
    DailyFeedRead,
    GeneratedContentCreate,
    GeneratedContentRead,
    GeneratedContentUpdate,
    LearningSessionCreate,
    LearningSessionRead,
    LearningSessionUpdate,
    SubtopicCreate,
    SubtopicRead,
    SubtopicUpdate,
    TopicCreate,
    TopicProgress,
    TopicRead,
    TopicUpdate,
    UserDashboard,
    UserSubtopicProgressCreate,
    UserSubtopicProgressRead,
    UserSubtopicProgressUpdate,
    UserTopicCreate,
    UserTopicRead,
    UserTopicUpdate,
)

router = APIRouter()


# Topic management endpoints
@router.post("/topics", response_model=TopicRead)
async def create_topic(
    topic_data: TopicCreate,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Create a new topic."""
    dao = LearningDAO(session)
    return await dao.topics.create_topic(**topic_data.model_dump())


@router.get("/topics", response_model=list[TopicRead])
async def get_topics(
    category: str | None = Query(None, description="Filter by category"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    limit: int = Query(100, ge=1, le=200, description="Number of topics to return"),
    offset: int = Query(0, ge=0, description="Number of topics to skip"),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get all topics with optional filters."""
    dao = LearningDAO(session)
    return await dao.topics.get_topics(
        category=category,
        is_active=is_active,
        limit=limit,
        offset=offset,
    )


@router.get("/topics/{topic_id}", response_model=TopicRead)
async def get_topic(
    topic_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get a specific topic."""
    dao = LearningDAO(session)
    topic = await dao.topics.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/topics/{topic_id}", response_model=TopicRead)
async def update_topic(
    topic_id: uuid.UUID,
    topic_data: TopicUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Update a topic."""
    dao = LearningDAO(session)
    topic = await dao.topics.update_topic(
        topic_id, 
        **topic_data.model_dump(exclude_unset=True)
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.delete("/topics/{topic_id}")
async def delete_topic(
    topic_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """Delete a topic."""
    dao = LearningDAO(session)
    success = await dao.topics.delete_topic(topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"message": "Topic deleted successfully"}


# Subtopic management endpoints
@router.post("/topics/{topic_id}/subtopics", response_model=SubtopicRead)
async def create_subtopic(
    topic_id: uuid.UUID,
    subtopic_data: SubtopicCreate,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Create a new subtopic for a topic."""
    dao = LearningDAO(session)
    
    # Verify topic exists
    topic = await dao.topics.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Create subtopic
    subtopic_dict = subtopic_data.model_dump()
    subtopic_dict["topic_id"] = topic_id
    return await dao.subtopics.create_subtopic(**subtopic_dict)


@router.get("/topics/{topic_id}/subtopics", response_model=list[SubtopicRead])
async def get_subtopics(
    topic_id: uuid.UUID,
    is_active: bool | None = Query(None, description="Filter by active status"),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get all subtopics for a topic."""
    dao = LearningDAO(session)
    return await dao.subtopics.get_subtopics_by_topic(topic_id, is_active)


@router.get("/subtopics/{subtopic_id}", response_model=SubtopicRead)
async def get_subtopic(
    subtopic_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get a specific subtopic."""
    dao = LearningDAO(session)
    subtopic = await dao.subtopics.get_subtopic(subtopic_id)
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return subtopic


@router.put("/subtopics/{subtopic_id}", response_model=SubtopicRead)
async def update_subtopic(
    subtopic_id: uuid.UUID,
    subtopic_data: SubtopicUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Update a subtopic."""
    dao = LearningDAO(session)
    subtopic = await dao.subtopics.update_subtopic(
        subtopic_id,
        **subtopic_data.model_dump(exclude_unset=True)
    )
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return subtopic


@router.delete("/subtopics/{subtopic_id}")
async def delete_subtopic(
    subtopic_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """Delete a subtopic."""
    dao = LearningDAO(session)
    success = await dao.subtopics.delete_subtopic(subtopic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subtopic not found")
    return {"message": "Subtopic deleted successfully"}


# User topic management endpoints
@router.post("/user/topics", response_model=UserTopicRead)
async def subscribe_to_topic(
    topic_data: UserTopicCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Subscribe user to a topic."""
    dao = LearningDAO(session)
    
    # Verify topic exists
    topic = await dao.topics.get_topic(topic_data.topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Check if user is already subscribed
    existing = await dao.user_topics.get_user_topic(
        current_user.id, topic_data.topic_id
    )
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="User already subscribed to this topic"
        )
    
    # Create subscription
    user_topic_dict = topic_data.model_dump()
    user_topic_dict["user_id"] = current_user.id
    return await dao.user_topics.create_user_topic(**user_topic_dict)


@router.get("/user/topics", response_model=list[UserTopicRead])
async def get_user_topics(
    is_active: bool | None = Query(None, description="Filter by active status"),
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get all topics for the current user."""
    dao = LearningDAO(session)
    return await dao.user_topics.get_user_topics(current_user.id, is_active)


@router.put("/user/topics/{topic_id}", response_model=UserTopicRead)
async def update_user_topic(
    topic_id: uuid.UUID,
    topic_data: UserTopicUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Update user's topic settings."""
    dao = LearningDAO(session)
    user_topic = await dao.user_topics.update_user_topic(
        current_user.id,
        topic_id,
        **topic_data.model_dump(exclude_unset=True)
    )
    if not user_topic:
        raise HTTPException(status_code=404, detail="User topic not found")
    return user_topic


# Progress tracking endpoints
@router.get("/user/progress/{subtopic_id}", response_model=UserSubtopicProgressRead)
async def get_user_progress(
    subtopic_id: uuid.UUID,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get user's progress for a subtopic."""
    dao = LearningDAO(session)
    progress = await dao.progress.get_progress(current_user.id, subtopic_id)
    if not progress:
        # Create initial progress if it doesn't exist
        progress = await dao.progress.create_progress(
            user_id=current_user.id,
            subtopic_id=subtopic_id,
        )
    return progress


@router.put("/user/progress/{subtopic_id}", response_model=UserSubtopicProgressRead)
async def update_user_progress(
    subtopic_id: uuid.UUID,
    progress_data: UserSubtopicProgressUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Update user's progress for a subtopic."""
    dao = LearningDAO(session)
    progress = await dao.progress.update_progress(
        current_user.id,
        subtopic_id,
        **progress_data.model_dump(exclude_unset=True)
    )
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return progress


@router.get("/user/progress/topic/{topic_id}", response_model=list[UserSubtopicProgressRead])
async def get_topic_progress(
    topic_id: uuid.UUID,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get user's progress for all subtopics in a topic."""
    dao = LearningDAO(session)
    return await dao.progress.get_user_progress_by_topic(current_user.id, topic_id)


@router.get("/user/reviews", response_model=list[UserSubtopicProgressRead])
async def get_due_reviews(
    limit: int = Query(10, ge=1, le=50, description="Number of reviews to return"),
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get subtopics due for review."""
    dao = LearningDAO(session)
    return await dao.progress.get_due_reviews(current_user.id, limit)


# Learning session endpoints
@router.post("/sessions", response_model=LearningSessionRead)
async def start_learning_session(
    session_data: LearningSessionCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Start a new learning session."""
    dao = LearningDAO(session)
    
    # Verify progress exists
    progress = await dao.progress.get_progress(
        current_user.id,
        session_data.progress_id,  # This should be subtopic_id in the schema
    )
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Create session
    session_dict = session_data.model_dump()
    session_dict["user_id"] = current_user.id
    session_dict["progress_id"] = progress.id  # Use actual progress ID
    return await dao.sessions.create_session(**session_dict)


@router.put("/sessions/{session_id}", response_model=LearningSessionRead)
async def update_learning_session(
    session_id: uuid.UUID,
    session_data: LearningSessionUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Update a learning session."""
    dao = LearningDAO(session)
    
    # Verify session belongs to user
    session_obj = await dao.sessions.get_session(session_id)
    if not session_obj or session_obj.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    updated_session = await dao.sessions.update_session(
        session_id,
        **session_data.model_dump(exclude_unset=True)
    )
    return updated_session


@router.get("/user/sessions", response_model=list[LearningSessionRead])
async def get_user_sessions(
    limit: int = Query(20, ge=1, le=100, description="Number of sessions to return"),
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get user's recent learning sessions."""
    dao = LearningDAO(session)
    return await dao.sessions.get_user_sessions(current_user.id, limit)


# Content generation endpoints
@router.post("/subtopics/{subtopic_id}/generate-content")
async def generate_learning_content(
    subtopic_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """Generate complete learning content for a subtopic."""
    from loop.services.learning.ai_content import ContentWorkflowService
    
    workflow_service = ContentWorkflowService(session)
    
    try:
        results = await workflow_service.generate_complete_learning_content(subtopic_id)
        return {
            "message": "Content generation completed",
            "generated": ", ".join(results.keys()),
            "subtopic_id": str(subtopic_id),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")


@router.post("/feeds/generate")
async def generate_daily_feed(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Generate today's learning feed for the current user."""
    from loop.services.learning.feed_generator import FeedGenerationService
    
    feed_service = FeedGenerationService(session)
    feed = await feed_service.generate_daily_feed(current_user.id)
    
    if not feed:
        return {
            "message": "No active topics found. Please subscribe to topics first.",
            "feed": None,
        }
    
    return {
        "message": "Daily feed generated successfully",
        "feed_id": str(feed.id),
        "subtopic_id": str(feed.subtopic_id),
    }


@router.put("/feeds/{feed_id}/complete")
async def complete_daily_feed(
    feed_id: uuid.UUID,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    """Mark a daily feed as completed."""
    from loop.services.learning.feed_generator import FeedGenerationService
    
    feed_service = FeedGenerationService(session)
    success = await feed_service.mark_feed_completed(current_user.id, feed_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Feed not found")
    
    return {"message": "Feed marked as completed"}


# Daily feed endpoints
@router.get("/user/feed/today", response_model=DailyFeedRead | None)
async def get_today_feed(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get user's feed for today."""
    dao = LearningDAO(session)
    return await dao.feeds.get_user_feed_for_date(
        current_user.id,
        datetime.utcnow(),
    )


@router.get("/user/feed/history", response_model=list[DailyFeedRead])
async def get_feed_history(
    days: int = Query(30, ge=1, le=90, description="Number of days to retrieve"),
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get user's feed history."""
    dao = LearningDAO(session)
    return await dao.feeds.get_user_feed_history(current_user.id, days)


@router.get("/user/streak", response_model=dict[str, int])
async def get_user_streak(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, int]:
    """Get user's current learning streak."""
    dao = LearningDAO(session)
    streak = await dao.feeds.get_user_streak(current_user.id)
    return {"streak_days": streak}


# Generated content endpoints
@router.post("/content", response_model=GeneratedContentRead)
async def create_content(
    content_data: GeneratedContentCreate,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Create new generated content."""
    dao = LearningDAO(session)
    return await dao.content.create_content(**content_data.model_dump())


@router.get("/subtopics/{subtopic_id}/content", response_model=list[GeneratedContentRead])
async def get_subtopic_content(
    subtopic_id: uuid.UUID,
    content_type: str | None = Query(None, description="Filter by content type"),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get generated content for a subtopic."""
    dao = LearningDAO(session)
    return await dao.content.get_content_by_subtopic(
        subtopic_id,
        content_type,
    )


@router.get("/content/{content_id}", response_model=GeneratedContentRead)
async def get_content(
    content_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get specific generated content."""
    dao = LearningDAO(session)
    content = await dao.content.get_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


# Dashboard endpoint
@router.get("/user/dashboard", response_model=UserDashboard)
async def get_user_dashboard(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get user's learning dashboard data."""
    dao = LearningDAO(session)
    
    # Get active topics
    active_topics = await dao.user_topics.get_user_topics(
        current_user.id, is_active=True
    )
    
    # Get today's feed
    today_feed = await dao.feeds.get_user_feed_for_date(
        current_user.id,
        datetime.utcnow(),
    )
    
    # Get streak
    streak = await dao.feeds.get_user_streak(current_user.id)
    
    # Get recent sessions
    recent_sessions = await dao.sessions.get_user_sessions(current_user.id, 5)
    
    # Calculate stats (placeholder - would need more complex queries)
    total_mastered = 0  # Count of mastered subtopics
    total_time_hours = 0.0  # Total time spent learning
    
    return UserDashboard(
        active_topics=active_topics,
        today_feed=today_feed,
        streak_days=streak,
        total_mastered_subtopics=total_mastered,
        total_time_spent_hours=total_time_hours,
        recent_sessions=recent_sessions,
    )


# Topic progress summary endpoint
@router.get("/user/topics/{topic_id}/progress", response_model=TopicProgress)
async def get_topic_progress_summary(
    topic_id: uuid.UUID,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_db_session),
) -> Any:
    """Get progress summary for a topic."""
    dao = LearningDAO(session)
    
    # Get topic
    topic = await dao.topics.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Get subtopics
    subtopics = await dao.subtopics.get_subtopics_by_topic(topic_id, is_active=True)
    
    # Get progress for all subtopics
    progress_list = await dao.progress.get_user_progress_by_topic(
        current_user.id, topic_id
    )
    
    # Calculate stats
    total_subtopics = len(subtopics)
    completed_count = sum(1 for p in progress_list if p.completed_at is not None)
    mastered_count = sum(
        1 for p in progress_list 
        if p.mastery_level.value in ["mastered", "expert"]
    )
    
    progress_percentage = (completed_count / total_subtopics * 100) if total_subtopics > 0 else 0
    
    # Find current subtopic (next incomplete one)
    current_subtopic = None
    for subtopic in subtopics:
        progress = next((p for p in progress_list if p.subtopic_id == subtopic.id), None)
        if not progress or progress.completed_at is None:
            current_subtopic = subtopic
            break
    
    return TopicProgress(
        topic=topic,
        total_subtopics=total_subtopics,
        completed_subtopics=completed_count,
        mastered_subtopics=mastered_count,
        current_subtopic=current_subtopic,
        progress_percentage=progress_percentage,
        estimated_completion_days=None,  # Would need more complex calculation
    )