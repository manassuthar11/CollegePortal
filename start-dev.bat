@echo off
REM College Portal Quick Start Script for Windows
echo 🚀 Starting College Portal Development Environment

REM Start backend
echo 📡 Starting Backend Server...
cd backend
start "Backend Server" cmd /k "npm run dev"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start frontend  
echo 🎨 Starting Frontend Development Server...
cd ../frontend
start "Frontend Server" cmd /k "npm run dev"

echo ✅ Both servers are starting up!
echo 📡 Backend: http://localhost:5000
echo 🎨 Frontend: http://localhost:5173
echo.
echo Press any key to exit...
pause >nul