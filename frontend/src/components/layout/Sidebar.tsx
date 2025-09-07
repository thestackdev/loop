import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Home,
  BookOpen,
  BarChart3,
  Target,
  Clock,
  Trophy,
  Settings,
  Zap
} from 'lucide-react';
import { useUserStreak, useDueReviews } from '../../hooks/useLearning';

interface SidebarItemProps {
  to: string;
  icon: React.ReactNode;
  label: string;
  badge?: number;
  isActive?: boolean;
}

const SidebarItem: React.FC<SidebarItemProps> = ({
  to,
  icon,
  label,
  badge,
  isActive = false
}) => {
  return (
    <Link
      to={to}
      className={`
        flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-colors
        ${isActive
          ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-700'
          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
        }
      `}
    >
      <div className="flex items-center space-x-3">
        {icon}
        <span>{label}</span>
      </div>
      {badge !== undefined && badge > 0 && (
        <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-0.5 rounded-full">
          {badge}
        </span>
      )}
    </Link>
  );
};

export const Sidebar: React.FC = () => {
  const location = useLocation();
  const { data: streak } = useUserStreak();
  const { data: dueReviews } = useDueReviews();

  const isActive = (path: string) => location.pathname === path;

  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
      <div className="p-6">
        <div className="space-y-2">
          <SidebarItem
            to="/dashboard"
            icon={<Home className="h-5 w-5" />}
            label="Dashboard"
            isActive={isActive('/dashboard')}
          />

          <SidebarItem
            to="/learn"
            icon={<Zap className="h-5 w-5" />}
            label="Today's Learning"
            isActive={isActive('/learn')}
          />

          <SidebarItem
            to="/topics"
            icon={<BookOpen className="h-5 w-5" />}
            label="Topics"
            isActive={isActive('/topics')}
          />

          <SidebarItem
            to="/progress"
            icon={<BarChart3 className="h-5 w-5" />}
            label="Progress"
            isActive={isActive('/progress')}
          />

          <SidebarItem
            to="/reviews"
            icon={<Clock className="h-5 w-5" />}
            label="Reviews"
            badge={dueReviews?.length}
            isActive={isActive('/reviews')}
          />

          <SidebarItem
            to="/goals"
            icon={<Target className="h-5 w-5" />}
            label="Goals"
            isActive={isActive('/goals')}
          />
        </div>

        <hr className="my-6 border-gray-200" />

        <div className="space-y-2">
          <SidebarItem
            to="/achievements"
            icon={<Trophy className="h-5 w-5" />}
            label="Achievements"
            isActive={isActive('/achievements')}
          />

          <SidebarItem
            to="/settings"
            icon={<Settings className="h-5 w-5" />}
            label="Settings"
            isActive={isActive('/settings')}
          />
        </div>

        {streak && (
          <div className="mt-8 p-4 bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <div className="bg-orange-100 p-2 rounded-lg">
                <Trophy className="h-5 w-5 text-orange-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Learning Streak</p>
                <p className="text-lg font-bold text-primary-600">
                  {streak.streak_days} days
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};
