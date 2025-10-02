import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function Layout({ children }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout, loading } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link to="/" className="flex-shrink-0 flex items-center">
                <span className="text-2xl font-bold text-primary-600">BUI Transport</span>
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              {user ? (
                <>
                  <Link
                    to="/"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/') ? 'text-primary-600 bg-primary-50' : 'text-gray-700 hover:text-primary-600'
                    }`}
                  >
                    Transport Options
                  </Link>
                  <Link
                    to="/bookings"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/bookings') ? 'text-primary-600 bg-primary-50' : 'text-gray-700 hover:text-primary-600'
                    }`}
                  >
                    My Bookings
                  </Link>
                  <Link
                    to="/profile"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/profile') ? 'text-primary-600 bg-primary-50' : 'text-gray-700 hover:text-primary-600'
                    }`}
                  >
                    Profile
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                  >
                    Register
                  </Link>
                </>
              )}
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-gray-700 hover:text-primary-600 focus:outline-none focus:text-primary-600"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                {user ? (
                  <>
                    <Link to="/" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600">
                      Transport Options
                    </Link>
                    <Link to="/bookings" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600">
                      My Bookings
                    </Link>
                    <Link to="/profile" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600">
                      Profile
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-3 py-2 text-base font-medium text-red-600 hover:text-red-700"
                    >
                      Logout
                    </button>
                  </>
                ) : (
                  <>
                    <Link to="/login" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600">
                      Login
                    </Link>
                    <Link to="/register" className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600">
                      Register
                    </Link>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}