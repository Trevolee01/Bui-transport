import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../apiClient';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';

export default function CreateBooking() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [transportOption, setTransportOption] = useState(null);
  const [seats, setSeats] = useState(1);
  const [paymentMethod, setPaymentMethod] = useState('wallet');
  const [specialRequests, setSpecialRequests] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchTransportOption();
  }, [id]);

  const fetchTransportOption = async () => {
    try {
      const res = await api.get(`/transport/options/${id}/`);
      setTransportOption(res.data);
    } catch (err) {
      setError('Failed to load transport option');
    } finally {
      setLoading(false);
    }
  };

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      await api.post('/bookings/create/', {
        transport_option: id,
        seats_booked: Number(seats),
        payment_method: paymentMethod,
        special_requests: specialRequests,
      });
      navigate('/bookings');
    } catch (err) {
      setError(err.response?.data?.detail || 'Booking failed');
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!transportOption) {
    return (
      <div className="text-center py-12">
        <Alert type="error" message="Transport option not found" />
      </div>
    );
  }

  const totalAmount = transportOption.price * seats;
  const platformFee = totalAmount * 0.02; // 2% platform fee
  const finalAmount = totalAmount + platformFee;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 bg-primary-600">
          <h1 className="text-2xl font-bold text-white">Complete Your Booking</h1>
        </div>

        <div className="p-6">
          {/* Transport Details */}
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Trip Details</h2>
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Route:</span>
                <span className="font-medium">{transportOption.route_name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">From:</span>
                <span className="font-medium">{transportOption.departure_location}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">To:</span>
                <span className="font-medium">{transportOption.destination}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Departure Time:</span>
                <span className="font-medium">{transportOption.departure_time}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Available Seats:</span>
                <span className="font-medium">{transportOption.available_seats}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Price per Seat:</span>
                <span className="font-medium">₦{transportOption.price}</span>
              </div>
            </div>
          </div>

          {/* Booking Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="seats" className="block text-sm font-medium text-gray-700 mb-2">
                Number of Seats
              </label>
              <select
                id="seats"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                value={seats}
                onChange={(e) => setSeats(Number(e.target.value))}
              >
                {[...Array(Math.min(transportOption.available_seats, 5))].map((_, i) => (
                  <option key={i + 1} value={i + 1}>
                    {i + 1} seat{i > 0 ? 's' : ''}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="paymentMethod" className="block text-sm font-medium text-gray-700 mb-2">
                Payment Method
              </label>
              <select
                id="paymentMethod"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                value={paymentMethod}
                onChange={(e) => setPaymentMethod(e.target.value)}
              >
                <option value="wallet">Wallet</option>
                <option value="mobile_money">Mobile Money</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="card">Card</option>
              </select>
            </div>

            <div>
              <label htmlFor="specialRequests" className="block text-sm font-medium text-gray-700 mb-2">
                Special Requests (Optional)
              </label>
              <textarea
                id="specialRequests"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="Any special requirements or requests..."
                value={specialRequests}
                onChange={(e) => setSpecialRequests(e.target.value)}
              />
            </div>

            {/* Price Breakdown */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Price Breakdown</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Seats ({seats}x):</span>
                  <span>₦{totalAmount.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Platform Fee (2%):</span>
                  <span>₦{platformFee.toFixed(2)}</span>
                </div>
                <div className="border-t pt-2 flex justify-between font-semibold text-lg">
                  <span>Total:</span>
                  <span>₦{finalAmount.toFixed(2)}</span>
                </div>
              </div>
            </div>

            {error && (
              <Alert type="error" message={error} onClose={() => setError('')} />
            )}

            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="flex-1 px-4 py-2 border border-transparent rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? <LoadingSpinner size="sm" /> : 'Confirm Booking'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

