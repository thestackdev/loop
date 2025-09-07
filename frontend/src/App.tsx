import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { Toaster } from "react-hot-toast";

import { queryClient } from "./lib/react-query";
import { AuthProvider } from "./components/auth/AuthProvider";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { Layout } from "./components/layout/Layout";

// Pages
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { Dashboard } from "./pages/Dashboard";
import { TestConnection } from "./pages/TestConnection";
import { TopicsPage } from "./pages/Topics";
import { LearningPage } from "./pages/Learning";
import { ProgressPage } from "./pages/Progress";
import { ReviewsPage } from "./pages/Reviews";
import { SettingsPage } from "./pages/Settings";

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <div className="App">
            <Routes>
              {/* Public routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* Protected routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <Dashboard />
                    </Layout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/topics"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <TopicsPage />
                    </Layout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/learn"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <LearningPage />
                    </Layout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/progress"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <ProgressPage />
                    </Layout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/reviews"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <ReviewsPage />
                    </Layout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/test"
                element={
                  <Layout showSidebar={false}>
                    <TestConnection />
                  </Layout>
                }
              />

              <Route
                path="/settings"
                element={
                  <ProtectedRoute>
                    <Layout>
                      <SettingsPage />
                    </Layout>
                  </ProtectedRoute>
                }
              />

              {/* Default redirect */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />

              {/* Catch all - redirect to dashboard */}
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </div>

          {/* Global toast notifications */}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              className: "bg-white shadow-lg border border-gray-200",
            }}
          />
        </AuthProvider>
      </Router>

      {/* React Query Devtools (only in development) */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default App;
