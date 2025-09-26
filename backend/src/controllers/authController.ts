/**
 * Authentication Controller
 * Handles user registration, login, and profile management
 */

import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { validationResult } from 'express-validator';
import { User } from '../models';
import { IAuthResponse, UserRole } from '../types';
import { AppError, asyncHandler } from '../middleware/errorMiddleware';

// Generate JWT Token
const generateToken = (id: string): string => {
  const jwtSecret = process.env.JWT_SECRET;
  const jwtExpire = process.env.JWT_EXPIRE || '30d';
  
  if (!jwtSecret) {
    throw new AppError('Server configuration error', 500);
  }

  return jwt.sign({ id }, jwtSecret, {
    expiresIn: jwtExpire,
  } as jwt.SignOptions);
};

/**
 * @desc    Register new user
 * @route   POST /api/auth/register
 * @access  Public
 */
export const registerUser = asyncHandler(
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return next(new AppError('Validation failed', 400));
    }

    const { 
      firstName, 
      lastName, 
      email, 
      password, 
      role = UserRole.STUDENT,
      studentId,
      department,
      year 
    } = req.body;

    // Check if user already exists
    const existingUser = await User.findOne({ email: email.toLowerCase() });
    if (existingUser) {
      return next(new AppError('User already exists with this email', 400));
    }

    // Check if student ID is already taken (for students only)
    if (role === UserRole.STUDENT && studentId) {
      const existingStudent = await User.findOne({ studentId });
      if (existingStudent) {
        return next(new AppError('Student ID already exists', 400));
      }
    }

    // Create user
    const user = await User.create({
      firstName,
      lastName,
      email: email.toLowerCase(),
      password,
      role,
      studentId: role === UserRole.STUDENT ? studentId : undefined,
      department,
      year: role === UserRole.STUDENT ? year : undefined,
    });

    // Generate token
    const token = generateToken(user._id.toString());

    const response: IAuthResponse = {
      success: true,
      message: 'User registered successfully',
      token,
      user: {
        _id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        studentId: user.studentId,
        department: user.department,
        year: user.year,
        isActive: user.isActive,
        createdAt: user.createdAt,
      },
    };

    res.status(201).json(response);
  }
);

/**
 * @desc    Login user
 * @route   POST /api/auth/login
 * @access  Public
 */
export const loginUser = asyncHandler(
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return next(new AppError('Validation failed', 400));
    }

    const { email, password } = req.body;

    // Find user by email
    const user = await User.findOne({ email: email.toLowerCase() }).select('+password');
    if (!user) {
      return next(new AppError('Invalid credentials', 401));
    }

    // Check if account is active
    if (!user.isActive) {
      return next(new AppError('Account is deactivated. Please contact administrator.', 401));
    }

    // Check password
    const isPasswordCorrect = await user.comparePassword(password);
    if (!isPasswordCorrect) {
      return next(new AppError('Invalid credentials', 401));
    }

    // Update last login
    user.lastLogin = new Date();
    await user.save();

    // Generate token
    const token = generateToken(user._id.toString());

    const response: IAuthResponse = {
      success: true,
      message: 'Login successful',
      token,
      user: {
        _id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        studentId: user.studentId,
        department: user.department,
        year: user.year,
        isActive: user.isActive,
        lastLogin: user.lastLogin,
        createdAt: user.createdAt,
      },
    };

    res.status(200).json(response);
  }
);

/**
 * @desc    Get current user profile
 * @route   GET /api/auth/profile
 * @access  Private
 */
export const getUserProfile = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const user = req.user;

    if (!user) {
      return next(new AppError('User not found', 404));
    }

    res.status(200).json({
      success: true,
      message: 'User profile retrieved successfully',
      data: {
        _id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        studentId: user.studentId,
        department: user.department,
        year: user.year,
        isActive: user.isActive,
        lastLogin: user.lastLogin,
        createdAt: user.createdAt,
        updatedAt: user.updatedAt,
      },
    });
  }
);

/**
 * @desc    Update user profile
 * @route   PUT /api/auth/profile
 * @access  Private
 */
export const updateUserProfile = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const user = req.user;
    const { firstName, lastName, department, year, profilePicture } = req.body;

    if (!user) {
      return next(new AppError('User not found', 404));
    }

    // Update allowed fields
    if (firstName) user.firstName = firstName;
    if (lastName) user.lastName = lastName;
    if (department) user.department = department;
    if (year && user.role === UserRole.STUDENT) user.year = year;
    if (profilePicture) user.profilePicture = profilePicture;

    await user.save();

    res.status(200).json({
      success: true,
      message: 'Profile updated successfully',
      data: {
        _id: user._id,
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        role: user.role,
        studentId: user.studentId,
        department: user.department,
        year: user.year,
        profilePicture: user.profilePicture,
        isActive: user.isActive,
        updatedAt: user.updatedAt,
      },
    });
  }
);

/**
 * @desc    Change password
 * @route   PUT /api/auth/change-password
 * @access  Private
 */
export const changePassword = asyncHandler(
  async (req: any, res: Response, next: NextFunction): Promise<void> => {
    const user = await User.findById(req.user._id).select('+password');
    const { currentPassword, newPassword } = req.body;

    if (!user) {
      return next(new AppError('User not found', 404));
    }

    // Verify current password
    const isCurrentPasswordCorrect = await user.comparePassword(currentPassword);
    if (!isCurrentPasswordCorrect) {
      return next(new AppError('Current password is incorrect', 400));
    }

    // Update password
    user.password = newPassword;
    await user.save();

    res.status(200).json({
      success: true,
      message: 'Password changed successfully',
    });
  }
);