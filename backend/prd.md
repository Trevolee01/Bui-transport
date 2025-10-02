BUI Transport System - Project Overview
Problem Statement
Students at BUI face significant challenges with transportation services:
•	Lack of centralized platform: Students struggle to find reliable transport options to various destinations
•	Limited visibility: Transport organizers have no efficient way to showcase their services to students
•	Trust and safety concerns: No verification system for transport providers, leading to unreliable services
•	Manual booking process: Students rely on word-of-mouth and informal WhatsApp groups for bookings
•	Poor management oversight: University administration lacks visibility into transport operations and cannot ensure service quality
•	Poor management oversight: University administration lacks visibility into transport operations and cannot ensure service quality
•	Communication Gaps: Poor communication between students and transport organizers
•	Inefficient resource utilization: Transport organizers cannot optimize their routes and capacity based on demand
Solution
A comprehensive web-based transport management platform that connects students with verified transport organizers while providing administrative oversight.
Key Features:
For Students:
•	Browse verified transport options with detailed information
•	Book rides securely with real-time availability
•	View booking history and manage current reservations
•	Rate and review transport organizers
•	Receive notifications about booking confirmations and updates
For Transport Organizers:
•	Register and get verified by university administration
•	List transport services with routes, schedules, and pricing
•	Manage bookings and passenger lists
•	Communicate with students through the platform
•	Track earnings and booking statistics
For University Administration:
•	Approve and verify transport organizer applications
•	Monitor transport operations and safety standards
•	Remove unreliable or unsafe transport providers
•	Generate reports on transport usage and incidents
•	Maintain oversight of all campus transport activities
User Flow
Student Journey
1.	Registration/Login → Create account or sign in
2.	Browse Transport Options → View available routes, schedules, and prices
3.	Select Service → Choose preferred transport based on destination and time
4.	Make Booking → Reserve seat and receive confirmation
5.	Manage Bookings → View, modify, or cancel existing bookings
6.	Receive Confirmation
7.	Provide Feedback → Rate and review transport services
Transport Organizer Journey
1.	Registration → Apply to become a transport organizer
2.	Wait for Approval → Admin reviews and verifies credentials
3.	Account Setup → Complete profile with vehicle and route information
4.	Receive Payments & Reviews
5.	List Services → Create transport options with routes, schedules, and pricing
6.	Manage Bookings → View and manage student reservations
7.	Update Availability → Real-time updates on seat availability
Admin Journey
1.	Login to Dashboard → Access administrative panel
2.	Review Applications → Evaluate and approve/reject transport organizer requests
3.	Monitor Services → Oversee transport operations and service quality
4.	Manage Users → Handle user accounts and resolve issues
5.	Remove Providers → Deactivate unreliable transport organizers
6.	Generate Reports → View system analytics and usage statistics
Database Schema
Users Table
- id (Primary Key)
- email (Unique)
- password (Hashed)
- first_name
- last_name
- phone_number
- role (student, transport_organizer, admin)
- is_verified
- created_at
- updated_at

Students Table

- id (Primary Key)
- user_id (Foreign Key → Users)
- student_id (University ID)
- department
- level (100, 200, 300, 400, 500)
- hostel_name
- room_number
- emergency_contact_name
- emergency_contact_phone
- is_verified
- verification_date
- created_at
- updated_at
Transport Organizers Table
CREATE TABLE transport_organizers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_name VARCHAR(200) NOT NULL,
    license_number VARCHAR(100),
    vehicle_count INTEGER DEFAULT 0,
    bank_account_number VARCHAR(50),
    bank_name VARCHAR(100),
    account_holder_name VARCHAR(200),
    mobile_money_number VARCHAR(20),
    approval_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approval_date TIMESTAMP,
    approved_by UUID REFERENCES users(id),
    rating DECIMAL(3,2) DEFAULT 0.00,
    total_trips INTEGER DEFAULT 0,
    total_earnings DECIMAL(12,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);Transport Options Table
