# 🧠 Adaptive Daily Tech Learning System

An AI-powered personalized learning platform that creates unique learning journeys for each user, ensuring they learn exactly what they need, when they need it, in the most effective way possible.

## 📋 Overview

The Adaptive Daily Tech Learning System leverages neuroscience-based techniques and AI to provide:
- **Knowledge Discovery**: Identifies what users don't know through intelligent gap analysis
- **AI-Generated Content**: Creates personalized explanations, articles, flashcards, and quizzes
- **Cognitive Enhancement**: Uses spaced repetition, active recall, and memory techniques
- **Progress Tracking**: Monitors learning effectiveness and adjusts difficulty dynamically

## 🏗️ Architecture

### Backend (FastAPI)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for session management and performance
- **AI Integration**: Azure OpenAI for dynamic content generation
- **Authentication**: JWT-based user authentication with FastAPI-Users
- **API Documentation**: Automatic OpenAPI/Swagger documentation

### Core Components
- **Learning Engine**: Manages topics, subtopics, and user progress
- **Content Generation**: AI-powered article, flashcard, and quiz creation
- **Feed System**: Daily personalized learning content delivery
- **Progress Tracking**: Spaced repetition and mastery level monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Azure OpenAI API access

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd learning-enhancer
```

2. **Set up the backend**
```bash
cd backend

# Install dependencies using Poetry
poetry install

# Or using pip
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configurations:
OSMOSIS_DB_HOST=localhost
OSMOSIS_DB_PORT=5432
OSMOSIS_DB_USER=your_db_user
OSMOSIS_DB_PASS=your_db_password
OSMOSIS_DB_BASE=learning_db

AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_MODEL_NAME=gpt-4

USERS_SECRET=your_jwt_secret_key
```

4. **Set up the database**
```bash
# Run database migrations
poetry run alembic upgrade head

# Seed initial topics (optional)
poetry run python loop/scripts/seed_topics.py
```

5. **Start the development server**
```bash
# Using Poetry
poetry run uvicorn loop.web.application:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m uvicorn loop.web.application:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with automatic documentation at `http://localhost:8000/docs`.

## 🐳 Docker Development

### Using Docker Compose

1. **Build and start all services**
```bash
cd backend
docker-compose up --build
```

This will start:
- **API**: FastAPI application on port 8000
- **Database**: PostgreSQL on port 5432  
- **Redis**: Redis on port 6379
- **Migrator**: Automatic database migrations

2. **Access the application**
- API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Database: `localhost:5432` (user: `loop`, password: `loop`, db: `loop`)

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/jwt/login` - Login and get JWT token
- `POST /auth/jwt/logout` - Logout
- `GET /auth/users/me` - Get current user profile

### Topics & Learning
- `GET /api/topics` - Get all available topics
- `POST /api/user/topics` - Subscribe to a topic
- `GET /api/user/topics` - Get user's subscribed topics
- `GET /api/topics/{topic_id}/subtopics` - Get subtopics for a topic

### Daily Learning Flow
- `POST /api/feeds/generate` - Generate today's learning feed
- `GET /api/user/feed/today` - Get today's learning content
- `PUT /api/feeds/{feed_id}/complete` - Mark feed as completed

### Content & Progress
- `POST /api/subtopics/{subtopic_id}/generate-content` - Generate AI content for subtopic
- `GET /api/subtopics/{subtopic_id}/content` - Get generated content
- `GET /api/user/progress/{subtopic_id}` - Get progress for subtopic
- `PUT /api/user/progress/{subtopic_id}` - Update progress

### Dashboard & Analytics
- `GET /api/user/dashboard` - Get user dashboard data
- `GET /api/user/streak` - Get current learning streak
- `GET /api/user/topics/{topic_id}/progress` - Get topic progress summary

## 🧪 Testing

### API Testing

The project includes a comprehensive API testing suite:

```bash
# Run all API tests
python backend/api_test_collection.py --base-url http://localhost:8000 --run-tests

# Save test results for analysis
python backend/api_test_collection.py --base-url http://localhost:8000 --run-tests --save-results

# Cleanup test resources
python backend/api_test_collection.py --base-url http://localhost:8000 --cleanup-only
```

### Unit Testing

```bash
# Run unit tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=loop --cov-report=html
```

### Code Quality

```bash
# Linting
poetry run ruff check .

# Type checking
poetry run mypy .

