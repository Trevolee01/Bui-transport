import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Layout({ children }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="min-h-screen bg-primary-50">
      <nav className="bg-primary-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex items-center">
                <span className="text-white text-2xl font-bold tracking-wider">
                  BUI TRANSPORT
                </span>
              </div>
            </div>

            <div className="hidden md:flex items-center space-x-8">
              {user ? (
                <>
                  <Link
                    to="/dashboard"
                    className={`px-3 py-2 rounded-md text-base font-medium transition-all duration-200 ${
                      isActive("/dashboard")
                        ? "bg-white text-primary-600"
                        : "text-primary-100 hover:text-white hover:bg-primary-500"
                    }`}
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/transport"
                    className={`px-3 py-2 rounded-md text-base font-medium transition-all duration-200 ${
                      isActive("/transport")
                        ? "bg-white text-primary-600"
                        : "text-primary-100 hover:text-white hover:bg-primary-500"
                    }`}
                  >
                    Transport Options
                  </Link>
                  <Link
                    to="/bookings"
                    className={`px-3 py-2 rounded-md text-base font-medium transition-all duration-200 ${
                      isActive("/bookings")
                        ? "bg-white text-primary-600"
                        : "text-primary-100 hover:text-white hover:bg-primary-500"
                    }`}
                  >
                    My Bookings
                  </Link>
                  <Link
                    to="/profile"
                    className={`px-3 py-2 rounded-md text-base font-medium transition-all duration-200 ${
                      isActive("/profile")
                        ? "bg-white text-primary-600"
                        : "text-primary-100 hover:text-white hover:bg-primary-500"
                    }`}
                  >
                    Profile
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 rounded-md text-base font-medium border-none cursor-pointer transition-all duration-200 bg-red-500 text-white hover:bg-red-600"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <></>
              )}
            </div>

            <div className="md:hidden flex items-center">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="bg-transparent border-none cursor-pointer text-primary-100 p-1 hover:text-white transition-colors duration-200"
              >
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="bg-primary-700 px-4 pt-2 pb-3 space-y-1">
                {user ? (
                  <>
                    <Link
                      to="/dashboard"
                      className="block px-3 py-2 text-base font-medium rounded-md text-primary-100 hover:text-white hover:bg-primary-600 transition-all duration-200"
                    >
                      Dashboard
                    </Link>
                    <Link
                      to="/transport"
                      className="block px-3 py-2 text-base font-medium rounded-md text-primary-100 hover:text-white hover:bg-primary-600 transition-all duration-200"
                    >
                      Transport Options
                    </Link>
                    <Link
                      to="/bookings"
                      className="block px-3 py-2 text-base font-medium rounded-md text-primary-100 hover:text-white hover:bg-primary-600 transition-all duration-200"
                    >
                      My Bookings
                    </Link>
                    <Link
                      to="/profile"
                      className="block px-3 py-2 text-base font-medium rounded-md text-primary-100 hover:text-white hover:bg-primary-600 transition-all duration-200"
                    >
                      Profile
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-3 py-2 text-base font-medium rounded-md border-none bg-transparent cursor-pointer text-red-300 hover:text-red-100 hover:bg-red-600 transition-all duration-200"
                    >
                      Logout
                    </button>
                  </>
                ) : (
                  <>
                    <Link
                      to="/transport"
                      className="block px-3 py-2 text-base font-medium rounded-md text-primary-100 hover:text-white hover:bg-primary-600 transition-all duration-200"
                    >
                      Browse Transport
                    </Link>
                    <Link
                      to="/register"
                      className="block px-3 py-2 text-base font-medium rounded-md text-primary-100 hover:text-white hover:bg-primary-600 transition-all duration-200"
                    >
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
      <main className="max-w-7xl mx-auto py-6 px-4">
        {children}
      </main>
    </div>
  );
}
