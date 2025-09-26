import React from 'react';

const AnnouncementsPage: React.FC = () => {
  const announcements = [
    {
      id: 1,
      title: "Academic Calendar Released",
      content: "The new academic calendar for 2024-2025 has been published. Please check important dates.",
      author: "Admin",
      date: "2025-09-20",
      category: "Academic"
    },
    {
      id: 2,
      title: "Library Timings Update",
      content: "Library hours have been extended. New timings: 8:00 AM to 10:00 PM on weekdays.",
      author: "Librarian",
      date: "2025-09-18",
      category: "General"
    },
    {
      id: 3,
      title: "Sports Day Registration",
      content: "Registration for annual sports day is now open. Last date for registration: October 5, 2025.",
      author: "Sports Committee",
      date: "2025-09-15",
      category: "Events"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Announcements</h1>
          <p className="text-gray-600 mt-2">Stay updated with the latest college news and updates</p>
        </div>

        <div className="grid gap-6">
          {announcements.map((announcement) => (
            <div key={announcement.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">
                    {announcement.title}
                  </h2>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span>By {announcement.author}</span>
                    <span>•</span>
                    <span>{new Date(announcement.date).toLocaleDateString()}</span>
                    <span>•</span>
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                      {announcement.category}
                    </span>
                  </div>
                </div>
              </div>
              
              <p className="text-gray-700 leading-relaxed">
                {announcement.content}
              </p>
              
              <div className="mt-4 pt-4 border-t border-gray-100">
                <button className="text-blue-600 hover:text-blue-800 font-medium">
                  Read More →
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Add New Announcement Button (for admins) */}
        <div className="mt-8 text-center">
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-200">
            Add New Announcement
          </button>
        </div>
      </div>
    </div>
  );
};

export default AnnouncementsPage;