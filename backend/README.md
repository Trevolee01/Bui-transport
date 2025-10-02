# BUI Transport System - Backend

A comprehensive Django REST API for managing university transport services, connecting students with verified transport organizers while providing administrative oversight.

## Features

### For Students
- User registration and authentication
- Browse verified transport options
- Book rides with real-time availability
- Manage bookings and view history
- Rate and review transport services
- Wallet system for payments
- Real-time messaging with organizers

### For Transport Organizers
- Registration and verification process
- Create and manage transport routes
- Handle bookings and passenger lists
- Real-time trip updates
- Earnings tracking and payouts
- Communication with students

### For Administrators
- Approve/reject transport organizer applications
- Monitor transport operations
- Manage user accounts and resolve issues
- Generate reports and analytics
- Handle refund requests

## Technology Stack

- **Backend**: Django 4.2.7 + Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **API Architecture**: RESTful APIs
- **Real-time Communication**: Django Channels (WebSocket)
- **Payment Integration**: Paystack/Flutterwave support
- **Location Services**: Google Maps API integration

## Project Structure

```
bui_transport/
├── apps/
│   ├── users/           # User management and authentication
│   ├── transport/       # Transport options and reviews
│   ├── bookings/        # Booking management
│   ├── communications/  # Messaging and notifications
│   └── payments/        # Payment processing and wallet
├── bui_transport/       # Main project settings
├── manage.py
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite can be used for development)
- pip (Python package manager)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd bui_transport
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

Edit `.env` file with your configuration:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (PostgreSQL)
DB_NAME=bui_transport
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
USE_SQLITE=False

# For SQLite development, set:
# USE_SQLITE=True
```

### 5. Database Setup

#### Option A: PostgreSQL (Recommended for Production)

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE bui_transport;
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Option B: SQLite (Development)

1. Set `USE_SQLITE=True` in your `.env` file
2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register/` | POST | User registration |
| `/auth/login/` | POST | User login |
| `/auth/logout/` | POST | User logout |
| `/auth/profile/` | GET, PUT | User profile management |
| `/auth/change-password/` | POST | Change password |

### Transport Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/transport/options/` | GET | List transport options |
| `/transport/options/<id>/` | GET | Get transport option details |
| `/transport/options/create/` | POST | Create transport option (organizers) |
| `/transport/options/<id>/reviews/` | GET | Get reviews for transport option |

### Booking Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/bookings/` | GET | List user bookings |
| `/bookings/create/` | POST | Create new booking |
| `/bookings/<id>/` | GET, PUT | Booking details and updates |
| `/bookings/<id>/cancel/` | PUT | Cancel booking |

### Communication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/communications/conversations/` | GET, POST | List/create conversations |
| `/communications/conversations/<id>/messages/` | GET, POST | List/send messages |
| `/communications/notifications/` | GET | List notifications |

### Payment Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/payments/methods/` | GET, POST | Manage payment methods |
| `/payments/wallet/balance/` | GET | Get wallet balance |
| `/payments/wallet/topup/` | POST | Top up wallet |
| `/payments/transactions/` | GET | List transactions |

## User Roles

### Student
- Register and create student profile
- Browse and book transport options
- Manage bookings and payments
- Rate and review services
- Communicate with organizers

### Transport Organizer
- Register and await approval
- Create transport options
- Manage bookings
- Send trip updates
- Track earnings

### Administrator
- Approve/reject organizers
- Monitor system operations
- Handle reports and issues
- Manage user accounts

## API Usage Examples

### User Registration

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@bui.edu.ng",
    "username": "student123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+2348012345678",
    "role": "student",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### User Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@bui.edu.ng",
    "password": "securepassword123"
  }'
```

### Create Booking (with JWT token)

```bash
curl -X POST http://localhost:8000/api/bookings/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "transport_option": "transport-option-uuid",
    "booking_date": "2024-01-15",
    "seats_booked": 1,
    "payment_method": "wallet",
    "special_requests": "Window seat preferred"
  }'
```

## Database Models

### Core Models
- **User**: Custom user model with role-based authentication
- **StudentProfile**: Extended profile for students
- **TransportOrganizer**: Profile for transport organizers
- **TransportOption**: Available transport routes and schedules
- **Booking**: Student bookings for transport options
- **Transaction**: Financial transactions
- **Message**: Real-time messaging
- **Notification**: System notifications

## Development

### Running Tests

```bash
python manage.py test
```

### Code Quality

```bash
# Install development dependencies
pip install flake8 black isort

# Format code
black .
isort .

# Lint code
flake8 .
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## Deployment

### Production Settings

1. Set `DEBUG=False` in production
2. Configure proper database settings
3. Set up static file serving
4. Configure email settings
5. Set up SSL certificates
6. Configure payment gateway credentials

### Environment Variables for Production

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=production_db_name
DB_USER=production_db_user
DB_PASSWORD=production_db_password
DB_HOST=production_db_host
EMAIL_HOST=smtp.your-provider.com
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
PAYSTACK_PUBLIC_KEY=pk_live_your_public_key
PAYSTACK_SECRET_KEY=sk_live_your_secret_key
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team or create an issue in the repository.

## API Rate Limiting

The API implements rate limiting to prevent abuse:
- Authentication endpoints: 5 requests per minute
- General API endpoints: 100 requests per hour
- File upload endpoints: 10 requests per hour

## Security Features

- JWT-based authentication
- Password hashing with Django's built-in hashers
- CORS protection
- SQL injection protection
- XSS protection
- CSRF protection for web forms
- Input validation and sanitization
- Audit logging for sensitive operations