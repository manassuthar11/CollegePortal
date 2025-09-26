# 🚀 How to Run the College Portal Application

## Quick Start

### Option 1: Automated Start (Recommended)
Simply double-click `start-application.bat` in the root directory. This will:
- Start the backend server on http://localhost:5000
- Start the frontend server on http://localhost:5173
- Open your browser automatically

### Option 2: Manual Start

#### Step 1: Start Backend Server
```bash
# Open terminal in backend directory
cd backend
npm run dev
```

#### Step 2: Start Frontend Server (in a new terminal)
```bash
# Open another terminal in frontend directory
cd frontend
npm run dev
```

## Prerequisites

### 1. Node.js and npm
- Ensure Node.js (v16 or higher) is installed
- Check with: `node --version` and `npm --version`

### 2. MongoDB Database
You have two options:

#### Option A: Local MongoDB
- Install MongoDB Community Server from https://www.mongodb.com/try/download/community
- MongoDB will typically start automatically on Windows
- Default connection: `mongodb://localhost:27017`

#### Option B: MongoDB Atlas (Cloud - Recommended for beginners)
1. Create free account at https://www.mongodb.com/atlas
2. Create a cluster
3. Get connection string
4. Update `MONGODB_URI` in `backend/.env` file

## Environment Configuration

### Backend (.env)
```bash
PORT=5000
NODE_ENV=development
MONGODB_URI=mongodb://localhost:27017/college-portal
JWT_SECRET=college-portal-super-secret-jwt-key-for-development-2024
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:5000/api
VITE_ENVIRONMENT=development
```

## Available Scripts

### Backend Scripts
```bash
npm run dev          # Start development server with hot reload
npm run build        # Build for production
npm run start        # Start production server
npm run type-check   # Check TypeScript types
```

### Frontend Scripts
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
- Backend (5000): Change `PORT` in `backend/.env`
- Frontend (5173): It will automatically try the next available port

#### 2. MongoDB Connection Error
- Ensure MongoDB is running
- Check connection string in `backend/.env`
- For Atlas: Whitelist your IP address

#### 3. CORS Errors
- Ensure `FRONTEND_URL` in `backend/.env` matches your frontend URL
- Default should be `http://localhost:5173`

#### 4. Dependencies Issues
```bash
# Reinstall dependencies
cd backend && npm install
cd ../frontend && npm install
```

## Application URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api (when running)

## Features Available

1. **User Authentication**
   - Register new account
   - Login/Logout
   - Protected routes

2. **Multilingual AI Chatbot**
   - Supports English, Hindi, and Rajasthani
   - Context-aware responses
   - RAG (Retrieval Augmented Generation)

3. **Announcements System**
   - View college announcements
   - Admin can create/manage announcements

4. **Responsive Design**
   - Mobile-friendly interface
   - Dark/Light theme support
   - Smooth animations

## Development Notes

- Both servers support hot reload for development
- TypeScript is used for both frontend and backend
- Frontend uses React 18 + Vite + Tailwind CSS
- Backend uses Node.js + Express + MongoDB + TypeScript

## Support

If you encounter any issues:
1. Check that all dependencies are installed
2. Verify MongoDB is running
3. Check environment variables are correctly set
4. Look at the console/terminal for error messages

Happy coding! 🎉