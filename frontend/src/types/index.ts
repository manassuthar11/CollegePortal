/**
 * TypeScript type definitions for the College Portal Frontend
 * Defines interfaces and types used throughout the React application
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
  isActive: boolean;
  profilePicture?: string;
  lastLogin?: Date;
  createdAt: Date;
  updatedAt: Date;
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

export interface RegisterData extends LoginCredentials {
  firstName: string;
  lastName: string;
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
export enum SupportedLanguage {
  ENGLISH = 'en',
  HINDI = 'hi',
  RAJASTHANI = 'raj',
}

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
  timestamp: Date;
  isUser: boolean; // For UI distinction
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
  timestamp: Date;
}

export interface ChatState {
  messages: ChatMessage[];
  isTyping: boolean;
  currentSession: string;
  selectedLanguage: SupportedLanguage;
  isConnected: boolean;
}

// Announcement Types
export interface Announcement {
  _id: string;
  title: string;
  content: string;
  author: string;
  category: AnnouncementCategory;
  priority: AnnouncementPriority;
  isPublished: boolean;
  publishDate?: Date;
  expiryDate?: Date;
  targetAudience: UserRole[];
  attachments?: string[];
  viewCount: number;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
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
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
  timestamp: Date;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
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
export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showCloseButton?: boolean;
}

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export interface SelectOption {
  value: string;
  label: string;
  icon?: React.ReactNode;
}

export interface SelectProps {
  options: SelectOption[];
  value?: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  label?: string;
  disabled?: boolean;
  multiple?: boolean;
}

// Navigation and Routing Types
export interface NavItem {
  name: string;
  path: string;
  icon?: React.ReactNode;
  badge?: string;
  children?: NavItem[];
}

export interface BreadcrumbItem {
  label: string;
  path?: string;
  icon?: React.ReactNode;
}

// Language and Localization Types
export interface LanguageOption {
  code: SupportedLanguage;
  name: string;
  nativeName: string;
  flag: string;
}

export interface TranslationStrings {
  [key: string]: string | TranslationStrings;
}

// Theme Types
export interface ThemeConfig {
  mode: 'light' | 'dark';
  primaryColor: string;
  secondaryColor: string;
  fontFamily: string;
  borderRadius: string;
}

// Error Types
export interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: React.ErrorInfo;
}

export interface ApiError {
  message: string;
  statusCode: number;
  errors?: ValidationError[];
}

export interface ValidationError {
  field: string;
  message: string;
  value?: any;
}

// Feature Flag Types
export interface FeatureFlags {
  enableChatbot: boolean;
  enableMultipleLanguages: boolean;
  enableAnnouncements: boolean;
  enableProfilePictures: boolean;
  enableNotifications: boolean;
}

// Analytics Types
export interface AnalyticsEvent {
  event: string;
  category: string;
  label?: string;
  value?: number;
  userId?: string;
  sessionId?: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

// Search Types
export interface SearchResult {
  id: string;
  title: string;
  excerpt: string;
  type: 'announcement' | 'page' | 'document';
  url: string;
  relevanceScore: number;
  highlightedFields?: Record<string, string>;
}

export interface SearchQuery {
  query: string;
  filters?: SearchFilters;
  sort?: SearchSort;
  pagination?: {
    page: number;
    limit: number;
  };
}

export interface SearchFilters {
  type?: string[];
  category?: string[];
  dateRange?: {
    start: Date;
    end: Date;
  };
  author?: string[];
  tags?: string[];
}

export interface SearchSort {
  field: string;
  direction: 'asc' | 'desc';
}

// Utility Types
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

export type RequireAtLeastOne<T, Keys extends keyof T = keyof T> =
  Pick<T, Exclude<keyof T, Keys>>
  & {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>
  }[Keys];

// Environment Configuration
export interface Environment {
  API_URL: string;
  ENVIRONMENT: 'development' | 'staging' | 'production';
  ENABLE_ANALYTICS: boolean;
  ENABLE_ERROR_REPORTING: boolean;
  CHATBOT_TIMEOUT: number;
  MAX_FILE_SIZE: number;
}

// Export default environment type
export interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_ENVIRONMENT: string;
  readonly VITE_ENABLE_ANALYTICS?: string;
  readonly VITE_ENABLE_ERROR_REPORTING?: string;
  readonly VITE_CHATBOT_TIMEOUT?: string;
  readonly VITE_MAX_FILE_SIZE?: string;
}

export interface ImportMeta {
  readonly env: ImportMetaEnv;
}