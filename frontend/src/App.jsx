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
      <Layout>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          <Route path="/student-dashboard" element={
            <ProtectedRoute>
              <StudentDashboard />
            </ProtectedRoute>
          } />
          <Route path="/organizer-dashboard" element={
            <ProtectedRoute>
              <OrganizerDashboard />
            </ProtectedRoute>
          } />
          <Route path="/transport" element={<TransportOptions />} />
          <Route path="/register" element={<Register />} />
          <Route path="/book/:id" element={
            <ProtectedRoute>
              <CreateBooking />
            </ProtectedRoute>
          } />
          <Route path="/bookings" element={
            <ProtectedRoute>
              <MyBookings />
            </ProtectedRoute>
          } />
          <Route path="/profile" element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          } />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
