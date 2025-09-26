/**
 * Announcement Controller
 * Handles college announcements and notifications CRUD operations
 */

import { Request, Response, NextFunction } from 'express';
import { validationResult } from 'express-validator';
import { Announcement } from '../models';
import { AnnouncementCategory, AnnouncementPriority, UserRole } from '../types';
import { AppError, asyncHandler } from '../middleware/errorMiddleware';

/**
 * @desc    Get all published announcements
 * @route   GET /api/announcements
 * @access  Public
 */
export const getPublicAnnouncements = asyncHandler(
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const { 
      page = 1, 
      limit = 10, 
      category, 
      priority, 
      targetRole 
    } = req.query;

    try {
      const announcements = await Announcement.getPublished(
        targetRole as UserRole,
        category as AnnouncementCategory,
        parseInt(limit as string),
        (parseInt(page as string) - 1) * parseInt(limit as string)
      );

      const totalCount = await Announcement.countDocuments({
        isPublished: true,
        $or: [
          { expiryDate: { $exists: false } },
          { expiryDate: { $gt: new Date() } }
        ],
        ...(category && { category }),
        ...(priority && { priority }),
        ...(targetRole && { targetAudience: targetRole }),
      });

      const totalPages = Math.ceil(totalCount / parseInt(limit as string));

      res.status(200).json({
        success: true,
        message: 'Announcements retrieved successfully',
        data: announcements,
        pagination: {
          currentPage: parseInt(page as string),
          totalPages,
          totalItems: totalCount,
          itemsPerPage: parseInt(limit as string),
          hasNext: parseInt(page as string) < totalPages,
          hasPrev: parseInt(page as string) > 1,
        },
      });

    } catch (error) {
      console.error('Error fetching announcements:', error);
      next(new AppError('Failed to fetch announcements', 500));
    }
  }
);

/**
 * @desc    Get single announcement by ID
 * @route   GET /api/announcements/:id
 * @access  Public
 */
export const getAnnouncementById = asyncHandler(
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const { id } = req.params;

    try {
      const announcement = await Announcement.findById(id)
        .populate('author', 'firstName lastName')
        .select('-__v');

      if (!announcement) {
        return next(new AppError('Announcement not found', 404));
      }

      // Check if announcement is published (unless user is admin)
      if (!announcement.isPublished && (req as any).user?.role !== UserRole.ADMIN) {
        return next(new AppError('Announcement not found', 404));
      }

      // Increment view count
      await announcement.incrementViewCount();

      res.status(200).json({
        success: true,
        message: 'Announcement retrieved successfully',
        data: announcement,
      });

    } catch (error) {
      console.error('Error fetching announcement:', error);
      next(new AppError('Failed to fetch announcement', 500));
    }
  }
);

/**
 * @desc    Create new announcement
 * @route   POST /api/announcements
 * @access  Private (Admin/Teacher only)
 */
export const createAnnouncement = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return next(new AppError('Validation failed', 400));
    }

    const {
      title,
      content,
      category,
      priority,
      targetAudience,
      isPublished = false,
      publishDate,
      expiryDate,
      tags = [],
      attachments = [],
    } = req.body;

    try {
      const announcement = await Announcement.create({
        title,
        content,
        author: req.user._id,
        category,
        priority,
        targetAudience,
        isPublished,
        publishDate: publishDate ? new Date(publishDate) : undefined,
        expiryDate: expiryDate ? new Date(expiryDate) : undefined,
        tags,
        attachments,
      });

      await announcement.populate('author', 'firstName lastName');

      res.status(201).json({
        success: true,
        message: 'Announcement created successfully',
        data: announcement,
      });

    } catch (error) {
      console.error('Error creating announcement:', error);
      next(new AppError('Failed to create announcement', 500));
    }
  }
);

/**
 * @desc    Update announcement
 * @route   PUT /api/announcements/:id
 * @access  Private (Admin/Author only)
 */
