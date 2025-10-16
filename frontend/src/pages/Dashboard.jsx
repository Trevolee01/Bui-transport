import { useAuth } from '../contexts/AuthContext';
import StudentDashboard from './StudentDashboard';
import OrganizerDashboard from './OrganizerDashboard';
import LoadingSpinner from '../components/LoadingSpinner';

export default function Dashboard() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Route to appropriate dashboard based on user role
  if (user?.role === 'organizer' || user?.role === 'transport_organizer') {
    return <OrganizerDashboard />;
  }

  // Default to student dashboard
  return <StudentDashboard />;
}
