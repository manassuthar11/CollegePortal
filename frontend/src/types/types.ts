/**
 * Frontend Type Definitions
 * TypeScript interfaces and types for the College Portal frontend
 */

// User and Authentication Types
export interface User {
  _id: string;
  firstName: string;
  lastName: string;
  email: string;
  role: UserRole;
  studentId?: string;
  department?: string;
  year?: number;
  profilePicture?: string;
  isActive: boolean;
  lastLogin?: string;
  createdAt: string;
  updatedAt: string;
}

export enum UserRole {
  STUDENT = 'student',
  TEACHER = 'teacher',
  ADMIN = 'admin',
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  role?: UserRole;
  studentId?: string;
  department?: string;
  year?: number;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  token?: string;
  user?: User;
}

// Chat and Chatbot Types
export interface ChatMessage {
  _id: string;
  userId: string;
  message: string;
  response: string;
  language: SupportedLanguage;
  confidence?: number;
  responseTime?: number;
  isFromRAG: boolean;
  context?: string[];
  sessionId: string;
  createdAt: string;
  updatedAt: string;
}

// Simplified chat message for frontend
export interface SimpleChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  language: 'en' | 'hi' | 'raj';
}

export enum SupportedLanguage {
  ENGLISH = 'en',
  HINDI = 'hi',
  RAJASTHANI = 'raj',
}

export interface ChatRequest {
  message: string;
  language?: SupportedLanguage;
  sessionId?: string;
}

export interface ChatResponse {
  success: boolean;
  response: string;
  language: SupportedLanguage;
  confidence?: number;
  responseTime: number;
  sessionId: string;
  timestamp: string;
  sources?: string[];
}

export interface ChatState {
  messages: SimpleChatMessage[];
  isLoading: boolean;
  currentSessionId: string | null;
  selectedLanguage: SupportedLanguage;
  isConnected: boolean;
}

export interface LanguageOption {
  code: SupportedLanguage;
  name: string;
  nativeName: string;
  flag: string;
}

export interface ChatContextType {
  messages: SimpleChatMessage[];
  isLoading: boolean;
  currentLanguage: 'en' | 'hi' | 'raj';
  sendMessage: (message: string) => Promise<void>;
  clearMessages: () => void;
  loadChatHistory: () => Promise<void>;
  changeLanguage: (language: 'en' | 'hi' | 'raj') => void;
}

// Announcement Types
export interface Announcement {
  _id: string;
  title: string;
  content: string;
  author: {
    _id: string;
    firstName: string;
    lastName: string;
  };
  category: AnnouncementCategory;
  priority: AnnouncementPriority;
  isPublished: boolean;
  publishDate?: string;
  expiryDate?: string;
  targetAudience: UserRole[];
  attachments?: string[];
  viewCount: number;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export enum AnnouncementCategory {
  ACADEMIC = 'academic',
  ADMINISTRATIVE = 'administrative',
  EVENT = 'event',
  EMERGENCY = 'emergency',
  GENERAL = 'general',
}

export enum AnnouncementPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

// API Response Types
export interface APIResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
  timestamp: string;
}

export interface PaginatedResponse<T> extends APIResponse<T[]> {
  pagination: {
    currentPage: number;
    totalPages: number;
    totalItems: number;
    itemsPerPage: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

// UI Component Types
export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface NotificationState {
  show: boolean;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
}

export interface ModalState {
  isOpen: boolean;
  title?: string;
  content?: any;
  onClose?: () => void;
  onConfirm?: () => void;
}

// Theme Types
export interface ThemeState {
  isDark: boolean;
  primaryColor: string;
  fontSize: 'small' | 'medium' | 'large';
}

// Context Types
export interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  updateProfile: (data: Partial<User>) => Promise<void>;
}

// Remove duplicate ChatContextType - use the simpler one defined earlier

export interface ThemeContextType {
  theme: ThemeState;
  toggleTheme: () => void;
  setPrimaryColor: (color: string) => void;
  setFontSize: (size: 'small' | 'medium' | 'large') => void;
}

// Component Props Types
export interface BaseComponentProps {
  className?: string;
  children?: any;
}

export interface ButtonProps extends BaseComponentProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}

export interface InputProps extends BaseComponentProps {
  type?: string;
  name: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  label?: string;
  required?: boolean;
}

export interface CardProps extends BaseComponentProps {
  title?: string;
  subtitle?: string;
  hoverable?: boolean;
  loading?: boolean;
  actions?: any;
}