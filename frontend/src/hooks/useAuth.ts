import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { authApi } from '../lib/api';
import { QUERY_KEYS } from '../lib/react-query';
import type { User, LoginForm, RegisterForm } from '../types';
import toast from 'react-hot-toast';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}

export const useAuth = () => {
  const queryClient = useQueryClient();

  // Get current user query
  const {
    data: user,
    isLoading,
    error,
  } = useQuery({
    queryKey: QUERY_KEYS.currentUser,
    queryFn: authApi.getCurrentUser,
    enabled: !!localStorage.getItem('authToken'),
    retry: false,
  });

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      localStorage.setItem('authToken', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      queryClient.setQueryData(QUERY_KEYS.currentUser, data.user);
      toast.success('Welcome back!');
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Login failed');
    },
  });

  // Register mutation
  const registerMutation = useMutation({
    mutationFn: authApi.register,
    onSuccess: (user) => {
      toast.success('Account created successfully! Please log in.');
    },
    onError: (error: any) => {
      toast.error(error.detail || 'Registration failed');
    },
  });

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: authApi.logout,
    onSuccess: () => {
      queryClient.clear();
      toast.success('Logged out successfully');
    },
    onError: () => {
      // Clear local data even if API call fails
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      queryClient.clear();
    },
  });

  const login = (credentials: LoginForm) => {
    return loginMutation.mutateAsync(credentials);
  };

  const register = (userData: RegisterForm) => {
    return registerMutation.mutateAsync(userData);
  };

  const logout = () => {
    logoutMutation.mutate();
  };

  const state: AuthState = {
    user: user || null,
    isLoading: isLoading || loginMutation.isPending || registerMutation.isPending,
    isAuthenticated: !!user && !!localStorage.getItem('authToken'),
    error: error?.detail || null,
  };

  return {
    ...state,
    login,
    register,
    logout,
    isLoggingIn: loginMutation.isPending,
    isRegistering: registerMutation.isPending,
    loginError: loginMutation.error?.detail,
    registerError: registerMutation.error?.detail,
  };
};
