import { useState, useEffect } from 'react';
import api from '../apiClient';
import LoadingSpinner from '../components/LoadingSpinner';
import Alert from '../components/Alert';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const [userRes, profileRes] = await Promise.all([
        api.get('/auth/user/'),
        api.get('/users/profile/')
      ]);
      setUser(userRes.data);
      setProfile(profileRes.data);
    } catch (err) {
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await api.patch('/users/profile/', profile);
      setSuccess('Profile updated successfully');
    } catch (err) {
      setError('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleInputChange = (field, value) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 bg-primary-600">
          <h1 className="text-2xl font-bold text-white">My Profile</h1>
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex">
            {[
              { key: 'profile', label: 'Profile Information' },
              { key: 'security', label: 'Security' },
              { key: 'preferences', label: 'Preferences' }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`py-4 px-6 border-b-2 font-medium text-sm ${
                  activeTab === tab.key
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {error && (
            <Alert type="error" message={error} onClose={() => setError('')} />
          )}
          {success && (
            <Alert type="success" message={success} onClose={() => setSuccess('')} />
          )}

          {/* Profile Information Tab */}
          {activeTab === 'profile' && (
            <form onSubmit={handleUpdateProfile} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-2">
                    First Name
                  </label>
                  <input
                    id="first_name"
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    value={user?.first_name || ''}
                    onChange={(e) => setUser(prev => ({ ...prev, first_name: e.target.value }))}
                  />
                </div>
                <div>
                  <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-2">
                    Last Name
                  </label>
                  <input
                    id="last_name"
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    value={user?.last_name || ''}
                    onChange={(e) => setUser(prev => ({ ...prev, last_name: e.target.value }))}
                  />
                </div>
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
                  value={user?.email || ''}
                  disabled
                />
                <p className="mt-1 text-sm text-gray-500">Email cannot be changed</p>
              </div>

              <div>
                <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number
                </label>
                <input
                  id="phone_number"
                  type="tel"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                  value={user?.phone_number || ''}
                  onChange={(e) => setUser(prev => ({ ...prev, phone_number: e.target.value }))}
                />
              </div>

              {user?.role === 'student' && profile && (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label htmlFor="student_id" className="block text-sm font-medium text-gray-700 mb-2">
                        Student ID
                      </label>
                      <input
                        id="student_id"
                        type="text"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                        value={profile.student_id || ''}
                        onChange={(e) => handleInputChange('student_id', e.target.value)}
                      />
                    </div>
                    <div>
                      <label htmlFor="department" className="block text-sm font-medium text-gray-700 mb-2">
                        Department
                      </label>
                      <input
                        id="department"
                        type="text"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                        value={profile.department || ''}
                        onChange={(e) => handleInputChange('department', e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                      <label htmlFor="level" className="block text-sm font-medium text-gray-700 mb-2">
                        Level
                      </label>
                      <select
                        id="level"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                        value={profile.level || ''}
                        onChange={(e) => handleInputChange('level', e.target.value)}
                      >
                        <option value="">Select Level</option>
                        <option value="100">100 Level</option>
                        <option value="200">200 Level</option>
                        <option value="300">300 Level</option>
                        <option value="400">400 Level</option>
                        <option value="500">500 Level</option>
                      </select>
                    </div>
                    <div>
                      <label htmlFor="hostel_name" className="block text-sm font-medium text-gray-700 mb-2">
                        Hostel Name
                      </label>
                      <input
                        id="hostel_name"
                        type="text"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                        value={profile.hostel_name || ''}
                        onChange={(e) => handleInputChange('hostel_name', e.target.value)}
                      />
                    </div>
                    <div>
                      <label htmlFor="room_number" className="block text-sm font-medium text-gray-700 mb-2">
                        Room Number
                      </label>
                      <input
                        id="room_number"
                        type="text"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                        value={profile.room_number || ''}
                        onChange={(e) => handleInputChange('room_number', e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label htmlFor="emergency_contact_name" className="block text-sm font-medium text-gray-700 mb-2">
                        Emergency Contact Name
                      </label>
                      <input
                        id="emergency_contact_name"
                        type="text"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                        value={profile.emergency_contact_name || ''}
                        onChange={(e) => handleInputChange('emergency_contact_name', e.target.value)}
                      />
                    </div>
                    <div>
                      <label htmlFor="emergency_contact_phone" className="block text-sm font-medium text-gray-700 mb-2">
                        Emergency Contact Phone
                      </label>
                      <input
                        id="emergency_contact_phone"
                        type="tel"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                        value={profile.emergency_contact_phone || ''}
                        onChange={(e) => handleInputChange('emergency_contact_phone', e.target.value)}
                      />
                    </div>
                  </div>
                </>
              )}

              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={saving}
                  className="px-6 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {saving ? <LoadingSpinner size="sm" /> : 'Save Changes'}
                </button>
              </div>
            </form>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Change Password</h3>
                <form className="space-y-4">
                  <div>
                    <label htmlFor="current_password" className="block text-sm font-medium text-gray-700 mb-2">
                      Current Password
                    </label>
                    <input
                      id="current_password"
                      type="password"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label htmlFor="new_password" className="block text-sm font-medium text-gray-700 mb-2">
                      New Password
                    </label>
                    <input
                      id="new_password"
                      type="password"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700 mb-2">
                      Confirm New Password
                    </label>
                    <input
                      id="confirm_password"
                      type="password"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                  <button
                    type="submit"
                    className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                  >
                    Update Password
                  </button>
                </form>
              </div>
            </div>
          )}

          {/* Preferences Tab */}
          {activeTab === 'preferences' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Notification Preferences</h3>
                <div className="space-y-4">
                  <div className="flex items-center">
                    <input
                      id="email_notifications"
                      type="checkbox"
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <label htmlFor="email_notifications" className="ml-2 block text-sm text-gray-900">
                      Email notifications for booking updates
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input
                      id="sms_notifications"
                      type="checkbox"
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <label htmlFor="sms_notifications" className="ml-2 block text-sm text-gray-900">
                      SMS notifications for trip updates
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input
                      id="marketing_emails"
                      type="checkbox"
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    />
                    <label htmlFor="marketing_emails" className="ml-2 block text-sm text-gray-900">
                      Marketing emails and promotions
                    </label>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}