@echo off
title JECRC RAG System - Setup and Launch
color 0A

echo.
echo ================================================================
echo 🤖 JECRC Foundation - Smart RAG Chatbot Setup
echo ================================================================
echo.

echo 📋 Pre-Setup Checklist:
echo ✅ Python 3.8+ installed
echo ✅ Internet connection for downloading AI models
echo ✅ At least 8GB RAM recommended
echo ✅ 2GB free disk space
echo.

echo 🚀 Starting setup process...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

echo.
echo 📦 Installing required packages...
echo This may take a few minutes for first-time setup...
echo.

REM Install requirements
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Package installation failed
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✅ All packages installed successfully!
echo.

echo 📁 Document folder structure ready at:
echo    📂 documents\admissions\    - Place admission-related documents here
echo    📂 documents\courses\       - Place course and curriculum documents here  
echo    📂 documents\fees\          - Place fee structure and payment info here
echo    📂 documents\general\       - Place general college information here
echo    📂 documents\hostel\        - Place hostel and accommodation info here
echo    📂 documents\placement\     - Place placement and career info here
echo    📂 documents\forms\         - Place forms and applications here
echo.

echo 🎯 NEXT STEPS:
echo 1. Add your documents (PDF, DOCX, TXT) to appropriate folders above
echo 2. Run the system using: python smart_rag_app.py
echo 3. Access web interface at: http://localhost:8000
echo.

echo 📖 For detailed instructions, see: DOCUMENT_UPLOAD_GUIDE.md
echo.

echo ⚡ Ready to launch the RAG system now? (Y/N)
set /p choice="Enter your choice: "

if /i "%choice%"=="Y" (
    echo.
    echo 🚀 Launching JECRC Smart RAG Chatbot...
    echo.
    echo 🌐 Web interface will be available at: http://localhost:8000
    echo 📡 API endpoints will be available at: http://localhost:8000
    echo.
    echo Press Ctrl+C to stop the server when done.
    echo.
    python smart_rag_app.py
) else (
    echo.
    echo ✅ Setup complete! 
    echo To start the system later, run: python smart_rag_app.py
    echo.
    pause
)

echo.
echo Thanks for using JECRC Smart RAG Chatbot! 🎓
pause