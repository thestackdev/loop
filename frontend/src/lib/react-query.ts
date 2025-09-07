import { QueryClient } from '@tanstack/react-query';

// Create a client
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      retry: (failureCount, error: any) => {
        // Don't retry on 401/403 errors
        if (error?.status_code === 401 || error?.status_code === 403) {
          return false;
        }
        // Retry up to 2 times for other errors
        return failureCount < 2;
      },
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: false,
    },
  },
});

// Query Keys - centralized for consistency
export const QUERY_KEYS = {
  // Auth
  currentUser: ['auth', 'currentUser'] as const,

  // Topics
  topics: (params?: any) => ['topics', params] as const,
  topic: (id: string) => ['topics', id] as const,
  userTopics: (isActive?: boolean) => ['userTopics', isActive] as const,

  // Subtopics
  subtopics: (topicId: string, isActive?: boolean) =>
    ['subtopics', topicId, isActive] as const,
  subtopic: (id: string) => ['subtopics', id] as const,

  // Progress
  userProgress: (subtopicId: string) => ['userProgress', subtopicId] as const,
  topicProgress: (topicId: string) => ['topicProgress', topicId] as const,
  topicProgressSummary: (topicId: string) => ['topicProgressSummary', topicId] as const,
  dueReviews: (limit?: number) => ['dueReviews', limit] as const,

  // Content
  subtopicContent: (subtopicId: string, contentType?: string) =>
    ['subtopicContent', subtopicId, contentType] as const,
  content: (id: string) => ['content', id] as const,

  // Sessions
  userSessions: (limit?: number) => ['userSessions', limit] as const,

  // Feed
  todayFeed: ['todayFeed'] as const,
  feedHistory: (days?: number) => ['feedHistory', days] as const,
  userStreak: ['userStreak'] as const,

  // Dashboard
  dashboard: ['dashboard'] as const,
} as const;