- id (Primary Key)
- organizer_id (Foreign Key → Transport Organizers)
- route_name
- departure_location
- destination
- departure_time
- arrival_time
- price
- total_seats
- available_seats
- days_of_operation (JSON)
- is_active
- created_at
- updated_at
Bookings Table
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    transport_option_id UUID REFERENCES transport_options(id) ON DELETE CASCADE,
    booking_date DATE NOT NULL,
    seats_booked INTEGER DEFAULT 1,
    total_amount DECIMAL(10,2) NOT NULL,
    platform_fee DECIMAL(10,2) DEFAULT 0.00,
    organizer_amount DECIMAL(10,2) NOT NULL,
    booking_status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'refunded', 'failed') DEFAULT 'pending',
    payment_method ENUM('wallet', 'mobile_money', 'bank_transfer', 'card') NOT NULL,
    payment_reference VARCHAR(100) UNIQUE,
    refund_amount DECIMAL(10,2) DEFAULT 0.00,
    refund_status ENUM('none', 'requested', 'approved', 'rejected', 'processed') DEFAULT 'none',
    refund_reason TEXT,
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Reviews Table
- id (Primary Key)
- booking_id (Foreign Key → Bookings)
- student_id (Foreign Key → Users)
- transport_option_id (Foreign Key → Transport Options)
- rating (1-5)
- comment
- created_at
Admin Actions Table
- id (Primary Key)
- admin_id (Foreign Key → Users)
- action_type (approve_organizer, remove_organizer, etc.)
- target_id (ID of affected record)
- reason
- created_at

Communication Reports table

CREATE TABLE communication_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_id UUID REFERENCES users(id) ON DELETE CASCADE,
    reported_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    report_type ENUM('spam', 'harassment', 'inappropriate_content', 'fraud', 'other') NOT NULL,
    description TEXT NOT NULL,
    status ENUM('pending', 'reviewed', 'resolved', 'dismissed') DEFAULT 'pending',
    admin_notes TEXT,
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


Notification table


CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type ENUM('booking', 'payment', 'trip_update', 'message', 'approval', 'reminder', 'general') NOT NULL,
    related_id UUID, -- Can reference booking_id, message_id, etc.
    is_read BOOLEAN DEFAULT false,
    is_push_sent BOOLEAN DEFAULT false, -- For mobile push notifications
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Audit Logs Table

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(100),
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Payment Methods Table

CREATE TABLE payment_methods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    method_type ENUM('mobile_money', 'bank_card', 'bank_account') NOT NULL,
    provider_name VARCHAR(100) NOT NULL, -- MTN, Airtel, Visa, MasterCard, etc.
    account_number VARCHAR(100), -- Phone number for mobile money, card number (encrypted), account number
    account_name VARCHAR(200),
    is_primary BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Transactions Table
sql
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id) ON DELETE CASCADE,
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    organizer_id UUID REFERENCES transport_organizers(id),
    transaction_type ENUM('payment', 'refund', 'wallet_topup', 'payout') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'NGN',
    payment_method ENUM('wallet', 'mobile_money', 'bank_transfer', 'card') NOT NULL,
    payment_reference VARCHAR(100) UNIQUE NOT NULL,
    external_reference VARCHAR(100), -- Payment gateway reference
    status ENUM('pending', 'success', 'failed', 'cancelled') DEFAULT 'pending',
    gateway_response JSONB,
    description TEXT,
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Wallet Transactions Table
sql
CREATE TABLE wallet_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    transaction_type ENUM('credit', 'debit') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    balance_before DECIMAL(10,2) NOT NULL,
    balance_after DECIMAL(10,2) NOT NULL,
    reference_type ENUM('booking', 'refund', 'topup') NOT NULL,
    reference_id UUID, -- Can reference booking_id or transaction_id
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Refund Requests Table
sql
CREATE TABLE refund_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id) ON DELETE CASCADE,
    student_id UUID REFERENCES student_profiles(id) ON DELETE CASCADE,
    organizer_id UUID REFERENCES transport_organizers(id) ON DELETE CASCADE,
    refund_amount DECIMAL(10,2) NOT NULL,
    reason TEXT NOT NULL,
    status ENUM('pending', 'approved', 'rejected', 'processed') DEFAULT 'pending',
    admin_notes TEXT,
    processed_by UUID REFERENCES users(id),
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Messages Table
sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
    message_type ENUM('text', 'image', 'location', 'announcement', 'system') DEFAULT 'text',
    content TEXT NOT NULL,
    media_url VARCHAR(500), -- For images or files
    location_data JSONB, -- For GPS coordinates {"lat": 6.5244, "lng": 3.3792}
    is_read BOOLEAN DEFAULT false,
    replied_to UUID REFERENCES messages(id), -- For message replies
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Conversations Table
sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_type ENUM('direct', 'trip_group', 'support') NOT NULL,
    trip_id UUID REFERENCES transport_options(id), -- NULL for direct messages
    booking_id UUID REFERENCES bookings(id), -- For trip-specific conversations
    title VARCHAR(200), -- For group conversations
    is_active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Conversation Participants Table
