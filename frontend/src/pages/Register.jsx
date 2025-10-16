import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import Alert from "../components/Alert";
import LoadingSpinner from "../components/LoadingSpinner";

export default function Register() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [form, setForm] = useState({
    email: "",
    username: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    role: "student",
    password: "",
    password_confirm: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function update(key, value) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (form.password !== form.password_confirm) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    try {
      console.log("Sending registration data:", form);
      const userData = await register(form);
      console.log("Registration successful:", userData);

      // If registration returns user data with tokens, redirect to appropriate dashboard
      if (userData && userData.user) {
        let redirectPath = "/dashboard";

        if (
          userData.user.role === "organizer" ||
          userData.user.role === "transport_organizer"
        ) {
          redirectPath = "/organizer-dashboard";
        } else {
          redirectPath = "/student-dashboard";
        }

        navigate(redirectPath);
      } else {
        // If registration doesn't return tokens (e.g., requires email verification)
        // Redirect to login page with success message
        navigate("/", {
          state: {
            message:
              "Registration successful! Please log in with your credentials.",
          },
        });
      }
    } catch (err) {
      console.error("Registration error:", err);
      console.error("Error response:", err.response?.data);

      // Handle different error formats
      let errorMessage = "Registration failed. Please try again.";

      if (err.response?.data) {
        const errorData = err.response.data;

        // Handle field-specific errors
        if (typeof errorData === "object") {
          const fieldErrors = [];
          Object.keys(errorData).forEach((field) => {
            if (Array.isArray(errorData[field])) {
              fieldErrors.push(`${field}: ${errorData[field].join(", ")}`);
            } else {
              fieldErrors.push(`${field}: ${errorData[field]}`);
            }
          });

          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join("\n");
          }
        } else if (typeof errorData === "string") {
          errorMessage = errorData;
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.message) {
          errorMessage = errorData.message;
        }
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="bg-white rounded-xl shadow-xl p-8 border border-blue-100">
          <div className="text-center mb-8">
            <div className="mx-auto h-16 w-16 bg-blue-600 rounded-full flex items-center justify-center mb-4">
              <svg
                className="h-8 w-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
                />
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-blue-900">
              Join Our Platform
            </h2>
            <p className="mt-2 text-sm text-blue-600">
              Create your transport account
            </p>
            <p className="mt-1 text-xs text-gray-500">
              Already have an account?{" "}
              <Link
                to="/"
                className="font-medium text-blue-600 hover:text-blue-500 underline"
              >
                Sign in here
              </Link>
            </p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label
                    htmlFor="first_name"
                    className="block text-sm font-medium text-blue-700"
                  >
                    First Name
                  </label>
                  <input
                    id="first_name"
                    name="first_name"
                    type="text"
                    required
                    className="mt-1 appearance-none relative block w-full px-4 py-3 border border-blue-200 placeholder-blue-300 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                    placeholder="First name"
                    value={form.first_name}
                    onChange={(e) => update("first_name", e.target.value)}
                  />
                </div>
                <div>
                  <label
                    htmlFor="last_name"
                    className="block text-sm font-medium text-blue-700"
                  >
                    Last Name
                  </label>
                  <input
                    id="last_name"
                    name="last_name"
                    type="text"
                    required
                    className="mt-1 appearance-none relative block w-full px-4 py-3 border border-blue-200 placeholder-blue-300 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                    placeholder="Last name"
                    value={form.last_name}
                    onChange={(e) => update("last_name", e.target.value)}
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="username"
                  className="block text-sm font-medium text-blue-700"
                >
                  Username
                </label>
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  className="mt-1 appearance-none relative block w-full px-4 py-3 border border-blue-200 placeholder-blue-300 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                  placeholder="Choose a username"
                  value={form.username}
                  onChange={(e) => update("username", e.target.value)}
                />
              </div>

              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-blue-700"
                >
                  Email Address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="mt-1 appearance-none relative block w-full px-4 py-3 border border-blue-200 placeholder-blue-300 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                  placeholder="Enter your email"
                  value={form.email}
                  onChange={(e) => update("email", e.target.value)}
                />
              </div>

              <div>
                <label
                  htmlFor="phone_number"
                  className="block text-sm font-medium text-blue-700"
                >
                  Phone Number
                </label>
                <input
                  id="phone_number"
                  name="phone_number"
                  type="tel"
                  required
                  className="mt-1 appearance-none relative block w-full px-4 py-3 border border-blue-200 placeholder-blue-300 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                  placeholder="Enter your phone number"
                  value={form.phone_number}
                  onChange={(e) => update("phone_number", e.target.value)}
                />
              </div>

              <div>
                <label
                  htmlFor="role"
                  className="block text-sm font-medium text-blue-700"
                >
                  Account Type
                </label>
                <select
                  id="role"
                  name="role"
                  className="mt-1 block w-full px-4 py-3 border border-blue-200 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                  value={form.role}
                  onChange={(e) => update("role", e.target.value)}
                >
                  <option value="student">Student</option>
                  <option value="transport_organizer">
                    Transport Organizer
                  </option>
                </select>
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-blue-700"
                >
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  required
                  className="mt-1 appearance-none relative block w-full px-4 py-3 border border-blue-200 placeholder-blue-300 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                  placeholder="Create a password"
                  value={form.password}
                  onChange={(e) => update("password", e.target.value)}
                />
              </div>

              <div>
                <label
                  htmlFor="password_confirm"
                  className="block text-sm font-medium text-blue-700"
                >
                  Confirm Password
                </label>
                <input
                  id="password_confirm"
                  name="password_confirm"
                  type="password"
                  autoComplete="new-password"
                  required
                  className="mt-1 appearance-none relative block w-full px-4 py-3 border border-blue-200 placeholder-blue-300 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-colors"
                  placeholder="Confirm your password"
                  value={form.password_confirm}
                  onChange={(e) => update("password_confirm", e.target.value)}
                />
              </div>
            </div>

            {error && (
              <Alert
                type="error"
                message={error}
                onClose={() => setError("")}
              />
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-lg hover:shadow-xl"
              >
                {loading ? <LoadingSpinner size="sm" /> : "Create Account"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

