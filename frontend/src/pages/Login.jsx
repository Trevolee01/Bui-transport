import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import LoadingSpinner from "../components/LoadingSpinner";
import ApiTest from "../components/ApiTest";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [dashboardChoice, setDashboardChoice] = useState("auto");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const userData = await login(email, password);

      let redirectPath = "/dashboard";

      if (dashboardChoice === "student") {
        redirectPath = "/student-dashboard";
      } else if (dashboardChoice === "transport_organizer") {
        redirectPath = "/organizer-dashboard";
      } else {
        if (
          userData.user?.role === "organizer" ||
          userData.user?.role === "transport_organizer"
        ) {
          redirectPath = "/organizer-dashboard";
        } else {
          redirectPath = "/student-dashboard";
        }
      }

      navigate(redirectPath);
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  // Show API test component if in development and there's a specific query parameter
  if (import.meta.env.DEV && new URLSearchParams(window.location.search).get('debug') === 'api') {
    return <ApiTest />;
  }

  return (
    <>
      <style>
        {`
          .login-input::placeholder {
            color: #64748b !important;
            opacity: 1;
          }
          .login-input:focus::placeholder {
            color: #94a3b8 !important;
          }
          .login-select option {
            background-color: #1e293b !important;
            color: #cbd5e1 !important;
          }
        `}
      </style>
      <div
        className="min-h-screen flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8"
        style={{
          background: "linear-gradient(to bottom, #334155, #1e293b, #0f172a)",
        }}
      >
        {/* Logo Space - Reserved for future logo */}
        <div style={{ marginBottom: "80px" }}>
          <div
            style={{
              width: "160px",
              height: "96px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                color: "white",
                fontSize: "48px",
                fontWeight: "900",
                letterSpacing: "0.1em",
              }}
            >
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                <div
                  style={{
                    fontSize: "50px",
                    fontWeight: "900",
                    lineHeight: "1",
                  }}
                >
                  BUI
                </div>
                <div
                  style={{
                    fontSize: "30px",
                    fontWeight: "600",
                    marginTop: "-8px",
                    lineHeight: "1",
                  }}
                >
                  Transport
                </div>
              </div>
            </div>
          </div>
        </div>

        <div style={{ width: "100%", maxWidth: "384px" }}>
          <form
            style={{ display: "flex", flexDirection: "column", gap: "16px" }}
            onSubmit={handleSubmit}
          >
            <div>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="w-full px-4 py-4 rounded-md text-base transition-all duration-200 login-input"
                style={{
                  backgroundColor: "rgba(30, 41, 59, 0.6)",
                  border: "1px solid rgba(71, 85, 105, 0.3)",
                  color: "#cbd5e1",
                }}
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onFocus={(e) => {
                  e.target.style.borderColor = "#64748b";
                  e.target.style.outline = "1px solid #64748b";
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = "rgba(71, 85, 105, 0.3)";
                  e.target.style.outline = "none";
                }}
              />
            </div>

            <div className="relative">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                autoComplete="current-password"
                required
                className="w-full px-4 py-4 pr-12 rounded-md text-base transition-all duration-200 login-input"
                style={{
                  backgroundColor: "rgba(30, 41, 59, 0.6)",
                  border: "1px solid rgba(71, 85, 105, 0.3)",
                  color: "#cbd5e1",
                }}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onFocus={(e) => {
                  e.target.style.borderColor = "#64748b";
                  e.target.style.outline = "1px solid #64748b";
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = "rgba(71, 85, 105, 0.3)";
                  e.target.style.outline = "none";
                }}
              />

              <div
                className="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  // Eye slash icon (password visible)
                  <svg
                    className="h-5 w-5"
                    style={{ color: "#64748b" }}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    onMouseEnter={(e) => (e.target.style.color = "#94a3b8")}
                    onMouseLeave={(e) => (e.target.style.color = "#64748b")}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"
                    />
                  </svg>
                ) : (
                  // Eye icon (password hidden)
                  <svg
                    className="h-5 w-5"
                    style={{ color: "#64748b" }}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    onMouseEnter={(e) => (e.target.style.color = "#94a3b8")}
                    onMouseLeave={(e) => (e.target.style.color = "#64748b")}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                  </svg>
                )}
              </div>
            </div>

            <div className="relative">
              <select
                id="dashboardChoice"
                name="dashboardChoice"
                className="w-full px-4 py-4 rounded-md text-base appearance-none cursor-pointer transition-all duration-200 login-select"
                style={{
                  backgroundColor: "rgba(30, 41, 59, 0.6)",
                  border: "1px solid rgba(71, 85, 105, 0.3)",
                  color: "#cbd5e1",
                }}
                value={dashboardChoice}
                onChange={(e) => setDashboardChoice(e.target.value)}
                onFocus={(e) => {
                  e.target.style.borderColor = "#64748b";
                  e.target.style.outline = "1px solid #64748b";
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = "rgba(71, 85, 105, 0.3)";
                  e.target.style.outline = "none";
                }}
              >
                <option
                  value="student"
                  style={{ backgroundColor: "#1e293b", color: "#cbd5e1" }}
                >
                  Student
                </option>
                <option
                  value="transport_organizer"
                  style={{ backgroundColor: "#1e293b", color: "#cbd5e1" }}
                >
                  Transport Organizer
                </option>
              </select>

              <div
                style={{
                  position: "absolute",
                  right: "12px",
                  top: "50%",
                  transform: "translateY(-50%)",
                  pointerEvents: "none",
                }}
              >
                <svg
                  style={{ height: "16px", width: "16px", color: "#64748b" }}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </div>
            </div>

            {error && (
              <div
                style={{
                  borderRadius: "6px",
                  padding: "12px",
                  backdropFilter: "blur(4px)",
                  backgroundColor: "rgba(127, 29, 29, 0.3)",
                  border: "1px solid rgba(185, 28, 28, 0.5)",
                }}
              >
                <p
                  style={{
                    color: "#fca5a5",
                    fontSize: "14px",
                    textAlign: "center",
                    margin: 0,
                  }}
                >
                  {error}
                </p>
              </div>
            )}

            <div style={{ paddingTop: "16px" }}>
              <button
                type="submit"
                disabled={loading}
                style={{
                  width: "100%",
                  padding: "16px",
                  color: "white",
                  fontWeight: "600",
                  borderRadius: "6px",
                  border: "none",
                  fontSize: "18px",
                  cursor: loading ? "not-allowed" : "pointer",
                  opacity: loading ? 0.5 : 1,
                  transition: "all 0.2s ease",
                  boxShadow:
                    "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
                  background: "linear-gradient(to right, #ea580c, #dc2626)",
                }}
                onMouseEnter={(e) => {
                  if (!loading) {
                    e.target.style.background =
                      "linear-gradient(to right, #dc2626, #b91c1c)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (!loading) {
                    e.target.style.background =
                      "linear-gradient(to right, #ea580c, #dc2626)";
                  }
                }}
              >
                {loading ? (
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <LoadingSpinner size="sm" />
                    <span style={{ marginLeft: "8px" }}>Signing in...</span>
                  </div>
                ) : (
                  "Login"
                )}
              </button>
            </div>
          </form>

          <div style={{ marginTop: "32px", textAlign: "center" }}>
            <Link
              to="/forgot-password"
              style={{
                color: "#94a3b8",
                fontSize: "16px",
                textDecoration: "none",
                transition: "color 0.2s ease",
              }}
              onMouseEnter={(e) => (e.target.style.color = "blue")}
              onMouseLeave={(e) => (e.target.style.color = "white")}
            >
              Forgot Password
            </Link>
          </div>

          <div style={{ marginTop: "80px", textAlign: "center" }}>
            <Link
              to="/register"
              style={{
                color: "#94a3b8",
                fontSize: "16px",
                textDecoration: "none",
                transition: "color 0.2s ease",
              }}
              onMouseEnter={(e) => (e.target.style.color = "blue")}
              onMouseLeave={(e) => (e.target.style.color = "#94a3b8")}
            >
              Create an Account
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
