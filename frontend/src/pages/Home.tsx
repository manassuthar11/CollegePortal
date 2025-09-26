import React from 'react';
import { motion } from 'framer-motion';

const Home: React.FC = () => {
  const containerVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        staggerChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  };

  const featureVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.5 },
    },
    hover: {
      scale: 1.05,
      transition: { duration: 0.2 },
    },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Hero Section */}
      <motion.section 
        className="relative py-20 px-4"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="max-w-7xl mx-auto text-center">
          <motion.h1 
            className="text-5xl font-bold text-gray-900 mb-6"
            variants={itemVariants}
          >
            Welcome to <span className="text-blue-600">College Portal</span>
          </motion.h1>
          <motion.p 
            className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto"
            variants={itemVariants}
          >
            Your gateway to academic excellence with AI-powered multilingual support
          </motion.p>
          <motion.div 
            className="flex flex-col sm:flex-row gap-4 justify-center"
            variants={itemVariants}
          >
            <motion.button 
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-200"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Get Started
            </motion.button>
            <motion.button 
              className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition duration-200"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Learn More
            </motion.button>
          </motion.div>
        </div>
      </motion.section>

      {/* Features Section */}
      <motion.section 
        className="py-20 px-4 bg-white"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.3 }}
        variants={containerVariants}
      >
        <div className="max-w-7xl mx-auto">
          <motion.h2 
            className="text-3xl font-bold text-center mb-12"
            variants={itemVariants}
          >
            Features
          </motion.h2>
          <motion.div 
            className="grid md:grid-cols-3 gap-8"
            variants={containerVariants}
          >
            <motion.div 
              className="text-center p-6"
              variants={featureVariants}
              whileHover="hover"
            >
              <motion.div 
                className="w-12 h-12 bg-blue-100 rounded-lg mx-auto mb-4 flex items-center justify-center"
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.3 }}
              >
                <span className="text-blue-600 text-xl">🤖</span>
              </motion.div>
              <h3 className="text-xl font-semibold mb-2">AI Chatbot</h3>
              <p className="text-gray-600">Multilingual AI assistant supporting Hindi, English, and Rajasthani</p>
            </motion.div>
            <motion.div 
              className="text-center p-6"
              variants={featureVariants}
              whileHover="hover"
            >
              <motion.div 
                className="w-12 h-12 bg-green-100 rounded-lg mx-auto mb-4 flex items-center justify-center"
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.3 }}
              >
                <span className="text-green-600 text-xl">📚</span>
              </motion.div>
              <h3 className="text-xl font-semibold mb-2">Announcements</h3>
              <p className="text-gray-600">Stay updated with the latest college news and updates</p>
            </motion.div>
            <motion.div 
              className="text-center p-6"
              variants={featureVariants}
              whileHover="hover"
            >
              <motion.div 
                className="w-12 h-12 bg-purple-100 rounded-lg mx-auto mb-4 flex items-center justify-center"
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.3 }}
              >
                <span className="text-purple-600 text-xl">👥</span>
              </motion.div>
              <h3 className="text-xl font-semibold mb-2">User Management</h3>
              <p className="text-gray-600">Secure authentication and profile management</p>
            </motion.div>
          </motion.div>
        </div>
      </motion.section>
    </div>
  );
};

export default Home;