// Core API types matching backend schema
export interface User {
  id: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface Topic {
  id: string;
  name: string;
  description: string;
  category: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  estimated_hours: number;
  prerequisites: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Subtopic {
  id: string;
  topic_id: string;
  name: string;
  description: string;
  order_index: number;
  estimated_time_minutes: number;
  prerequisites: string[];
  difficulty_level: number;
  is_active: boolean;
  created_at: string;
}

export interface UserTopic {
  id: string;
  user_id: string;
  topic_id: string;
  is_active: boolean;
  created_at: string;
  topic?: Topic;
}

export interface UserSubtopicProgress {
  id: string;
  user_id: string;
  subtopic_id: string;
  mastery_level: 'not_started' | 'learning' | 'practiced' | 'mastered' | 'expert';
  confidence_score: number;
  total_attempts: number;
  correct_attempts: number;
  last_attempt_at: string | null;
  completed_at: string | null;
  next_review_date: string | null;
  spaced_repetition_interval: number;
  created_at: string;
  updated_at: string;
  subtopic?: Subtopic;
}

export interface LearningSession {
  id: string;
  user_id: string;
  progress_id: string;
  session_type: 'reading' | 'flashcards' | 'quiz' | 'review';
  started_at: string;
  completed_at: string | null;
  time_spent_seconds: number;
  performance_score: number | null;
  created_at: string;
}

export interface DailyFeed {
  id: string;
  user_id: string;
  subtopic_id: string;
  feed_date: string;
  is_completed: boolean;
  completed_at: string | null;
  created_at: string;
  subtopic?: Subtopic;
}

export interface GeneratedContent {
  id: string;
  subtopic_id: string;
  content_type: 'article' | 'flashcard' | 'quiz' | 'summary';
  title: string;
  content: any; // JSON content structure varies by type
  metadata: any; // Additional metadata
  created_at: string;
}

export interface UserDashboard {
  active_topics: UserTopic[];
  today_feed: DailyFeed | null;
  streak_days: number;
  total_mastered_subtopics: number;
  total_time_spent_hours: number;
  recent_sessions: LearningSession[];
}

export interface TopicProgress {
  topic: Topic;
  total_subtopics: number;
  completed_subtopics: number;
  mastered_subtopics: number;
  current_subtopic: Subtopic | null;
  progress_percentage: number;
  estimated_completion_days: number | null;
}

// Learning content specific types
export interface Article {
  title: string;
  content: string;
  key_concepts: string[];
  examples: any[];
  reading_time_minutes: number;
}

export interface Flashcard {
  id: string;
  question: string;
  answer: string;
  hint?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  tags: string[];
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

export interface Quiz {
  questions: QuizQuestion[];
  passing_score: number;
  time_limit_minutes?: number;
}

// Form types
export interface LoginForm {
  email: string;
  password: string;
}

export interface RegisterForm {
  email: string;
  password: string;
  confirmPassword: string;
}

export interface TopicSelectionForm {
  selectedTopics: string[];
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

// Learning flow state types
export interface LearningState {
  currentPhase: 'reading' | 'flashcards' | 'quiz' | 'completed';
  currentSubtopic: Subtopic | null;
  currentContent: GeneratedContent | null;
  sessionStartTime: Date | null;
  progress: {
    reading: boolean;
    flashcards: boolean;
    quiz: boolean;
  };
}

// UI state types
export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  message?: string;
  code?: string;
}
