# 🎯 Frontend Learning Flow - API Sequence & Mental Model

## 📋 Overview

This document outlines the complete learning journey from a frontend perspective, detailing every API call, database interaction, and the ideal user experience flow for the Adaptive Daily Tech Learning System.

---

## 🔄 Complete Learning Journey

### Phase 1: User Onboarding & Setup

#### 1.1 Initial Authentication Flow
```mermaid
sequenceDiagram
    participant F as Frontend
    participant A as Auth API
    participant DB as Database
    
    F->>A: POST /auth/register
    A->>DB: Create user record
    DB-->>A: User created
    A-->>F: User token + profile
    
    F->>A: POST /auth/login
    A->>DB: Validate credentials
    DB-->>A: User data
    A-->>F: JWT token + user info
```

**API Calls:**
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Authenticate existing user

**Purpose:** Establish user identity and session management

**Database Impact:** Creates/validates `users` table record

---

#### 1.2 Topic Selection & Subscription
```mermaid
sequenceDiagram
    participant F as Frontend
    participant L as Learning API
    participant DB as Database
    
    F->>L: GET /topics
    L->>DB: Fetch all available topics
    DB-->>L: Topic list with metadata
    L-->>F: Available topics for selection
    
    F->>L: POST /user/topics (selected topics)
    L->>DB: Create user_topics subscriptions
    DB-->>L: Subscription records created
    L-->>F: User topic preferences saved
```

**API Calls:**
- `GET /topics` - Fetch all available learning topics
- `POST /user/topics` - Subscribe user to selected topics

**Purpose:** Allow users to choose their learning domains

**Database Impact:** 
- Reads from `topics` table
- Creates records in `user_topics` table

---

### Phase 2: Daily Learning Experience

#### 2.1 Dashboard Load & Today's Feed
```mermaid
sequenceDiagram
    participant F as Frontend
    participant L as Learning API
    participant AI as AI Service
    participant DB as Database
    
    F->>L: GET /user/dashboard
    L->>DB: Get user stats, progress, streaks
    DB-->>L: Aggregated user data
    L-->>F: Dashboard metrics
    
    F->>L: GET /user/feed/today
    L->>DB: Check for existing daily feed
    alt No feed exists
        L->>AI: Generate daily learning content
        AI-->>L: Generated article + metadata
        L->>DB: Store daily feed record
    end
    DB-->>L: Today's learning content
    L-->>F: Daily feed with article
```

**API Calls:**
- `GET /user/dashboard` - Load user progress overview
- `GET /user/feed/today` - Get today's personalized learning content

**Purpose:** Show user's learning state and provide daily content

**Database Impact:**
- Reads from `users`, `user_topics`, `user_subtopic_progress`, `learning_sessions`
- May create `daily_feeds` record if none exists

---

#### 2.2 Article Reading Experience
```mermaid
sequenceDiagram
    participant F as Frontend
    participant L as Learning API
    participant DB as Database
    
    F->>L: POST /sessions (start reading)
    L->>DB: Create learning session record
    DB-->>L: Session ID created
    L-->>F: Session tracking initiated
    
    Note over F: User reads article content
    
    F->>L: PUT /sessions/{session_id} (reading complete)
    L->>DB: Update session with completion time
    DB-->>L: Session updated
    L-->>F: Reading phase completed
```

**API Calls:**
- `POST /sessions` - Start learning session tracking
- `PUT /sessions/{session_id}` - Mark article as read

**Purpose:** Track reading engagement and completion

**Database Impact:**
- Creates record in `learning_sessions` table
- Updates session with completion status and time

---

