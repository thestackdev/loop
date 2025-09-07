import React from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  Target,
  Clock,
  TrendingUp,
  Zap,
  Calendar,
  Trophy,
  ArrowRight
} from 'lucide-react';

import { useDashboard, useTodayFeed, useUserStreak } from '../hooks/useLearning';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';

const StatCard: React.FC<{
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: string;
  color?: 'blue' | 'green' | 'purple' | 'orange';
}> = ({ title, value, icon, trend, color = 'blue' }) => {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    orange: 'bg-orange-50 text-orange-600',
  };

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
          {trend && (
            <p className="text-sm text-green-600 mt-1 flex items-center">
              <TrendingUp className="h-4 w-4 mr-1" />
              {trend}
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
    </Card>
  );
};

export const Dashboard: React.FC = () => {
  const { data: dashboard, isLoading: isDashboardLoading } = useDashboard();
  const { data: todayFeed } = useTodayFeed();
  const { data: streak } = useUserStreak();

  if (isDashboardLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  const hasLearningToday = todayFeed && !todayFeed.is_completed;
  const completedToday = todayFeed?.is_completed;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Good morning! 👋</h1>
          <p className="text-gray-600 mt-1">Ready to continue your learning journey?</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <p className="text-sm text-gray-600">Today</p>
            <p className="text-lg font-semibold text-gray-900">
              {new Date().toLocaleDateString('en-US', {
                weekday: 'long',
                month: 'short',
                day: 'numeric'
              })}
            </p>
          </div>
        </div>
      </div>

      {/* Today's Learning Card */}
      {hasLearningToday && (
        <Card className="bg-gradient-to-r from-primary-500 to-primary-600 text-white p-8">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2">Today's Learning</h2>
              <p className="text-primary-100 mb-4">
                Continue your journey with {todayFeed.subtopic?.name}
              </p>
              <Link to="/learn">
                <Button variant="secondary" className="bg-white text-primary-600 hover:bg-gray-50">
                  Start Learning
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
            <div className="hidden md:block">
              <Zap className="h-16 w-16 text-primary-200" />
            </div>
          </div>
        </Card>
      )}

      {/* Completed Today Message */}
      {completedToday && (
        <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white p-8">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2">Great job today! 🎉</h2>
              <p className="text-green-100 mb-4">
                You've completed today's learning session. Come back tomorrow for more!
              </p>
              <Link to="/progress">
                <Button variant="secondary" className="bg-white text-green-600 hover:bg-gray-50">
                  View Progress
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
            <div className="hidden md:block">
              <Trophy className="h-16 w-16 text-green-200" />
            </div>
          </div>
        </Card>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Learning Streak"
          value={`${streak?.streak_days || 0} days`}
          icon={<Trophy className="h-6 w-6" />}
          color="orange"
        />

        <StatCard
          title="Active Topics"
          value={dashboard?.active_topics?.length || 0}
          icon={<BookOpen className="h-6 w-6" />}
          color="blue"
        />

        <StatCard
          title="Mastered Subtopics"
          value={dashboard?.total_mastered_subtopics || 0}
          icon={<Target className="h-6 w-6" />}
          trend="+2 this week"
          color="green"
        />

        <StatCard
          title="Time Spent"
          value={`${Math.round(dashboard?.total_time_spent_hours || 0)}h`}
          icon={<Clock className="h-6 w-6" />}
          color="purple"
        />
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Active Topics */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Active Topics</h3>
            <Link to="/topics" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
              View all
            </Link>
          </div>

          <div className="space-y-4">
            {dashboard?.active_topics?.slice(0, 3).map((userTopic) => (
              <div key={userTopic.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium text-gray-900">{userTopic.topic?.name}</h4>
                  <p className="text-sm text-gray-600">{userTopic.topic?.category}</p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-gray-500">
                    {userTopic.topic?.difficulty_level}
                  </span>
                </div>
              </div>
            )) || (
              <div className="text-center py-8">
                <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No active topics yet</p>
                <Link to="/topics">
                  <Button variant="primary" className="mt-4">
                    Browse Topics
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </Card>

        {/* Recent Sessions */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Recent Sessions</h3>
            <Link to="/progress" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
              View all
            </Link>
          </div>

          <div className="space-y-4">
            {dashboard?.recent_sessions?.slice(0, 3).map((session) => (
              <div key={session.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium text-gray-900 capitalize">
                    {session.session_type} Session
                  </h4>
                  <p className="text-sm text-gray-600">
                    {Math.round(session.time_spent_seconds / 60)} minutes
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-gray-500">
                    {new Date(session.started_at).toLocaleDateString()}
                  </p>
                  {session.performance_score && (
                    <p className="text-sm font-medium text-green-600">
                      {Math.round(session.performance_score)}% score
                    </p>
                  )}
                </div>
              </div>
            )) || (
              <div className="text-center py-8">
                <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">No recent sessions</p>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};
