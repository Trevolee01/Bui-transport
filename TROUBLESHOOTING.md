# BUI Transport - Login/Registration Troubleshooting Guide

## Issues Identified and Fixed

### 1. **Backend Model Corruption** ✅ FIXED
- **Problem**: The `backend/apps/users/models.py` file had corrupted regex patterns
- **Solution**: Rewrote the entire models.py file with correct regex patterns
- **Impact**: This was preventing the Django server from starting properly

### 2. **Missing Backend Environment Configuration** ✅ FIXED
- **Problem**: No `.env` file in the backend directory
- **Solution**: Created `backend/.env` with proper development settings
- **Impact**: Django settings were using defaults which might not work correctly

### 3. **Enhanced Error Logging** ✅ ADDED
- **Problem**: Limited error information in frontend
- **Solution**: Added comprehensive error logging in AuthContext
- **Impact**: Now you can see detailed error information in browser console

## How to Debug the Issue

### Step 1: Check Backend Server
1. Open terminal in `backend` directory
2. Run: `python manage.py runserver`
3. If you get Python not found error, activate your virtual environment first:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Then run
   python manage.py runserver
   ```

### Step 2: Test API Endpoints
1. Go to: `http://localhost:3000/?debug=api` (when frontend is running)
2. Click "Test Server Connection" to check if backend is reachable
3. Click "Test Registration" to test the registration endpoint

### Step 3: Check Browser Console
1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Try to register/login and check for detailed error messages

### Step 4: Check Network Tab
1. In Developer Tools, go to Network tab
2. Try to register/login
3. Look for failed requests and their response details

## Common Issues and Solutions

### Issue: "Server is not running"
**Solution**: Start the Django backend server
```bash
cd backend
python manage.py runserver
```

### Issue: "CORS Error"
**Solution**: Backend settings already configured for CORS, but check if frontend URL matches

### Issue: "Database Error"
**Solution**: Run migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Validation Error"
**Solution**: Check that all required fields are being sent:
- email
- username
- first_name
- last_name
- phone_number
- role
- password
- password_confirm

## Files Modified for Debugging

1. `backend/.env` - Created with development settings
2. `backend/apps/users/models.py` - Fixed corrupted regex patterns
3. `frontend/src/contexts/AuthContext.jsx` - Added detailed error logging
4. `frontend/src/components/ApiTest.jsx` - Created debug component
5. `frontend/src/pages/Login.jsx` - Added debug mode access

## Next Steps

1. **Start Backend Server**: Make sure Django is running on port 8000
2. **Test API**: Use the debug component at `/?debug=api`
3. **Check Console**: Look for detailed error messages
4. **Report Findings**: Share the console output for further debugging

## Quick Test Commands

```bash
# Test if backend is accessible
curl http://127.0.0.1:8000/api/auth/register/

# Test registration endpoint
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","first_name":"Test","last_name":"User","phone_number":"1234567890","role":"student","password":"testpass123","password_confirm":"testpass123"}'
```