# Code formatting
poetry run black .
```

## 📊 Database Schema

### Core Tables

- **`users`** - User accounts and authentication
- **`topics`** - Learning topics (e.g., "System Design", "Docker Mastery")
- **`subtopics`** - Individual learning units within topics
- **`user_topics`** - User topic subscriptions
- **`user_subtopic_progress`** - Learning progress and mastery tracking
- **`daily_feeds`** - Daily learning assignments
- **`learning_sessions`** - Individual learning session records
- **`generated_content`** - AI-generated articles, flashcards, quizzes

### Key Relationships

- Users subscribe to Topics
- Topics contain multiple Subtopics (ordered sequence)
- Progress is tracked per User-Subtopic combination
- Daily Feeds assign specific Subtopics to Users
- Generated Content is created per Subtopic

## 🤖 AI Content Generation

### Azure OpenAI Integration

The system uses Azure OpenAI to generate:
- **Technical Articles**: Comprehensive explanations for each subtopic
- **Flashcards**: Q&A pairs with mnemonics for key concepts  
- **Quizzes**: Challenging questions to test understanding
- **Memory Aids**: Mnemonics and memory palace techniques

### Content Types

1. **Articles**: 10-15 minute technical deep-dives
2. **Flashcards**: Active recall with memory techniques
3. **Quizzes**: Application-focused questions
4. **Mnemonics**: Memory aids for complex concepts

## 🧠 Learning Science Features

### Spaced Repetition
- **Algorithm**: Enhanced SM-2 with cognitive load adjustment
- **Intervals**: Dynamic based on performance and mastery level
- **Review Scheduling**: Automatic scheduling of content for optimal retention

### Mastery Tracking
- **Levels**: `learning` → `familiar` → `proficient` → `mastered` → `expert`
- **Scoring**: Multi-dimensional based on speed, accuracy, and consistency
- **Adaptation**: Content difficulty adjusts based on mastery level

### Cognitive Optimization
- **Session Length**: Optimized for attention span (15-30 minutes)
- **Cognitive Load**: Balanced information presentation
- **Active Recall**: Testing-based learning methodology

## 🎯 Learning Flow

### Daily Learning Cycle

1. **Morning**: User opens app and receives today's learning feed
2. **Article**: Read comprehensive content on selected subtopic (15-20 min)
3. **Flashcards**: Active recall session with mnemonics (5-10 min) 
4. **Quiz**: Application questions to test understanding (5-10 min)
5. **Progress**: System updates mastery level and schedules next content

### Topic Progression

- **Sequential Learning**: Users complete subtopics in order
- **Prerequisite Enforcement**: Advanced topics unlock after foundations
- **Mastery Gates**: Must achieve proficiency before advancing
- **Spaced Review**: Previously learned content resurfaces for retention

## 🎮 Gamification Features

### Progress Tracking
- **Learning Streaks**: Daily learning completion tracking
- **Mastery Badges**: Achievement system for completed topics
- **Progress Visualization**: Topic completion percentages
- **Time Tracking**: Total learning time and session analytics

### Engagement Mechanics
- **Daily Goals**: Personalized learning targets
- **Achievement System**: Badges for milestones and consistency
- **Progress Sharing**: Social features for motivation
- **Streak Maintenance**: Streak freeze and recovery mechanisms

## 📈 Monitoring & Analytics

### User Analytics
- **Learning Velocity**: Topics mastered per week
- **Retention Rates**: Spaced repetition success rates
- **Engagement Metrics**: Session duration and frequency
- **Content Effectiveness**: Performance by content type

### System Metrics
- **API Performance**: Response times and error rates
- **Content Quality**: User ratings and feedback
- **AI Generation**: Content creation success rates
- **Database Performance**: Query optimization and indexing

## 🔧 Development

### Project Structure

```
learning-enhancer/
├── backend/                 # FastAPI backend application
│   ├── loop/               # Main application package
│   │   ├── db/             # Database models and DAOs
│   │   ├── web/            # API routes and schemas
│   │   ├── services/       # Business logic and AI services
│   │   └── scripts/        # Management scripts
│   ├── tests/              # Test suite
│   ├── docker-compose.yml  # Development environment
│   └── pyproject.toml      # Python dependencies
├── CLAUDE.md               # Development instructions
└── README.md               # This file
```

### Code Style

- **Linting**: Ruff for code quality
- **Type Checking**: MyPy for static analysis  
- **Formatting**: Black for consistent code style
- **Documentation**: Comprehensive docstrings and API docs

### Contributing

1. **Setup**: Follow the installation guide
2. **Development**: Use Poetry for dependency management
3. **Testing**: Ensure all tests pass before submitting
4. **Code Quality**: Run linting and type checking
5. **Documentation**: Update docs for new features

## 🚀 Production Deployment

### Environment Setup

1. **Database**: PostgreSQL with appropriate sizing for user base
2. **Cache**: Redis cluster for high availability
3. **API**: Gunicorn with multiple workers
4. **Monitoring**: Prometheus + Grafana for observability
5. **Logging**: Structured logging with centralized collection

### Scaling Considerations

- **Database**: Read replicas for analytical queries
- **API**: Horizontal scaling with load balancing
- **Background Jobs**: Celery with Redis for async processing
- **CDN**: Static content delivery for better performance

## 📋 Roadmap

### Phase 1: Core Learning Engine ✅
- [x] User authentication and profiles
- [x] Topic/subtopic management
- [x] Daily feed generation
- [x] Basic progress tracking
- [x] AI content generation

### Phase 2: Enhanced Intelligence 🔄
- [ ] Advanced spaced repetition algorithms
- [ ] Cross-topic knowledge mapping
- [ ] Adaptive difficulty adjustment  
- [ ] Learning style personalization
- [ ] Performance analytics dashboard

### Phase 3: Social & Gamification 📅
- [ ] Social learning features
- [ ] Advanced achievement system
- [ ] Peer challenges and competitions
- [ ] Community-driven content
- [ ] Mobile application

### Phase 4: Enterprise & Scale 🔮
- [ ] Multi-tenant architecture
- [ ] Enterprise learning programs
- [ ] Advanced analytics and insights
- [ ] Integration APIs for LMS systems
- [ ] White-label solutions

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL 16+ with SQLAlchemy
- **Cache**: Redis 6+ with hiredis
- **Authentication**: JWT with FastAPI-Users
- **AI**: Azure OpenAI API integration
- **Task Queue**: (Future) Celery with Redis backend
- **Monitoring**: Prometheus + Grafana integration

### Development Tools
- **Package Management**: Poetry
- **Code Quality**: Ruff, Black, MyPy
- **Testing**: pytest with coverage
- **Database Migrations**: Alembic
- **API Documentation**: Automatic OpenAPI/Swagger
- **Containerization**: Docker with multi-stage builds

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support, questions, or contributions:
- **Issues**: Create a GitHub issue for bugs or feature requests
- **Documentation**: Check the `/docs` endpoint when running the API
- **Development**: See `CLAUDE.md` for detailed development instructions

---

**Built with ❤️ for developers who never stop learning**