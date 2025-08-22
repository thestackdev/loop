# 🧠 Adaptive Learning Backend - System Development Prompt

## 🎯 Project Vision
Build a neuroscience-based learning system that leverages brain hacks (active recall, spaced repetition, mnemonics) to maximize learning efficiency through a structured daily learning flow.

## 🔄 Core Learning Flow
1. **Daily Feed**: User opens app → sees today's learning card
2. **Article Reading**: Comprehensive but digestible content on selected subtopic
3. **Flashcard Session**: Active recall with mnemonics for key concepts
4. **Quiz Session**: Different questions to stress-test understanding
5. **Progress Tracking**: System intelligently selects next subtopic

## 🏗️ Backend Architecture Priorities

### Phase 1: Core Learning Engine (4-6 weeks)
```python
# Essential APIs to build:
✅ User Management & Authentication
✅ Topic/Subtopic Management System
✅ Daily Feed Generation API
✅ Article Content Storage & Serving
✅ Progress Tracking System
✅ Basic Flashcard Generation
✅ Quiz Generation & Scoring
✅ Smart Next-Topic Selection Algorithm
```

### Phase 2: AI Integration (2-3 weeks)
```python
# AI-Powered Features:
🤖 Dynamic Article Generation (OpenAI/Claude API)
🤖 Intelligent Flashcard Creation
🤖 Adaptive Quiz Generation
🤖 Mnemonic Generation for Complex Concepts
🤖 Content Difficulty Adjustment
```

### Phase 3: Learning Optimization (2-3 weeks)
```python
# Advanced Learning Features:
🧠 Spaced Repetition Algorithm (SM-2+)
🧠 Performance Analytics & Weak Area Detection
🧠 Learning Session Optimization
🧠 Retention Rate Tracking
```

## 📊 Database Schema Focus

### Core Tables
```sql
-- User learning state and preferences
users, user_topics, user_progress

-- Content hierarchy and management  
topics, subtopics, articles

-- Learning session tracking
learning_sessions, flashcard_attempts, quiz_attempts

-- Generated content versioning
flashcards, quizzes, mnemonics
```

## 🎯 Key Development Rules

### 1. **Sequential Learning Enforcement**
- Users must complete current subtopic before advancing
- No random topic jumping (implement later as feature)
- Smart prerequisite checking

### 2. **Content Generation Strategy**
- Generate flashcards/quizzes on-the-fly
- Save all versions for performance tracking
- Ensure quiz questions differ from flashcards

### 3. **Performance Tracking**
- Track reading completion, flashcard success rates
- Quiz scores and attempt counts
- Time spent on each learning component

### 4. **AI Integration Points**
```python
# Content Generation Services
article_generator(subtopic, user_level) → comprehensive article
flashcard_generator(article_content) → Q&A + mnemonics  
quiz_generator(subtopic, difficulty, exclusions) → challenging questions
mnemonic_generator(concept) → memory aids
```

## 🚀 Development Approach

### Start Simple, Scale Smart
1. **MVP**: Rule-based content selection, predefined articles
2. **AI Layer**: Integrate content generation gradually
3. **Optimization**: Add spaced repetition and analytics

### Technology Stack
- **Framework**: FastAPI (already set up)
- **Database**: PostgreSQL with SQLAlchemy
- **AI**: OpenAI/Claude API integration
- **Background Jobs**: Celery/Redis for daily feed generation
- **Caching**: Redis for performance optimization

## 🎓 Learning Science Implementation

### Active Recall Integration
- Flashcards force retrieval practice
- Quiz questions test application knowledge
- Progressive difficulty adjustment

### Spaced Repetition System
- Track performance on each concept
- Calculate optimal review intervals
- Automatically surface concepts for review

### Cognitive Load Management
- One subtopic per day maximum
- Balanced article length (10-15 min read)
- Chunked learning with clear phases

## 📈 Success Metrics to Track
- Daily learning completion rates
- Flashcard success percentages  
- Quiz performance trends
- Topic mastery progression
- User engagement consistency

