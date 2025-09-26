/**
 * TypeScript interfaces and types for the College Portal application
 * Defines data structures used throughout the application
 */

import { Document } from 'mongoose';

// Base interface for all documents
export interface IBaseDocument extends Document {
  createdAt: Date;
  updatedAt: Date;
}

// User related interfaces
export interface IUser extends IBaseDocument {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  role: UserRole;
  isActive: boolean;
  lastLogin?: Date;
  profilePicture?: string;
  studentId?: string;
  department?: string;
  year?: number;
  comparePassword(password: string): Promise<boolean>;
}

export enum UserRole {
  STUDENT = 'student',
  TEACHER = 'teacher',
  ADMIN = 'admin',
}

// Authentication related interfaces
export interface IAuthRequest {
  email: string;
  password: string;
}

export interface IRegisterRequest extends IAuthRequest {
  firstName: string;
  lastName: string;
  role?: UserRole;
  studentId?: string;
  department?: string;
  year?: number;
}

export interface IAuthResponse {
  success: boolean;
  message: string;
  token?: string;
  user?: Partial<IUser>;
}

// Chat and Chatbot related interfaces
export interface IChatMessage extends IBaseDocument {
  userId: string;
  message: string;
  response: string;
  language: SupportedLanguage;
  confidence?: number;
  responseTime?: number;
  isFromRAG: boolean;
  context?: string[];
  sessionId: string;
}

export enum SupportedLanguage {
  ENGLISH = 'en',
  HINDI = 'hi',
  RAJASTHANI = 'raj',
}

export interface IChatRequest {
  message: string;
  language?: SupportedLanguage;
  sessionId?: string;
  userId?: string;
}

export interface IChatResponse {
  success: boolean;
  response: string;
  language: SupportedLanguage;
  confidence?: number;
  responseTime: number;
  sessionId: string;
}

// Announcement related interfaces
export interface IAnnouncement extends IBaseDocument {
  title: string;
  content: string;
  author: string; // User ID reference
  category: AnnouncementCategory;
  priority: AnnouncementPriority;
  isPublished: boolean;
  publishDate?: Date;
  expiryDate?: Date;
  targetAudience: UserRole[];
  attachments?: string[];
  viewCount: number;
  tags: string[];
  // Virtual properties
  isExpired: boolean;
  isActive: boolean;
  // Instance methods
  incrementViewCount(): Promise<void>;
}

// Model interface for static methods
export interface IAnnouncementModel {
  getPublished(targetRole?: UserRole, category?: AnnouncementCategory, limit?: number, skip?: number): Promise<IAnnouncement[]>;
  getUrgent(targetRole: UserRole): Promise<IAnnouncement[]>;
  search(query: string, filters?: any): Promise<IAnnouncement[]>;
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

// RAG and Language Processing interfaces
export interface IDocumentChunk {
  id: string;
  content: string;
  metadata: {
    source: string;
    language: SupportedLanguage;
    category: string;
    lastUpdated: Date;
  };
  embedding?: number[];
}

export interface ILanguageDetectionResult {
  language: SupportedLanguage;
  confidence: number;
  alternatives?: {
    language: SupportedLanguage;
    confidence: number;
  }[];
}

export interface IRAGResult {
  answer: string;
  context: string[];
  confidence: number;
  sources: string[];
  language: SupportedLanguage;
}

// API Response interfaces
export interface IAPIResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
  timestamp: Date;
}

export interface IPaginatedResponse<T> extends IAPIResponse<T[]> {
  pagination: {
    currentPage: number;
    totalPages: number;
    totalItems: number;
    itemsPerPage: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

// Environment configuration
export interface IEnvironmentConfig {
  NODE_ENV: string;
  PORT: number;
  MONGODB_URI: string;
  JWT_SECRET: string;
  JWT_EXPIRE: string;
  BCRYPT_SALT_ROUNDS: number;
  HUGGINGFACE_API_KEY?: string;
  CHROMA_DB_PATH: string;
  RATE_LIMIT_WINDOW_MS: number;
  RATE_LIMIT_MAX_REQUESTS: number;
}

// Express Request with User
export interface IAuthenticatedRequest extends Express.Request {
  user?: IUser;
}

// Middleware interfaces
export interface IErrorResponse {
  success: false;
  message: string;
  error?: string;
  stack?: string;
  statusCode: number;
}

export interface IValidationError {
  field: string;
  message: string;
  value?: any;
}