import axios, { AxiosResponse } from 'axios';
import type {
  User,
  Topic,
  Subtopic,
  UserTopic,
  UserSubtopicProgress,
  LearningSession,
  DailyFeed,
  GeneratedContent,
  UserDashboard,
  TopicProgress,
  LoginForm,
  RegisterForm,
  ApiError,
} from '../types';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Helper function for handling API responses
const handleResponse = <T>(response: AxiosResponse<T>): T => response.data;

// Helper function for handling API errors
const handleError = (error: any): never => {
  const apiError: ApiError = {
    detail: error.response?.data?.detail || error.message || 'An unexpected error occurred',
    status_code: error.response?.status || 500,
  };
  throw apiError;
};

// Auth API
export const authApi = {
  async login(credentials: LoginForm): Promise<{ access_token: string; user: User }> {
    try {
      const formData = new FormData();
      formData.append('username', credentials.email);
      formData.append('password', credentials.password);

      const response = await apiClient.post('/auth/jwt/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async register(userData: RegisterForm): Promise<User> {
    try {
      const response = await apiClient.post('/auth/register', {
        email: userData.email,
        password: userData.password,
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getCurrentUser(): Promise<User> {
    try {
      const response = await apiClient.get('/users/me');
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/jwt/logout');
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    } catch (error) {
      // Even if logout fails, clear local storage
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
    }
  },
};

// Learning API
export const learningApi = {
  // Topics
  async getTopics(params?: {
    category?: string;
    is_active?: boolean;
    limit?: number;
    offset?: number;
  }): Promise<Topic[]> {
    try {
      const response = await apiClient.get('/learning/topics', { params });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getTopic(topicId: string): Promise<Topic> {
    try {
      const response = await apiClient.get(`/learning/topics/${topicId}`);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async createTopic(topicData: Partial<Topic>): Promise<Topic> {
    try {
      const response = await apiClient.post('/learning/topics', topicData);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  // Subtopics
  async getSubtopics(topicId: string, isActive?: boolean): Promise<Subtopic[]> {
    try {
      const response = await apiClient.get(`/learning/topics/${topicId}/subtopics`, {
        params: { is_active: isActive },
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getSubtopic(subtopicId: string): Promise<Subtopic> {
    try {
      const response = await apiClient.get(`/learning/subtopics/${subtopicId}`);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  // User Topics
  async subscribeToTopic(topicId: string): Promise<UserTopic> {
    try {
      const response = await apiClient.post('/learning/user/topics', {
        topic_id: topicId,
        is_active: true,
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getUserTopics(isActive?: boolean): Promise<UserTopic[]> {
    try {
      const response = await apiClient.get('/learning/user/topics', {
        params: { is_active: isActive },
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async updateUserTopic(topicId: string, data: Partial<UserTopic>): Promise<UserTopic> {
    try {
      const response = await apiClient.put(`/learning/user/topics/${topicId}`, data);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  // Progress
  async getUserProgress(subtopicId: string): Promise<UserSubtopicProgress> {
    try {
      const response = await apiClient.get(`/learning/user/progress/${subtopicId}`);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async updateUserProgress(
    subtopicId: string,
    progressData: Partial<UserSubtopicProgress>
  ): Promise<UserSubtopicProgress> {
    try {
      const response = await apiClient.put(`/learning/user/progress/${subtopicId}`, progressData);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getTopicProgress(topicId: string): Promise<UserSubtopicProgress[]> {
    try {
      const response = await apiClient.get(`/learning/user/progress/topic/${topicId}`);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getDueReviews(limit: number = 10): Promise<UserSubtopicProgress[]> {
    try {
      const response = await apiClient.get('/learning/user/reviews', {
        params: { limit },
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  // Learning Sessions
  async startLearningSession(progressId: string, sessionType: string): Promise<LearningSession> {
    try {
      const response = await apiClient.post('/learning/sessions', {
        progress_id: progressId,
        session_type: sessionType,
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async updateLearningSession(
    sessionId: string,
    sessionData: Partial<LearningSession>
  ): Promise<LearningSession> {
    try {
      const response = await apiClient.put(`/learning/sessions/${sessionId}`, sessionData);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getUserSessions(limit: number = 20): Promise<LearningSession[]> {
    try {
      const response = await apiClient.get('/learning/user/sessions', {
        params: { limit },
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  // Content Generation
  async generateContent(subtopicId: string): Promise<{ message: string; generated: string }> {
    try {
      const response = await apiClient.post(`/learning/subtopics/${subtopicId}/generate-content`);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getSubtopicContent(
    subtopicId: string,
    contentType?: string
  ): Promise<GeneratedContent[]> {
    try {
      const response = await apiClient.get(`/learning/subtopics/${subtopicId}/content`, {
        params: { content_type: contentType },
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getContent(contentId: string): Promise<GeneratedContent> {
    try {
      const response = await apiClient.get(`/learning/content/${contentId}`);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  // Daily Feed
  async generateDailyFeed(): Promise<{ message: string; feed_id: string }> {
    try {
      const response = await apiClient.post('/learning/feeds/generate');
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getTodayFeed(): Promise<DailyFeed | null> {
    try {
      const response = await apiClient.get('/learning/user/feed/today');
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async completeDailyFeed(feedId: string): Promise<{ message: string }> {
    try {
      const response = await apiClient.put(`/learning/feeds/${feedId}/complete`);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getFeedHistory(days: number = 30): Promise<DailyFeed[]> {
    try {
      const response = await apiClient.get('/learning/user/feed/history', {
        params: { days },
      });
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getUserStreak(): Promise<{ streak_days: number }> {
    try {
      const response = await apiClient.get('/learning/user/streak');
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  // Dashboard
  async getUserDashboard(): Promise<UserDashboard> {
    try {
      const response = await apiClient.get('/learning/user/dashboard');
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },

  async getTopicProgressSummary(topicId: string): Promise<TopicProgress> {
    try {
      const response = await apiClient.get(`/learning/user/topics/${topicId}/progress`);
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },
};

// Health check
export const healthApi = {
  async check(): Promise<any> {
    try {
      const response = await apiClient.get('/health');
      return handleResponse(response);
    } catch (error) {
      return handleError(error);
    }
  },
};

// Export the main client for custom requests
export { apiClient };
