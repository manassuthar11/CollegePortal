# College Portal with Multilingual AI Chatbot

A comprehensive college management system built with TypeScript, featuring a multilingual AI chatbot powered by RAG (Retrieval-Augmented Generation) technology supporting English, Hindi, and Rajasthani languages.

## ✨ Features

### 🤖 **AI-Powered Multilingual Chatbot**
- **RAG Technology**: Advanced retrieval-augmented generation for accurate responses
- **Language Support**: English, Hindi, and Rajasthani with automatic language detection
- **Real-time Chat**: Instant responses with typing indicators and animations
- **Context Awareness**: Maintains conversation context for better user experience

### 📚 **Announcement System**
- Create, edit, and manage announcements
- Category-based organization (Academic, Administrative, Events, Emergency)
- Priority levels (Low, Medium, High, Urgent)
- Target audience filtering (Students, Teachers, Admins)
- Expiry date management and view tracking

### 👥 **User Management**
- Role-based authentication (Student, Teacher, Admin)
- Secure JWT-based authentication
- Profile management with department and year information
- Protected routes and authorization

### 🎨 **Modern UI/UX**
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Advanced Animations**: Smooth transitions using Framer Motion
- **Dark/Light Theme**: Theme switching capability
- **Floating Chatbot**: Always-accessible AI assistant
- **Progressive Enhancement**: Optimized performance and accessibility

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v16 or higher)
- **MongoDB** (local installation or MongoDB Atlas)

### Installation

1. **Clone the repository**
2. **Install dependencies**: `npm install` in both backend and frontend directories
3. **Environment setup**: Create `.env` file in backend directory
4. **Start servers**: Run `start-dev.bat` (Windows) or manually start both servers

### Access Points
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 🏗️ Tech Stack

### Backend: Node.js, Express, MongoDB, JWT, Hugging Face, ChromaDB
### Frontend: React 18, TypeScript, Vite, Tailwind CSS, Framer Motion

## 🎨 Animation Features
Comprehensive animations using Framer Motion for smooth user interactions, page transitions, and real-time chat experiences.

## 🌍 Language Support
- **English**: Primary interface language
- **Hindi (हिंदी)**: Native Devanagari script support  
- **Rajasthani (राजस्थानी)**: Regional language support

---

Built with ❤️ for educational institutions and student communities.

## 🚀 Features

- **Modern UI/UX**: Clean, responsive design built with React + TypeScript + Tailwind CSS
- **Multilingual Support**: Chatbot supports Hindi, English, and Rajasthani
- **RAG Chatbot**: Retrieval-Augmented Generation using Hugging Face models and ChromaDB
- **User Authentication**: Secure JWT-based login/signup system
- **Announcements System**: Admin panel for college updates and notifications
- **Real-time Chat**: Modern bubble-style chat interface with floating widget
- **Vector Search**: Semantic document search using embeddings

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API calls
- **React Hooks** for state management

### Backend
- **Node.js** with Express.js
- **MongoDB** with Mongoose ODM
- **JWT** for authentication
- **bcryptjs** for password hashing
- **CORS** for cross-origin requests

### AI/ML
- **Hugging Face Transformers** (MiniLM embeddings, DistilBERT QA)
- **ChromaDB** for vector storage and similarity search
- **Language Detection** utilities
- **RAG Pipeline** for context-aware responses

## 📁 Project Structure

```
College-portal/
├── frontend/                # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Route-based page components
│   │   ├── types/           # TypeScript type definitions
│   │   ├── utils/           # Utility functions
│   │   ├── App.tsx          # Main app component
│   │   └── index.tsx        # Entry point
│   ├── public/              # Static assets
│   ├── package.json         # Frontend dependencies
│   ├── tailwind.config.js   # Tailwind configuration
│   ├── tsconfig.json        # TypeScript configuration
│   └── .env                 # Environment variables
│
├── backend/                 # Node.js Express backend
│   ├── src/
│   │   ├── controllers/     # Route controllers
│   │   ├── models/          # Mongoose models
│   │   ├── routes/          # API route definitions
│   │   ├── middleware/      # Custom middleware
│   │   ├── utils/           # Utility functions
│   │   ├── config/          # Configuration files
│   │   └── index.js         # Server entry point
│   ├── package.json         # Backend dependencies
│   └── .env                 # Environment variables
│
├── .gitignore              # Git ignore rules
└── README.md              # This file
```

## ⚡ Quick Start

### Prerequisites
- Node.js (v16 or higher)
- MongoDB (local or Atlas)
- npm or yarn package manager

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file in the backend directory:
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/college-portal
JWT_SECRET=your-super-secret-jwt-key
NODE_ENV=development
```

4. Start the backend server:
```bash
npm run dev
```

Backend will be running on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENVIRONMENT=development
```

4. Start the frontend development server:
```bash
npm start
```

Frontend will be running on `http://localhost:3000`

## 🔧 Environment Variables

### Backend (.env)
```env
PORT=5000                                    # Server port
MONGODB_URI=mongodb://localhost:27017/college-portal  # MongoDB connection string
JWT_SECRET=your-super-secret-jwt-key         # JWT signing secret
NODE_ENV=development                         # Environment (development/production)
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api  # Backend API base URL
REACT_APP_ENVIRONMENT=development            # Environment identifier
```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile (protected)

### Chatbot
- `POST /api/chat/message` - Send message to chatbot
- `GET /api/chat/history/:userId` - Get chat history (protected)
- `DELETE /api/chat/history/:userId` - Clear chat history (protected)

### Announcements
- `GET /api/announcements` - Get all announcements
- `POST /api/announcements` - Create announcement (admin only)
- `PUT /api/announcements/:id` - Update announcement (admin only)
- `DELETE /api/announcements/:id` - Delete announcement (admin only)

## 🤖 Chatbot Features

- **Multilingual Support**: Automatic language detection and response in Hindi, English, or Rajasthani
- **RAG Pipeline**: Context-aware responses using document retrieval
- **Semantic Search**: Vector-based similarity search using ChromaDB
- **Conversation Memory**: Maintains chat history for better context
- **Floating Widget**: Minimizable chat interface on all pages

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcryptjs
- CORS protection
- Input validation and sanitization
- Error handling and logging

## 🎨 UI/UX Features

- Responsive design for all screen sizes
- Modern bubble-style chat interface
- Dark/light theme support
- Loading states and animations
- Accessible components with proper ARIA labels

## 🚀 Deployment

### Backend Deployment
1. Set production environment variables
2. Build the application: `npm run build`
3. Deploy to your preferred platform (Heroku, Vercel, etc.)

### Frontend Deployment
1. Set production API URL in `.env`
2. Build the application: `npm run build`
3. Deploy the `build` folder to your hosting service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [MongoDB Documentation](https://docs.mongodb.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Express.js](https://expressjs.com/)
- [Hugging Face](https://huggingface.co/docs)

## 📞 Support

For support, email support@collegeportal.com or create an issue in this repository.

---

**Made with ❤️ for educational institutions**