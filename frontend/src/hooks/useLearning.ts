import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { learningApi } from '../lib/api';
import { QUERY_KEYS } from '../lib/react-query';
import toast from 'react-hot-toast';

// Dashboard hook
export const useDashboard = () => {
  return useQuery({
    queryKey: QUERY_KEYS.dashboard,
    queryFn: learningApi.getUserDashboard,
  });
};

// Topics hooks
export const useTopics = (params?: {
  category?: string;
  is_active?: boolean;
  limit?: number;
  offset?: number;
}) => {
  return useQuery({
    queryKey: QUERY_KEYS.topics(params),
    queryFn: () => learningApi.getTopics(params),
  });
};

export const useTopic = (topicId: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.topic(topicId),
    queryFn: () => learningApi.getTopic(topicId),
    enabled: !!topicId,
  });
};

export const useUserTopics = (isActive?: boolean) => {
  return useQuery({
    queryKey: QUERY_KEYS.userTopics(isActive),
    queryFn: () => learningApi.getUserTopics(isActive),
  });
};

// Subtopics hooks
export const useSubtopics = (topicId: string, isActive?: boolean) => {
  return useQuery({
    queryKey: QUERY_KEYS.subtopics(topicId, isActive),
    queryFn: () => learningApi.getSubtopics(topicId, isActive),
    enabled: !!topicId,
  });
};

export const useSubtopic = (subtopicId: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.subtopic(subtopicId),
    queryFn: () => learningApi.getSubtopic(subtopicId),
    enabled: !!subtopicId,
  });
};

// Progress hooks
export const useUserProgress = (subtopicId: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.userProgress(subtopicId),
    queryFn: () => learningApi.getUserProgress(subtopicId),
    enabled: !!subtopicId,
  });
};

export const useTopicProgress = (topicId: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.topicProgress(topicId),
    queryFn: () => learningApi.getTopicProgress(topicId),
    enabled: !!topicId,
  });
};

export const useTopicProgressSummary = (topicId: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.topicProgressSummary(topicId),
    queryFn: () => learningApi.getTopicProgressSummary(topicId),
    enabled: !!topicId,
  });
};

export const useDueReviews = (limit?: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.dueReviews(limit),
    queryFn: () => learningApi.getDueReviews(limit),
  });
};

// Content hooks
export const useSubtopicContent = (subtopicId: string, contentType?: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.subtopicContent(subtopicId, contentType),
    queryFn: () => learningApi.getSubtopicContent(subtopicId, contentType),
    enabled: !!subtopicId,
  });
};

export const useContent = (contentId: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.content(contentId),
    queryFn: () => learningApi.getContent(contentId),
    enabled: !!contentId,
  });
};

// Feed hooks
export const useTodayFeed = () => {
  return useQuery({
    queryKey: QUERY_KEYS.todayFeed,
    queryFn: learningApi.getTodayFeed,
  });
};

export const useFeedHistory = (days?: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.feedHistory(days),
    queryFn: () => learningApi.getFeedHistory(days),
  });
};

export const useUserStreak = () => {
  return useQuery({
    queryKey: QUERY_KEYS.userStreak,
    queryFn: learningApi.getUserStreak,
  });
};

// Sessions hook
export const useUserSessions = (limit?: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.userSessions(limit),
    queryFn: () => learningApi.getUserSessions(limit),
  });
};

// Mutation hooks
export const useSubscribeToTopic = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: learningApi.subscribeToTopic,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userTopics'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast.success('Successfully subscribed to topic!');
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Failed to subscribe to topic');
    },
  });
};

export const useUpdateUserProgress = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ subtopicId, progressData }: {
      subtopicId: string;
      progressData: any;
    }) => learningApi.updateUserProgress(subtopicId, progressData),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['userProgress', variables.subtopicId] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['dueReviews'] });
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Failed to update progress');
    },
  });
};

export const useGenerateContent = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: learningApi.generateContent,
    onSuccess: (_, subtopicId) => {
      queryClient.invalidateQueries({ queryKey: ['subtopicContent', subtopicId] });
      toast.success('Content generated successfully!');
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Failed to generate content');
    },
  });
};

export const useStartLearningSession = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ progressId, sessionType }: {
      progressId: string;
      sessionType: string;
    }) => learningApi.startLearningSession(progressId, sessionType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userSessions'] });
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Failed to start learning session');
    },
  });
};

export const useUpdateLearningSession = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ sessionId, sessionData }: {
      sessionId: string;
      sessionData: any;
    }) => learningApi.updateLearningSession(sessionId, sessionData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userSessions'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Failed to update session');
    },
  });
};

export const useGenerateDailyFeed = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: learningApi.generateDailyFeed,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todayFeed'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      toast.success('Daily feed generated!');
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Failed to generate daily feed');
    },
  });
};

export const useCompleteDailyFeed = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: learningApi.completeDailyFeed,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todayFeed'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['userStreak'] });
      toast.success('Daily learning completed! 🎉');
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Failed to complete daily feed');
    },
  });
};
