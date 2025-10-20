import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';
import TransportOptions from './pages/TransportOptions.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import CreateBooking from './pages/CreateBooking.jsx';
import MyBookings from './pages/MyBookings.jsx';
import Profile from './pages/Profile.jsx';
import Dashboard from './pages/Dashboard.jsx';
import StudentDashboard from './pages/StudentDashboard.jsx';
import OrganizerDashboard from './pages/OrganizerDashboard.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Auth routes without layout */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Protected routes with layout */}
        <Route path="/dashboard" element={
          <Layout>
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          </Layout>
        } />
        <Route path="/student-dashboard" element={
          <Layout>
            <ProtectedRoute>
              <StudentDashboard />
            </ProtectedRoute>
          </Layout>
        } />
        <Route path="/organizer-dashboard" element={
          <Layout>
            <ProtectedRoute>
              <OrganizerDashboard />
            </ProtectedRoute>
          </Layout>
        } />
        <Route path="/transport" element={
          <Layout>
            <TransportOptions />
          </Layout>
        } />
        <Route path="/book/:id" element={
          <Layout>
            <ProtectedRoute>
              <CreateBooking />
            </ProtectedRoute>
          </Layout>
        } />
        <Route path="/bookings" element={
          <Layout>
            <ProtectedRoute>
              <MyBookings />
            </ProtectedRoute>
          </Layout>
        } />
        <Route path="/profile" element={
          <Layout>
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          </Layout>
        } />
      </Routes>
    </BrowserRouter>
  );
}