export const updateAnnouncement = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return next(new AppError('Validation failed', 400));
    }

    const { id } = req.params;
    const {
      title,
      content,
      category,
      priority,
      targetAudience,
      isPublished,
      publishDate,
      expiryDate,
      tags,
      attachments,
    } = req.body;

    try {
      const announcement = await Announcement.findById(id);

      if (!announcement) {
        return next(new AppError('Announcement not found', 404));
      }

      // Check permissions (admin can edit all, others can only edit their own)
      if (req.user.role !== UserRole.ADMIN && announcement.author.toString() !== req.user._id.toString()) {
        return next(new AppError('Not authorized to update this announcement', 403));
      }

      // Update fields
      if (title !== undefined) announcement.title = title;
      if (content !== undefined) announcement.content = content;
      if (category !== undefined) announcement.category = category;
      if (priority !== undefined) announcement.priority = priority;
      if (targetAudience !== undefined) announcement.targetAudience = targetAudience;
      if (isPublished !== undefined) announcement.isPublished = isPublished;
      if (publishDate !== undefined) announcement.publishDate = publishDate ? new Date(publishDate) : undefined;
      if (expiryDate !== undefined) announcement.expiryDate = expiryDate ? new Date(expiryDate) : undefined;
      if (tags !== undefined) announcement.tags = tags;
      if (attachments !== undefined) announcement.attachments = attachments;

      await announcement.save();
      await announcement.populate('author', 'firstName lastName');

      res.status(200).json({
        success: true,
        message: 'Announcement updated successfully',
        data: announcement,
      });

    } catch (error) {
      console.error('Error updating announcement:', error);
      next(new AppError('Failed to update announcement', 500));
    }
  }
);

/**
 * @desc    Delete announcement
 * @route   DELETE /api/announcements/:id
 * @access  Private (Admin/Author only)
 */
export const deleteAnnouncement = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const { id } = req.params;

    try {
      const announcement = await Announcement.findById(id);

      if (!announcement) {
        return next(new AppError('Announcement not found', 404));
      }

      // Check permissions (admin can delete all, others can only delete their own)
      if (req.user.role !== UserRole.ADMIN && announcement.author.toString() !== req.user._id.toString()) {
        return next(new AppError('Not authorized to delete this announcement', 403));
      }

      await Announcement.findByIdAndDelete(id);

      res.status(200).json({
        success: true,
        message: 'Announcement deleted successfully',
      });

    } catch (error) {
      console.error('Error deleting announcement:', error);
      next(new AppError('Failed to delete announcement', 500));
    }
  }
);

/**
 * @desc    Get urgent announcements
 * @route   GET /api/announcements/urgent
 * @access  Public
 */
export const getUrgentAnnouncements = asyncHandler(
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const { targetRole } = req.query;

    try {
      const urgentAnnouncements = await Announcement.getUrgent(targetRole as UserRole);

      res.status(200).json({
        success: true,
        message: 'Urgent announcements retrieved successfully',
        data: urgentAnnouncements,
      });

    } catch (error) {
      console.error('Error fetching urgent announcements:', error);
      next(new AppError('Failed to fetch urgent announcements', 500));
    }
  }
);

/**
 * @desc    Get my announcements (created by current user)
 * @route   GET /api/announcements/my
 * @access  Private (Teacher/Admin only)
 */
export const getMyAnnouncements = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const { page = 1, limit = 10, status } = req.query;

    try {
      let query: any = { author: req.user._id };

      if (status === 'published') {
        query.isPublished = true;
      } else if (status === 'draft') {
        query.isPublished = false;
      }

      const announcements = await Announcement.find(query)
        .populate('author', 'firstName lastName')
        .sort({ createdAt: -1 })
        .limit(parseInt(limit as string))
        .skip((parseInt(page as string) - 1) * parseInt(limit as string))
        .select('-__v');

      const totalCount = await Announcement.countDocuments(query);
      const totalPages = Math.ceil(totalCount / parseInt(limit as string));

      res.status(200).json({
        success: true,
        message: 'My announcements retrieved successfully',
        data: announcements,
        pagination: {
          currentPage: parseInt(page as string),
          totalPages,
          totalItems: totalCount,
          itemsPerPage: parseInt(limit as string),
          hasNext: parseInt(page as string) < totalPages,
          hasPrev: parseInt(page as string) > 1,
        },
      });

    } catch (error) {
      console.error('Error fetching my announcements:', error);
      next(new AppError('Failed to fetch my announcements', 500));
    }
  }
);

/**
 * @desc    Get announcement categories and priorities
 * @route   GET /api/announcements/metadata
 * @access  Public
 */
export const getAnnouncementMetadata = asyncHandler(
  async (req: Request, res: Response): Promise<void> => {
    const metadata = {
      categories: Object.values(AnnouncementCategory).map(category => ({
        value: category,
        label: category.charAt(0).toUpperCase() + category.slice(1),
      })),
      priorities: Object.values(AnnouncementPriority).map(priority => ({
        value: priority,
        label: priority.charAt(0).toUpperCase() + priority.slice(1),
      })),
      targetAudiences: Object.values(UserRole).map(role => ({
        value: role,
        label: role.charAt(0).toUpperCase() + role.slice(1),
      })),
    };

    res.status(200).json({
      success: true,
      message: 'Announcement metadata retrieved successfully',
      data: metadata,
    });
  }
);