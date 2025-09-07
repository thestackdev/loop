import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { healthApi, learningApi } from '../lib/api';
import { Card } from '../components/ui/Card';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react';

const TestItem: React.FC<{
  title: string;
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  data?: any;
  error?: any;
}> = ({ title, isLoading, isSuccess, isError, data, error }) => {
  return (
    <div className="flex items-center justify-between p-4 border-b border-gray-100 last:border-b-0">
      <div className="flex-1">
        <h4 className="font-medium text-gray-900">{title}</h4>
        {isLoading && <p className="text-sm text-gray-500">Testing...</p>}
        {isSuccess && <p className="text-sm text-green-600">✓ Connected</p>}
        {isError && <p className="text-sm text-red-600">✗ Failed: {error?.detail || 'Unknown error'}</p>}
      </div>
      <div>
        {isLoading && <LoadingSpinner size="small" />}
        {isSuccess && <CheckCircle className="h-5 w-5 text-green-500" />}
        {isError && <XCircle className="h-5 w-5 text-red-500" />}
      </div>
    </div>
  );
};

export const TestConnection: React.FC = () => {
  // Test health endpoint
  const healthQuery = useQuery({
    queryKey: ['test', 'health'],
    queryFn: healthApi.check,
    retry: false,
  });

  // Test topics endpoint (public)
  const topicsQuery = useQuery({
    queryKey: ['test', 'topics'],
    queryFn: () => learningApi.getTopics({ limit: 5 }),
    retry: false,
  });

  const allTests = [
    {
      title: 'Backend Health Check',
      ...healthQuery,
    },
    {
      title: 'Topics API (Public)',
      ...topicsQuery,
    },
  ];

  const successCount = allTests.filter(test => test.isSuccess).length;
  const totalTests = allTests.length;
  const allPassed = successCount === totalTests;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">System Status</h1>
        <p className="text-gray-600">Testing frontend-backend connectivity</p>
      </div>

      <Card className="mb-6">
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Connection Tests</h3>
              <p className="text-sm text-gray-600">
                {successCount} of {totalTests} tests passed
              </p>
            </div>
            <div className="flex items-center space-x-2">
              {allPassed ? (
                <CheckCircle className="h-6 w-6 text-green-500" />
              ) : (
                <AlertCircle className="h-6 w-6 text-yellow-500" />
              )}
            </div>
          </div>
        </div>

        <div>
          {allTests.map((test, index) => (
            <TestItem
              key={index}
              title={test.title}
              isLoading={test.isLoading}
              isSuccess={test.isSuccess}
              isError={test.isError}
              data={test.data}
              error={test.error}
            />
          ))}
        </div>
      </Card>

      {/* Server Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Frontend Server</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">URL:</span>
              <span className="font-mono">localhost:5173</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Framework:</span>
              <span>React + Vite</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Status:</span>
              <span className="text-green-600">Running</span>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Backend Server</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">URL:</span>
              <span className="font-mono">localhost:8000</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Framework:</span>
              <span>FastAPI + Python</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Status:</span>
              <span className={healthQuery.isSuccess ? 'text-green-600' : 'text-red-600'}>
                {healthQuery.isSuccess ? 'Running' : 'Error'}
              </span>
            </div>
          </div>
        </Card>
      </div>

      {/* Sample Data */}
      {topicsQuery.isSuccess && topicsQuery.data && (
        <Card className="mt-6 p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Sample Topics Data</h3>
          <div className="space-y-2">
            {topicsQuery.data.slice(0, 3).map((topic: any) => (
              <div key={topic.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium text-gray-900">{topic.name}</h4>
                  <p className="text-sm text-gray-600">{topic.category}</p>
                </div>
                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                  {topic.difficulty_level}
                </span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};
