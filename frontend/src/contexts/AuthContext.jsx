import { createContext, useContext, useState, useEffect } from "react";
import api from "../apiClient";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      try {
        const response = await api.get("/auth/user/");
        setUser(response.data);
      } catch (error) {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
      }
    }
    setLoading(false);
  };

  const login = async (email, password) => {
    console.log("AuthContext: Attempting login for:", email);
    console.log("AuthContext: API base URL:", api.defaults.baseURL);
    
    try {
      const response = await api.post("/auth/login/", { email, password });
      console.log("AuthContext: Login response:", response.data);
      const { tokens, user: userData } = response.data;

      localStorage.setItem("accessToken", tokens.access);
      localStorage.setItem("refreshToken", tokens.refresh);
      setUser(userData);

      return response.data;
    } catch (error) {
      console.error("AuthContext: Login error:", error);
      console.error("AuthContext: Error response:", error.response?.data);
      console.error("AuthContext: Error status:", error.response?.status);
      console.error("AuthContext: Error config:", error.config);
      throw error;
    }
  };

  const register = async (userData) => {
    console.log("AuthContext: Sending registration request with data:", userData);
    console.log("AuthContext: API base URL:", api.defaults.baseURL);
    
    try {
      const response = await api.post("/auth/register/", userData);
      console.log("AuthContext: Registration response:", response.data);
      const { tokens, user: newUser } = response.data;

      localStorage.setItem("accessToken", tokens.access);
      localStorage.setItem("refreshToken", tokens.refresh);
      setUser(newUser);

      return response.data;
    } catch (error) {
      console.error("AuthContext: Registration error:", error);
      console.error("AuthContext: Error response:", error.response?.data);
      console.error("AuthContext: Error status:", error.response?.status);
      console.error("AuthContext: Error config:", error.config);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