#### 2.3 Flashcard Generation & Practice
```mermaid
sequenceDiagram
    participant F as Frontend
    participant L as Learning API
    participant AI as AI Service
    participant DB as Database
    
    F->>L: POST /subtopics/{subtopic_id}/generate-content
    L->>AI: Generate flashcards from article
    AI-->>L: Flashcard Q&A + mnemonics
    L->>DB: Store generated flashcards
    DB-->>L: Flashcards saved
    L-->>F: Generated flashcards ready
    
    F->>L: GET /subtopics/{subtopic_id}/content?type=flashcard
    L->>DB: Fetch flashcards for subtopic
    DB-->>L: Flashcard content
    L-->>F: Flashcards for practice
    
    loop For each flashcard attempt
        Note over F: User answers flashcard
        F->>L: PUT /user/progress/{subtopic_id}
        L->>DB: Record attempt results
        DB-->>L: Progress updated
        L-->>F: Performance feedback
    end
```

**API Calls:**
- `POST /subtopics/{subtopic_id}/generate-content` - Generate AI flashcards
- `GET /subtopics/{subtopic_id}/content` - Retrieve flashcards
- `PUT /user/progress/{subtopic_id}` - Record flashcard attempts

**Purpose:** Active recall practice with AI-generated content

**Database Impact:**
- Creates records in `generated_content` table
- Updates `user_subtopic_progress` with attempt data

---

#### 2.4 Quiz Challenge & Mastery Assessment
```mermaid
sequenceDiagram
    participant F as Frontend
    participant L as Learning API
    participant AI as AI Service
    participant DB as Database
    
    F->>L: POST /content (generate quiz)
    L->>AI: Create quiz questions (different from flashcards)
    AI-->>L: Quiz questions + answers
    L->>DB: Store quiz content
    DB-->>L: Quiz saved
    L-->>F: Quiz questions ready
    
    loop For each quiz question
        Note over F: User answers question
        F->>L: PUT /user/progress/{subtopic_id}
        L->>DB: Record quiz performance
        DB-->>L: Score calculated
        L-->>F: Immediate feedback
    end
    
    F->>L: GET /user/progress/{subtopic_id}
    L->>DB: Calculate mastery score
    DB-->>L: Overall progress metrics
    L-->>F: Mastery assessment result
```

**API Calls:**
- `POST /content` - Generate quiz questions
- `PUT /user/progress/{subtopic_id}` - Submit quiz answers
- `GET /user/progress/{subtopic_id}` - Get mastery assessment

**Purpose:** Test understanding and calculate mastery level

**Database Impact:**
- Creates quiz records in `generated_content` table
- Updates `user_subtopic_progress` with quiz scores
- Triggers mastery calculation algorithms

---

#### 2.5 Progress Update & Next Topic Selection
```mermaid
sequenceDiagram
    participant F as Frontend
    participant L as Learning API
    participant AI as AI Service
    participant DB as Database
    
    alt Mastery achieved (80%+)
        L->>DB: Mark subtopic as mastered
        L->>AI: Calculate next optimal subtopic
        AI->>DB: Analyze user progress patterns
        DB-->>AI: Learning history data
        AI-->>L: Next subtopic recommendation
        L->>DB: Update learning path
        DB-->>L: Path updated
        L-->>F: Advancement notification
    else Mastery not achieved
        L->>DB: Schedule review session
        L->>AI: Generate additional practice content
        AI-->>L: Remedial content created
        L->>DB: Store review materials
        DB-->>L: Review scheduled
        L-->>F: Additional practice required
    end
    
    F->>L: PUT /feeds/{feed_id}/complete
    L->>DB: Mark daily session complete
    DB-->>L: Session completed
    L-->>F: Daily goal achieved
```

**API Calls:**
- `PUT /feeds/{feed_id}/complete` - Mark daily learning complete
- AI-driven next topic selection (internal process)

**Purpose:** Advance learning path or schedule reviews

**Database Impact:**
- Updates `user_subtopic_progress` mastery status
- May update `user_topics` with next subtopic
- Updates `daily_feeds` completion status

---

### Phase 3: Ongoing Engagement & Analytics

