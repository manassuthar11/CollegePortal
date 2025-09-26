import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          {/* College Info */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">CP</span>
              </div>
              <span className="text-xl font-bold">College Portal</span>
            </div>
            <p className="text-gray-400 leading-relaxed">
              Your gateway to academic excellence with AI-powered multilingual support
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-gray-400">
              <li><a href="/" className="hover:text-white transition duration-200">Home</a></li>
              <li><a href="/announcements" className="hover:text-white transition duration-200">Announcements</a></li>
              <li><a href="/chatbot" className="hover:text-white transition duration-200">AI Assistant</a></li>
              <li><a href="/profile" className="hover:text-white transition duration-200">Profile</a></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition duration-200">Help Center</a></li>
              <li><a href="#" className="hover:text-white transition duration-200">Contact Us</a></li>
              <li><a href="#" className="hover:text-white transition duration-200">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-white transition duration-200">Terms of Service</a></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact Info</h3>
            <div className="space-y-2 text-gray-400">
              <p>📧 info@collegeportal.edu</p>
              <p>📞 +1 (555) 123-4567</p>
              <p>📍 College Campus, City, State</p>
              <div className="flex space-x-4 mt-4">
                <a href="#" className="text-gray-400 hover:text-white transition duration-200">
                  📘 Facebook
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition duration-200">
                  🐦 Twitter
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition duration-200">
                  💼 LinkedIn
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 College Portal. All rights reserved. Built with ❤️ for students.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;