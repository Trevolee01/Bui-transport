import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../apiClient';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';

export default function MyBookings() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const res = await api.get('/bookings/my-bookings/');
      setBookings(res.data.results || res.data);
    } catch (err) {
      setError('Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId) => {
    if (!confirm('Are you sure you want to cancel this booking?')) return;

    try {
      await api.patch(`/bookings/${bookingId}/cancel/`);
      fetchBookings(); // Refresh the list
    } catch (err) {
      setError('Failed to cancel booking');
    }
  };

  const filteredBookings = bookings.filter(booking => {
    if (filter === 'all') return true;
    return booking.booking_status === filter;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">My Bookings</h1>
          <Link
            to="/"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
          >
            Book New Trip
          </Link>
        </div>

        {/* Filter Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            {[
              { key: 'all', label: 'All Bookings' },
              { key: 'pending', label: 'Pending' },
              { key: 'confirmed', label: 'Confirmed' },
              { key: 'completed', label: 'Completed' },
              { key: 'cancelled', label: 'Cancelled' }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setFilter(tab.key)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  filter === tab.key
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {error && (
          <Alert type="error" message={error} onClose={() => setError('')} />
        )}

        {/* Bookings List */}
        {filteredBookings.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No bookings found</h3>
            <p className="mt-1 text-sm text-gray-500">
              {filter === 'all' ? 'You haven\'t made any bookings yet.' : `No ${filter} bookings found.`}
            </p>
            {filter === 'all' && (
              <div className="mt-6">
                <Link
                  to="/"
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  Book Your First Trip
                </Link>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {filteredBookings.map((booking) => (
              <div key={booking.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {booking.transport_option?.route_name}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {booking.transport_option?.departure_location} → {booking.transport_option?.destination}
                    </p>
                  </div>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(booking.booking_status)}`}>
                    {booking.booking_status.charAt(0).toUpperCase() + booking.booking_status.slice(1)}
                  </span>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-gray-500">Booking Date</p>
                    <p className="font-medium">{new Date(booking.booking_date).toLocaleDateString()}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Seats</p>
                    <p className="font-medium">{booking.seats_booked}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Total Amount</p>
                    <p className="font-medium">₦{booking.total_amount}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Payment Status</p>
                    <p className={`font-medium ${booking.payment_status === 'paid' ? 'text-green-600' : 'text-yellow-600'}`}>
                      {booking.payment_status.charAt(0).toUpperCase() + booking.payment_status.slice(1)}
                    </p>
                  </div>
                </div>

                {booking.special_requests && (
                  <div className="mb-4">
                    <p className="text-sm text-gray-500">Special Requests</p>
                    <p className="text-sm text-gray-700">{booking.special_requests}</p>
                  </div>
                )}

                <div className="flex justify-between items-center">
                  <p className="text-sm text-gray-500">
                    Booked on {new Date(booking.created_at).toLocaleDateString()}
                  </p>
                  <div className="flex space-x-2">
                    {booking.booking_status === 'pending' && (
                      <button
                        onClick={() => handleCancelBooking(booking.id)}
                        className="px-3 py-1 text-sm text-red-600 hover:text-red-700 border border-red-300 rounded hover:bg-red-50"
                      >
                        Cancel
                      </button>
                    )}
                    {booking.booking_status === 'completed' && !booking.review && (
                      <button className="px-3 py-1 text-sm text-primary-600 hover:text-primary-700 border border-primary-300 rounded hover:bg-primary-50">
                        Leave Review
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}