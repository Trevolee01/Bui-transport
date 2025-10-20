import { useState } from 'react';
import api from '../apiClient';

export default function ApiTest() {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const testConnection = async () => {
    setLoading(true);
    setResult('Testing connection...');
    
    try {
      // Test basic connection
      const response = await fetch('http://127.0.0.1:8000/api/auth/register/', {
        method: 'OPTIONS',
      });
      
      setResult(`✅ Server is reachable. Status: ${response.status}`);
    } catch (error) {
      setResult(`❌ Connection failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const testRegistration = async () => {
    setLoading(true);
    setResult('Testing registration...');
    
    const testData = {
      email: `test${Date.now()}@example.com`,
      username: `testuser${Date.now()}`,
      first_name: 'Test',
      last_name: 'User',
      phone_number: '1234567890',
      role: 'student',
      password: 'testpassword123',
      password_confirm: 'testpassword123'
    };

    try {
      console.log('Sending test registration:', testData);
      const response = await api.post('/auth/register/', testData);
      setResult(`✅ Registration successful: ${JSON.stringify(response.data, null, 2)}`);
    } catch (error) {
      console.error('Registration test error:', error);
      setResult(`❌ Registration failed: ${error.response?.data ? JSON.stringify(error.response.data, null, 2) : error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">API Debug Test</h2>
      
      <div className="space-y-4">
        <button
          onClick={testConnection}
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          Test Server Connection
        </button>
        
        <button
          onClick={testRegistration}
          disabled={loading}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
        >
          Test Registration
        </button>
      </div>
      
      {result && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h3 className="font-semibold mb-2">Result:</h3>
          <pre className="whitespace-pre-wrap text-sm">{result}</pre>
        </div>
      )}
      
      <div className="mt-4 p-4 bg-blue-50 rounded">
        <h3 className="font-semibold mb-2">Current API Config:</h3>
        <p><strong>Base URL:</strong> {api.defaults.baseURL}</p>
        <p><strong>Environment:</strong> {import.meta.env.MODE}</p>
        <p><strong>VITE_API_BASE:</strong> {import.meta.env.VITE_API_BASE}</p>
      </div>
    </div>
  );
}