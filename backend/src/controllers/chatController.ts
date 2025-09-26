/**
 * Chatbot Controller
 * Handles multilingual chat interactions and RAG processing
 */

import { Request, Response, NextFunction } from 'express';
import { validationResult } from 'express-validator';
import { ChatMessage } from '../models';
import { IChatRequest, SupportedLanguage } from '../types';
import { AppError, asyncHandler } from '../middleware/errorMiddleware';
import { processRAGQuery, getDocumentStats } from '../utils/ragUtils';
import { detectLanguage, getGreeting } from '../utils/languageUtils';

// Generate session ID
const generateSessionId = (): string => {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * @desc    Process chat message and get bot response
 * @route   POST /api/chat/message
 * @access  Public (can be used with or without auth)
 */
export const processChatMessage = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return next(new AppError('Validation failed', 400));
    }

    const { message, language, sessionId }: IChatRequest = req.body;
    const userId = req.user?._id?.toString() || 'anonymous';
    const startTime = Date.now();

    try {
      // Detect or validate language
      let detectedLanguage = language;
      if (!language) {
        const languageResult = detectLanguage(message);
        detectedLanguage = languageResult.language;
      }

      // Handle greeting messages
      const isGreeting = /^(hi|hello|hey|namaste|राम राम|नमस्ते)/i.test(message.trim());
      if (isGreeting) {
        const greeting = getGreeting(detectedLanguage!);
        
        const chatMessage = new ChatMessage({
          userId,
          message: message.trim(),
          response: greeting,
          language: detectedLanguage,
          confidence: 0.9,
          responseTime: Date.now() - startTime,
          isFromRAG: false,
          context: [],
          sessionId: sessionId || generateSessionId(),
        });

        await chatMessage.save();

        res.status(200).json({
          success: true,
          response: greeting,
          language: detectedLanguage,
          confidence: 0.9,
          responseTime: Date.now() - startTime,
          sessionId: chatMessage.sessionId,
          timestamp: new Date(),
        });
        return;
      }

      // Process with RAG
      const ragResult = await processRAGQuery(message, detectedLanguage);
      
      // Save chat message to database
      const chatMessage = new ChatMessage({
        userId,
        message: message.trim(),
        response: ragResult.answer,
        language: ragResult.language,
        confidence: ragResult.confidence,
        responseTime: Date.now() - startTime,
        isFromRAG: true,
        context: ragResult.context,
        sessionId: sessionId || generateSessionId(),
      });

      await chatMessage.save();

      // Send response
      res.status(200).json({
        success: true,
        response: ragResult.answer,
        language: ragResult.language,
        confidence: ragResult.confidence,
        responseTime: Date.now() - startTime,
        sessionId: chatMessage.sessionId,
        timestamp: new Date(),
        sources: ragResult.sources,
      });

    } catch (error) {
      console.error('Error processing chat message:', error);
      next(new AppError('Failed to process chat message', 500));
    }
  }
);

/**
 * @desc    Get chat history for authenticated user
 * @route   GET /api/chat/history
 * @access  Private
 */
export const getChatHistory = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const userId = req.user._id.toString();
    const { page = 1, limit = 50, sessionId } = req.query;

    try {
      let query: any = { userId };
      
      if (sessionId) {
        query.sessionId = sessionId;
      }

      const messages = await ChatMessage.find(query)
        .sort({ createdAt: -1 })
        .limit(limit * 1)
        .skip((page - 1) * limit)
        .select('-__v');

      const totalMessages = await ChatMessage.countDocuments(query);
      const totalPages = Math.ceil(totalMessages / limit);

      res.status(200).json({
        success: true,
        message: 'Chat history retrieved successfully',
        data: messages.reverse(), // Reverse to show chronological order
        pagination: {
          currentPage: parseInt(page),
          totalPages,
          totalItems: totalMessages,
          itemsPerPage: parseInt(limit),
          hasNext: page < totalPages,
          hasPrev: page > 1,
        },
      });

    } catch (error) {
      console.error('Error fetching chat history:', error);
      next(new AppError('Failed to fetch chat history', 500));
    }
  }
);

/**
 * @desc    Get user's active chat sessions
 * @route   GET /api/chat/sessions
 * @access  Private
 */
export const getUserSessions = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const userId = req.user._id.toString();

    try {
      const sessions = await ChatMessage.aggregate([
        { $match: { userId } },
        {
          $group: {
            _id: '$sessionId',
            lastMessage: { $last: '$message' },
            lastResponse: { $last: '$response' },
            messageCount: { $sum: 1 },
            lastActivity: { $max: '$createdAt' },
            language: { $last: '$language' },
          }
        },
        { $sort: { lastActivity: -1 } },
        { $limit: 10 }
      ]);

      res.status(200).json({
        success: true,
        message: 'Chat sessions retrieved successfully',
        data: sessions,
      });

    } catch (error) {
      console.error('Error fetching chat sessions:', error);
      next(new AppError('Failed to fetch chat sessions', 500));
    }
  }
);

