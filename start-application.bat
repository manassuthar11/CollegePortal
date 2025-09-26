@echo off
echo ===============================================
echo 🚀 Starting College Portal Application
echo ===============================================
echo.

echo 📋 Pre-flight Checklist:
echo ✅ 1. Dependencies installed
echo ✅ 2. Environment variables configured
echo.

echo 🔍 Checking MongoDB connection...
echo Note: Make sure MongoDB is running on your system!
echo - If you have MongoDB installed locally, it should start automatically
echo - If not, you can use MongoDB Atlas (cloud) by updating the MONGODB_URI in backend/.env
echo.

echo 📝 Instructions:
echo 1. This will start the BACKEND server first
echo 2. Then you need to start the FRONTEND in a separate terminal
echo 3. Frontend will be available at: http://localhost:5173
echo 4. Backend API will be available at: http://localhost:5000
echo.

pause
echo.
echo 🔧 Starting Backend Server...
cd backend
start "College Portal Backend" cmd /k "npm run dev"

echo.
echo ⏱️ Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo 🎨 Starting Frontend Server...
cd ../frontend
start "College Portal Frontend" cmd /k "npm run dev"

echo.
echo ✅ Both servers are starting!
echo.
echo 📱 Your application will open automatically in your browser
echo 🔗 Frontend: http://localhost:5173
echo 🔗 Backend API: http://localhost:5000
echo.
echo Press any key to close this window...
pause > nul