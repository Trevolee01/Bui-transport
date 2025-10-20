import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
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
  const [showPassword, setShowPassword] = useState(false);
  const [showPasswordConfirm, setShowPasswordConfirm] = useState(false);

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
    <>
      <style>
        {`
          .register-input::placeholder {
            color: #64748b !important;
            opacity: 1;
          }
          .register-input:focus::placeholder {
            color: #94a3b8 !important;
          }
          .register-select option {
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
        {/* Logo Space - Same as Login */}
        <div style={{ marginBottom: "40px" }}>
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

        <div style={{ width: "100%", maxWidth: "500px" }}>
          {/* Header Text */}
          <div style={{ textAlign: "center", marginBottom: "32px" }}>
            <h2
              style={{
                fontSize: "36px",
                fontWeight: "900",
                color: "white",
                marginBottom: "8px",
              }}
            >
              Join Our Platform
            </h2>
            <p
              style={{
                fontSize: "16px",
                color: "#94a3b8",
                marginBottom: "4px",
              }}
            >
              Create your transport account
            </p>
            <p
              style={{
                fontSize: "14px",
                color: "#64748b",
              }}
            ></p>
          </div>

          <form
            style={{ display: "flex", flexDirection: "column", gap: "16px" }}
            onSubmit={handleSubmit}
          >
            <div
              style={{ display: "flex", flexDirection: "column", gap: "16px" }}
            >
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "16px",
                }}
              >
                <div>
                  <input
                    id="first_name"
                    name="first_name"
                    type="text"
                    required
                    className="w-full px-4 py-4 rounded-md text-base transition-all duration-200 register-input"
                    style={{
                      backgroundColor: "rgba(30, 41, 59, 0.6)",
                      border: "1px solid rgba(71, 85, 105, 0.3)",
                      color: "#cbd5e1",
                    }}
                    placeholder="First name"
                    value={form.first_name}
                    onChange={(e) => update("first_name", e.target.value)}
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
                <div>
                  <input
                    id="last_name"
                    name="last_name"
                    type="text"
                    required
                    className="w-full px-4 py-4 rounded-md text-base transition-all duration-200 register-input"
                    style={{
                      backgroundColor: "rgba(30, 41, 59, 0.6)",
                      border: "1px solid rgba(71, 85, 105, 0.3)",
                      color: "#cbd5e1",
                    }}
                    placeholder="Last name"
                    value={form.last_name}
                    onChange={(e) => update("last_name", e.target.value)}
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
              </div>

              <div>
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  className="w-full px-4 py-4 rounded-md text-base transition-all duration-200 register-input"
                  style={{
                    backgroundColor: "rgba(30, 41, 59, 0.6)",
                    border: "1px solid rgba(71, 85, 105, 0.3)",
                    color: "#cbd5e1",
                  }}
                  placeholder="Choose a username"
                  value={form.username}
                  onChange={(e) => update("username", e.target.value)}
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

              <div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="w-full px-4 py-4 rounded-md text-base transition-all duration-200 register-input"
                  style={{
                    backgroundColor: "rgba(30, 41, 59, 0.6)",
                    border: "1px solid rgba(71, 85, 105, 0.3)",
                    color: "#cbd5e1",
                  }}
                  placeholder="Enter your email"
                  value={form.email}
                  onChange={(e) => update("email", e.target.value)}
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

              <div>
                <input
                  id="phone_number"
                  name="phone_number"
                  type="tel"
                  required
                  className="w-full px-4 py-4 rounded-md text-base transition-all duration-200 register-input"
                  style={{
                    backgroundColor: "rgba(30, 41, 59, 0.6)",
                    border: "1px solid rgba(71, 85, 105, 0.3)",
                    color: "#cbd5e1",
                  }}
                  placeholder="Enter your phone number"
                  value={form.phone_number}
                  onChange={(e) => update("phone_number", e.target.value)}
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
                <select
                  id="role"
                  name="role"
                  className="w-full px-4 py-4 rounded-md text-base appearance-none cursor-pointer transition-all duration-200 register-select"
                  style={{
                    backgroundColor: "rgba(30, 41, 59, 0.6)",
                    border: "1px solid rgba(71, 85, 105, 0.3)",
                    color: "#cbd5e1",
                  }}
                  value={form.role}
                  onChange={(e) => update("role", e.target.value)}
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

              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="new-password"
                  required
                  className="w-full px-4 py-4 pr-12 rounded-md text-base transition-all duration-200 register-input"
                  style={{
                    backgroundColor: "rgba(30, 41, 59, 0.6)",
                    border: "1px solid rgba(71, 85, 105, 0.3)",
                    color: "#cbd5e1",
                  }}
                  placeholder="Create a password"
                  value={form.password}
                  onChange={(e) => update("password", e.target.value)}
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
                <input
                  id="password_confirm"
                  name="password_confirm"
                  type={showPasswordConfirm ? "text" : "password"}
                  autoComplete="new-password"
                  required
                  className="w-full px-4 py-4 pr-12 rounded-md text-base transition-all duration-200 register-input"
                  style={{
                    backgroundColor: "rgba(30, 41, 59, 0.6)",
                    border: "1px solid rgba(71, 85, 105, 0.3)",
                    color: "#cbd5e1",
                  }}
                  placeholder="Confirm your password"
                  value={form.password_confirm}
                  onChange={(e) => update("password_confirm", e.target.value)}
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
                  onClick={() => setShowPasswordConfirm(!showPasswordConfirm)}
                >
                  {showPasswordConfirm ? (
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
                    <span style={{ marginLeft: "8px" }}>
                      Creating Account...
                    </span>
                  </div>
                ) : (
                  "Create Account"
                )}
              </button>
            </div>
          </form>
        </div>
        <div style={{ marginTop: "80px", textAlign: "center" }}>
          Already have an account?{" "}
          <Link
            to="/"
            style={{
              color: "#94a3b8",
              textDecoration: "none",
              transition: "color 0.2s ease",
            }}
            onMouseEnter={(e) => (e.target.style.color = "blue")}
            onMouseLeave={(e) => (e.target.style.color = "#94a3b8")}
          >
            Sign in here
          </Link>
        </div>
      </div>
    </>
  );
}
