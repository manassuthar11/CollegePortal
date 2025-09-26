/**
 * Announcement Routes
 * Handles all announcement-related API endpoints
 */

import { Router } from 'express';
import { body, query, param } from 'express-validator';
import {
  getPublicAnnouncements,
  getAnnouncementById,
  createAnnouncement,
  updateAnnouncement,
  deleteAnnouncement,
  getUrgentAnnouncements,
  getMyAnnouncements,
  getAnnouncementMetadata,
} from '../controllers/announcementController';
import { authenticate, authorize } from '../middleware/authMiddleware';
import { AnnouncementCategory, AnnouncementPriority, UserRole } from '../types';

const router = Router();

// Validation middleware
const validateAnnouncementCreation = [
  body('title')
    .trim()
    .isLength({ min: 5, max: 200 })
    .withMessage('Title must be between 5 and 200 characters'),
  body('content')
    .trim()
    .isLength({ min: 10, max: 5000 })
    .withMessage('Content must be between 10 and 5000 characters'),
  body('category')
    .isIn(Object.values(AnnouncementCategory))
    .withMessage('Invalid category specified'),
  body('priority')
    .isIn(Object.values(AnnouncementPriority))
    .withMessage('Invalid priority specified'),
  body('targetAudience')
    .isArray({ min: 1 })
    .withMessage('At least one target audience must be specified')
    .custom((audiences) => {
      const validRoles = Object.values(UserRole);
      return audiences.every((audience: string) => validRoles.includes(audience as UserRole));
    })
    .withMessage('Invalid target audience specified'),
  body('isPublished')
    .optional()
    .isBoolean()
    .withMessage('isPublished must be a boolean'),
  body('publishDate')
    .optional()
    .isISO8601()
    .withMessage('Invalid publish date format'),
  body('expiryDate')
    .optional()
    .isISO8601()
    .withMessage('Invalid expiry date format')
    .custom((value, { req }) => {
      if (value && req.body.publishDate && new Date(value) <= new Date(req.body.publishDate)) {
        throw new Error('Expiry date must be after publish date');
      }
      return true;
    }),
  body('tags')
    .optional()
    .isArray()
    .withMessage('Tags must be an array')
    .custom((tags) => {
      return tags.every((tag: string) => typeof tag === 'string' && tag.length <= 50);
    })
    .withMessage('Each tag must be a string with maximum 50 characters'),
  body('attachments')
    .optional()
    .isArray()
    .withMessage('Attachments must be an array'),
];

const validateAnnouncementUpdate = [
  body('title')
    .optional()
    .trim()
    .isLength({ min: 5, max: 200 })
    .withMessage('Title must be between 5 and 200 characters'),
  body('content')
    .optional()
    .trim()
    .isLength({ min: 10, max: 5000 })
    .withMessage('Content must be between 10 and 5000 characters'),
  body('category')
    .optional()
    .isIn(Object.values(AnnouncementCategory))
    .withMessage('Invalid category specified'),
  body('priority')
    .optional()
    .isIn(Object.values(AnnouncementPriority))
    .withMessage('Invalid priority specified'),
  body('targetAudience')
    .optional()
    .isArray({ min: 1 })
    .withMessage('At least one target audience must be specified')
    .custom((audiences) => {
      const validRoles = Object.values(UserRole);
      return audiences.every((audience: string) => validRoles.includes(audience as UserRole));
    })
    .withMessage('Invalid target audience specified'),
  body('isPublished')
    .optional()
    .isBoolean()
    .withMessage('isPublished must be a boolean'),
  body('publishDate')
    .optional()
    .isISO8601()
    .withMessage('Invalid publish date format'),
  body('expiryDate')
    .optional()
    .isISO8601()
    .withMessage('Invalid expiry date format'),
  body('tags')
    .optional()
    .isArray()
    .withMessage('Tags must be an array'),
  body('attachments')
    .optional()
    .isArray()
    .withMessage('Attachments must be an array'),
];

const validateAnnouncementQuery = [
  query('page')
    .optional()
    .isInt({ min: 1 })
    .withMessage('Page must be a positive integer'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 50 })
    .withMessage('Limit must be between 1 and 50'),
  query('category')
    .optional()
    .isIn(Object.values(AnnouncementCategory))
    .withMessage('Invalid category specified'),
  query('priority')
    .optional()
    .isIn(Object.values(AnnouncementPriority))
    .withMessage('Invalid priority specified'),
  query('targetRole')
    .optional()
    .isIn(Object.values(UserRole))
    .withMessage('Invalid target role specified'),
];

const validateIdParam = [
  param('id')
    .isMongoId()
    .withMessage('Invalid announcement ID'),
];

// Public routes
router.get('/metadata', getAnnouncementMetadata);
router.get('/urgent', getUrgentAnnouncements);
router.get('/', validateAnnouncementQuery, getPublicAnnouncements);
router.get('/:id', validateIdParam, getAnnouncementById);

// Protected routes (require authentication)
// Teacher and Admin can create announcements
router.post('/', 
  authenticate, 
  authorize(UserRole.TEACHER, UserRole.ADMIN), 
  validateAnnouncementCreation, 
  createAnnouncement
);

// Get my announcements (Teacher/Admin only)
router.get('/my/announcements', 
  authenticate, 
  authorize(UserRole.TEACHER, UserRole.ADMIN),
  query('status').optional().isIn(['published', 'draft']).withMessage('Invalid status'),
  validateAnnouncementQuery,
  getMyAnnouncements
);

// Update announcement (Author or Admin only)
router.put('/:id', 
  authenticate, 
  authorize(UserRole.TEACHER, UserRole.ADMIN), 
  validateIdParam, 
  validateAnnouncementUpdate, 
  updateAnnouncement
);

// Delete announcement (Author or Admin only)
router.delete('/:id', 
  authenticate, 
  authorize(UserRole.TEACHER, UserRole.ADMIN), 
  validateIdParam, 
  deleteAnnouncement
);

export default router;