## 🤖 AI Content Generation Strategy (Azure OpenAI)

### Complete AI-First Approach
- **No manual content**: Everything generated from day one using Azure OpenAI
- **Content Types**: Articles, flashcards, quizzes, mnemonics all AI-generated
- **Quality Control**: Senior backend engineer level depth and accuracy
- **Dynamic Generation**: Content created on-demand, not pre-stored

### Azure OpenAI Integration Points
```python
# Core AI Services Required:
article_generator(subtopic, engineer_level) → comprehensive technical article
flashcard_generator(article_content) → Q&A pairs + mnemonics
quiz_generator(subtopic, difficulty, exclude_questions) → challenging questions
mnemonic_generator(complex_concept) → memory aids
topic_breakdown_generator(topic_name) → subtopic hierarchy
```

## 📊 Backend Engineer Topic Importance Matrix

### HIGH IMPORTANCE (15-25 subtopics)
**Core Infrastructure & Architecture**
- SSH (18 subtopics): Advanced tunneling, security, automation
- Docker (20 subtopics): Multi-stage builds, networking, security
- Kubernetes (25 subtopics): Deep orchestration, troubleshooting
- System Design (30 subtopics): Scalability, consistency, performance
- Database Design (22 subtopics): Advanced patterns, optimization
- API Design (20 subtopics): REST, GraphQL, versioning
- Microservices (25 subtopics): Patterns, communication, data management

### MEDIUM-HIGH IMPORTANCE (12-15 subtopics)
**Backend Technologies**
- PostgreSQL, Redis, Message Queues, Load Balancing, Caching Strategies

### MEDIUM IMPORTANCE (8-12 subtopics)
**Development & Operations**
- Git Advanced, Linux Administration, Monitoring & Logging

### Topic Selection Strategy
- Users select 3-5 topics during onboarding
- System enforces sequential learning within each topic
- Topic switching allowed but discouraged until current topic completion

## 🎯 AI-Driven Mastery Detection Criteria

### Mastery Scoring Components
```
Flashcard Performance (30% weight):
- Success Rate Target: 85%+ correct answers
- Consistency Factor: Performance across multiple cards
- Time Efficiency: Appropriate response time

Quiz Performance (40% weight):
- First Attempt Score: 80%+ on initial try
- Multiple Attempt Penalty: -10% per additional attempt
- Improvement Recognition: Bonus for learning between attempts

Learning Efficiency (30% weight):
- Time Within Expected Range: 80%-120% of estimated time
- Engagement Quality: Active interaction vs passive reading
```

### Mastery Thresholds & Actions
```
90%+ Mastery: Advance to next subtopic + 7-day spaced repetition
80-89% Mastery: Advance + 3-day review reminder
70-79% Mastery: Additional quiz recommended
50-69% Mastery: Review flashcards, retry quiz
<50% Mastery: Re-read article, start learning cycle over
```

### Spaced Repetition Integration
- Higher mastery scores = longer review intervals
- Failed reviews reduce intervals dynamically
- Cross-topic concept reinforcement

## 🔧 Immediate Development Tasks

### Week 1-2: AI-Powered Foundation
1. Azure OpenAI service integration setup
2. Core database models with AI content versioning
3. User authentication with topic selection
4. AI article generation and serving system

### Week 3-4: Interactive Learning Flow
1. AI flashcard generation with mnemonic creation
2. Dynamic quiz generation with difficulty adjustment
3. Real-time mastery calculation engine
4. Progress tracking with spaced repetition scheduling

### Week 5-6: Intelligence & Optimization
1. Smart next-subtopic selection algorithm
2. Performance analytics and weak area detection
3. Cross-topic learning optimization
4. AI prompt optimization for content quality

## 🎯 Development Mindset
**Focus**: Build an AI-native learning engine that adapts to the user's brain patterns. Every algorithm should leverage AI to create personalized, neuroscience-backed learning experiences.

**Principle**: AI-first backend architecture. Design systems that get smarter with user interaction data, continuously improving content generation and learning path optimization.