/**
 * @desc    Clear chat history for user
 * @route   DELETE /api/chat/history
 * @access  Private
 */
export const clearChatHistory = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const userId = req.user._id.toString();
    const { sessionId } = req.body;

    try {
      let deleteQuery: any = { userId };
      
      if (sessionId) {
        deleteQuery.sessionId = sessionId;
      }

      const result = await ChatMessage.deleteMany(deleteQuery);

      res.status(200).json({
        success: true,
        message: sessionId 
          ? 'Session history cleared successfully' 
          : 'Chat history cleared successfully',
        deletedCount: result.deletedCount,
      });

    } catch (error) {
      console.error('Error clearing chat history:', error);
      next(new AppError('Failed to clear chat history', 500));
    }
  }
);

/**
 * @desc    Get chatbot analytics and statistics
 * @route   GET /api/chat/analytics
 * @access  Private (Admin only)
 */
export const getChatAnalytics = asyncHandler(
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const { startDate, endDate } = req.query;

    try {
      const start = startDate ? new Date(startDate as string) : new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
      const end = endDate ? new Date(endDate as string) : new Date();

      // Get message statistics
      const messageStats = await ChatMessage.aggregate([
        {
          $match: {
            createdAt: { $gte: start, $lte: end }
          }
        },
        {
          $group: {
            _id: null,
            totalMessages: { $sum: 1 },
            avgConfidence: { $avg: '$confidence' },
            avgResponseTime: { $avg: '$responseTime' },
            uniqueUsers: { $addToSet: '$userId' },
            uniqueSessions: { $addToSet: '$sessionId' },
          }
        }
      ]);

      // Get language distribution
      const languageStats = await ChatMessage.aggregate([
        {
          $match: {
            createdAt: { $gte: start, $lte: end }
          }
        },
        {
          $group: {
            _id: '$language',
            count: { $sum: 1 },
            avgConfidence: { $avg: '$confidence' }
          }
        },
        { $sort: { count: -1 } }
      ]);

      // Get daily message counts
      const dailyStats = await ChatMessage.aggregate([
        {
          $match: {
            createdAt: { $gte: start, $lte: end }
          }
        },
        {
          $group: {
            _id: {
              year: { $year: '$createdAt' },
              month: { $month: '$createdAt' },
              day: { $dayOfMonth: '$createdAt' }
            },
            messageCount: { $sum: 1 },
            uniqueUsers: { $addToSet: '$userId' }
          }
        },
        { $sort: { '_id.year': 1, '_id.month': 1, '_id.day': 1 } }
      ]);

      // Get document statistics
      const documentStats = getDocumentStats();

      const analytics = {
        messageStats: messageStats[0] || {
          totalMessages: 0,
          avgConfidence: 0,
          avgResponseTime: 0,
          uniqueUsers: [],
          uniqueSessions: []
        },
        languageStats,
        dailyStats,
        documentStats,
        dateRange: { start, end }
      };

      // Add computed fields
      analytics.messageStats.uniqueUserCount = analytics.messageStats.uniqueUsers.length;
      analytics.messageStats.uniqueSessionCount = analytics.messageStats.uniqueSessions.length;
      delete analytics.messageStats.uniqueUsers;
      delete analytics.messageStats.uniqueSessions;

      res.status(200).json({
        success: true,
        message: 'Chat analytics retrieved successfully',
        data: analytics,
      });

    } catch (error) {
      console.error('Error fetching chat analytics:', error);
      next(new AppError('Failed to fetch chat analytics', 500));
    }
  }
);

/**
 * @desc    Get supported languages
 * @route   GET /api/chat/languages
 * @access  Public
 */
export const getSupportedLanguages = asyncHandler(
  async (req: Request, res: Response): Promise<void> => {
    const languages = [
      {
        code: SupportedLanguage.ENGLISH,
        name: 'English',
        nativeName: 'English',
        flag: '🇺🇸'
      },
      {
        code: SupportedLanguage.HINDI,
        name: 'Hindi',
        nativeName: 'हिंदी',
        flag: '🇮🇳'
      },
      {
        code: SupportedLanguage.RAJASTHANI,
        name: 'Rajasthani',
        nativeName: 'राजस्थानी',
        flag: '🏴󠁩󠁮󠁲󠁪󠁿'
      }
    ];

    res.status(200).json({
      success: true,
      message: 'Supported languages retrieved successfully',
      data: languages,
    });
  }
);