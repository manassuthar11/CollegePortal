/**
 * Chat Routes
 * Handles all chatbot-related API endpoints
 */

import { Router } from 'express';
import { body, query } from 'express-validator';
import {
  processChatMessage,
  getChatHistory,
  getUserSessions,
  clearChatHistory,
  getChatAnalytics,
  getSupportedLanguages,
} from '../controllers/chatController';
import { authenticate, authorize, optionalAuth } from '../middleware/authMiddleware';
import { SupportedLanguage, UserRole } from '../types';

const router = Router();

// Validation middleware
const validateChatMessage = [
  body('message')
    .trim()
    .isLength({ min: 1, max: 1000 })
    .withMessage('Message must be between 1 and 1000 characters'),
  body('language')
    .optional()
    .isIn(Object.values(SupportedLanguage))
    .withMessage('Invalid language specified'),
  body('sessionId')
    .optional()
    .isLength({ min: 10, max: 50 })
    .withMessage('Invalid session ID format'),
];

const validateHistoryQuery = [
  query('page')
    .optional()
    .isInt({ min: 1 })
    .withMessage('Page must be a positive integer'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('sessionId')
    .optional()
    .isLength({ min: 10, max: 50 })
    .withMessage('Invalid session ID format'),
];

const validateAnalyticsQuery = [
  query('startDate')
    .optional()
    .isISO8601()
    .withMessage('Invalid start date format'),
  query('endDate')
    .optional()
    .isISO8601()
    .withMessage('Invalid end date format'),
];

const validateClearHistory = [
  body('sessionId')
    .optional()
    .isLength({ min: 10, max: 50 })
    .withMessage('Invalid session ID format'),
];

// Public routes
router.get('/languages', getSupportedLanguages);

// Chat message processing (works with or without auth)
router.post('/message', optionalAuth, validateChatMessage, processChatMessage);

// Protected routes (require authentication)
router.get('/history', authenticate, validateHistoryQuery, getChatHistory);
router.get('/sessions', authenticate, getUserSessions);
router.delete('/history', authenticate, validateClearHistory, clearChatHistory);

// Admin only routes
router.get('/analytics', authenticate, authorize(UserRole.ADMIN), validateAnalyticsQuery, getChatAnalytics);

export default router;