import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthContext } from '../auth/AuthProvider';
import { Button } from '../ui/Button';
import {
  Brain,
  User,
  LogOut,
  Settings,
  BarChart3
} from 'lucide-react';

export const Header: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuthContext();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated) {
    return (
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900">Loop Learning</span>
          </Link>

          <div className="flex items-center space-x-4">
            <Link to="/login">
              <Button variant="ghost" size="sm">Sign In</Button>
            </Link>
            <Link to="/register">
              <Button variant="primary" size="sm">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>
    );
  }

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center space-x-2">
          <Brain className="h-8 w-8 text-primary-600" />
          <span className="text-xl font-bold text-gray-900">Loop Learning</span>
        </Link>

        <nav className="hidden md:flex items-center space-x-6">
          <Link
            to="/dashboard"
            className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
          >
            Dashboard
          </Link>
          <Link
            to="/topics"
            className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
          >
            Topics
          </Link>
          <Link
            to="/progress"
            className="text-gray-600 hover:text-gray-900 font-medium transition-colors flex items-center space-x-1"
          >
            <BarChart3 className="h-4 w-4" />
            <span>Progress</span>
          </Link>
        </nav>

        <div className="flex items-center space-x-4">
          <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
            <User className="h-4 w-4" />
            <span>{user?.email}</span>
          </div>

          <div className="flex items-center space-x-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/settings')}
            >
              <Settings className="h-4 w-4" />
            </Button>

            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
            >
              <LogOut className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};