#### 3.1 Spaced Repetition Reviews
```mermaid
sequenceDiagram
    participant F as Frontend
    participant L as Learning API
    participant DB as Database
    
    F->>L: GET /user/reviews
    L->>DB: Fetch due review items
    DB-->>L: Items needing review
    L-->>F: Review session content
    
    loop For each review item
        Note over F: User completes review
        F->>L: PUT /user/progress/{subtopic_id}
        L->>DB: Update spaced repetition schedule
        DB-->>L: Next review date calculated
        L-->>F: Review feedback
    end
```

**API Calls:**
- `GET /user/reviews` - Get items due for spaced repetition
- `PUT /user/progress/{subtopic_id}` - Record review performance

**Purpose:** Reinforce previously learned concepts

**Database Impact:**
- Reads from `user_subtopic_progress` where review_date <= today
- Updates review intervals based on performance

---

#### 3.2 Progress Analytics & Insights
```mermaid
sequenceDiagram
    participant F as Frontend
    participant L as Learning API
    participant DB as Database
    
    F->>L: GET /user/streak
    L->>DB: Calculate learning streak
    DB-->>L: Streak count
    L-->>F: Streak information
    
    F->>L: GET /user/topics/{topic_id}/progress
    L->>DB: Aggregate topic progress
    DB-->>L: Topic completion metrics
    L-->>F: Progress visualization data
    
    F->>L: GET /user/feed/history
    L->>DB: Fetch learning history
    DB-->>L: Past sessions data
    L-->>F: Historical performance
```

**API Calls:**
- `GET /user/streak` - Get current learning streak
- `GET /user/topics/{topic_id}/progress` - Topic-level progress
- `GET /user/feed/history` - Learning history

**Purpose:** Provide engagement insights and motivation

**Database Impact:**
- Complex queries across multiple tables for analytics
- Read-only operations for reporting

---

## 🎯 Mental Model Summary

### Core Database Relationships
```
users (1) ←→ (∞) user_topics ←→ (1) topics
topics (1) ←→ (∞) subtopics
users (1) ←→ (∞) user_subtopic_progress ←→ (1) subtopics
users (1) ←→ (∞) learning_sessions
users (1) ←→ (∞) daily_feeds
subtopics (1) ←→ (∞) generated_content
```

### Key State Transitions
1. **Unsubscribed** → Topic Selection → **Subscribed**
2. **New Subtopic** → Article Reading → **Reading Complete**
3. **Reading Complete** → Flashcards → **Practice Complete**
4. **Practice Complete** → Quiz → **Assessment Complete**
5. **Assessment Complete** → Mastery Check → **Mastered** | **Needs Review**
6. **Mastered** → Next Subtopic | **Needs Review** → Additional Practice

### Critical Success Metrics
- **Reading Completion Rate**: % of articles read fully
- **Flashcard Success Rate**: Average correct answers
- **Quiz Performance**: First-attempt success rate
- **Mastery Progression**: Subtopics mastered per week
- **Retention Rate**: Spaced repetition performance
- **Engagement Consistency**: Daily session completion

### AI Integration Points
- **Content Generation**: Articles, flashcards, quizzes
- **Difficulty Adjustment**: Based on user performance
- **Path Optimization**: Next topic selection
- **Personalization**: Content style and examples
- **Mastery Assessment**: Intelligent scoring algorithms

---

## 🚀 Implementation Priority

### Phase 1: Core Flow (Weeks 1-4)
- Authentication & topic selection
- Daily feed generation
- Article reading tracking
- Basic progress recording

### Phase 2: Interactive Learning (Weeks 5-8)
- AI content generation
- Flashcard system
- Quiz engine
- Mastery calculation

### Phase 3: Intelligence Layer (Weeks 9-12)
- Spaced repetition
- Advanced analytics
- Path optimization
- Performance insights

This mental model ensures every frontend interaction has a clear purpose, proper API backing, and measurable learning outcomes.