sql
CREATE TABLE conversation_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role ENUM('admin', 'organizer', 'student') NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_read_at TIMESTAMP,
    is_muted BOOLEAN DEFAULT false,
    UNIQUE(conversation_id, user_id)
);
Trip Updates Table
sql
CREATE TABLE trip_updates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transport_option_id UUID REFERENCES transport_options(id) ON DELETE CASCADE,
    organizer_id UUID REFERENCES transport_organizers(id) ON DELETE CASCADE,
    update_type ENUM('delay', 'cancellation', 'route_change', 'location', 'general') NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    location_data JSONB, -- Current GPS location
    estimated_arrival TIME, -- For delay updates
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Technology Stack
Backend Development
•	Framework: Django REST Framework (DRF)
•	Language: Python
•	Authentication: JWT (JSON Web Tokens) using djangorestframework-simplejwt
•	Database: PostgreSQL (Production), SQLite (Development)
•	API Architecture: RESTful APIs
Frontend Development
•	Framework: React.jsx
•	Language: JavaScript
•	Styling: Tailwind CSS
•	HTTP Client: Axios for API requests
•	State Management: React hooks (useState, useEffect)
•	Authentication Storage: Local Storage for JWT tokens
Database & Deployment
•	Database: PostgreSQL
•	Backend Deployment: Render
•	Frontend Deployment: Vercel
•	Version Control: Git
•	Real-time Communication: WebSocket (Django Channels) for live messaging
•	Push Notifications: Firebase Cloud Messaging (FCM) or OneSignal
•	GPS/Location Services: Google Maps API or Mapbox
•	Payment Integration: Paystack/Flutterwave for Nigerian mobile money and card payments
Development Tools
•	Package Managers: pip (Python), npm (JavaScript)
•	Testing: Django Test Suite, Jest (for React components)
•	Code Quality: ESLint, Prettier
•	API Documentation: Django REST Framework browsable API

Key Relationships
•	Users have different roles (student, organizer, admin)
•	Students can make one Bookings at a time and have Payment Methods
•	Students participate in Conversations and receive Messages
•	Students have Wallet Transactions for balance management
•	Transport Organizers can create multiple Transport Options and receive Transactions
•	Transport Organizers send Trip Updates and participate in Conversations
•	Bookings connect Students with Transport Options and generate Transactions
•	Bookings create Trip-specific Conversations for communication
•	Reviews are linked to completed Bookings
•	Messages belong to Conversations with multiple Participants
•	Trip Updates are broadcast to all passengers of a transport option
•	Communication Reports track inappropriate messaging behavior
•	Refund Requests are linked to Bookings and processed by Admins
•	Transactions track all financial activities (payments, refunds, payouts)
•	Admin Users can approve/reject Transport Organizers and Refund Requests
•	Notifications keep all users informed of bookings, payments, messages, and trip updates

