import React from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { useAuthContext } from '../auth/AuthProvider';

interface LayoutProps {
  children: React.ReactNode;
  showSidebar?: boolean;
}

export const Layout: React.FC<LayoutProps> = ({ children, showSidebar = true }) => {
  const { isAuthenticated } = useAuthContext();

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="flex">
        {isAuthenticated && showSidebar && <Sidebar />}

        <main className={`flex-1 ${isAuthenticated && showSidebar ? 'ml-0' : ''}`}>
          <div className="max-w-7xl mx-auto px-6 py-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
