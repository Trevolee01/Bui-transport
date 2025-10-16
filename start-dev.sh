#!/bin/bash

echo "Starting BUI Transport Development Environment..."
echo

echo "Starting Django Backend..."
cd backend
source venv/bin/activate
python manage.py runserver 127.0.0.1:8000 &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting React Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo
echo "Development servers are starting..."
echo "Backend: http://127.0.0.1:8000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait