🛒 Mini E-Commerce API
A complete backend system for an online shopping platform built with Django REST Framework. This project implements user authentication, product management, shopping cart functionality, and order processing with proper business logic and data consistency.

📋 Table of Contents
Quick Start

Tech Stack

Database Schema

Architectural Decisions

Assumptions

API Endpoints

Testing

Project Structure

🚀 Quick Start
Prerequisites
Python 3.8+

pip (Python package manager)

Setup Instructions
1. Clone the Repository
bash
git clone <repository-url>
cd mini-ecommerce
2. Create and Activate Virtual Environment
bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
3. Install Dependencies
bash
pip install django djangorestframework djangorestframework-simplejwt pillow
4. Configure Database
bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate
5. Create Superuser (Admin)
bash
python manage.py createsuperuser
Follow the prompts to create an admin account.

6. Run Development Server
bash
python manage.py runserver
Server will start at: http://127.0.0.1:8000/

🛠️ Tech Stack
Backend
Framework: Django 4.2.7

API Framework: Django REST Framework 3.14.0

Authentication: JWT with Simple JWT 5.3.0

Database: SQLite (Development), PostgreSQL-ready

Image Handling: Pillow 10.0.0

Architecture
Design Pattern: Model-View-Template (MVT)

API Style: RESTful

Authentication: Token-based (JWT)

Database: Relational with Django ORM

🗃️ Database Schema
ER Diagram
text
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│      User       │      │     Product     │      │      Cart       │
├─────────────────┤      ├─────────────────┤      ├─────────────────┤
│ id (PK)         │      │ id (PK)         │      │ id (PK)         │
│ email           │──────│ name            │      │ user_id (FK)    │────┐
│ password        │      │ description     │      │ product_id (FK) │    │
│ first_name      │      │ price           │◄─┐   │ quantity        │    │
│ last_name       │      │ stock           │  │   │ created_at      │    │
│ phone           │      │ image           │  │   │ updated_at      │    │
│ role            │      │ created_at      │  │   └─────────────────┘    │
│ is_active       │      │ updated_at      │  │                           │
│ created_at      │      └─────────────────┘  │   ┌─────────────────┐    │
│ updated_at      │                           │   │     Order       │    │
└─────────────────┘                           │   ├─────────────────┤    │
                   1:N                       │   │ id (PK)         │    │
┌─────────────────┐                           │   │ order_number    │    │
│    OrderItem    │                           │   │ user_id (FK)    │────┘
├─────────────────┤                           │   │ total_amount    │
│ id (PK)         │                           │   │ status          │
│ order_id (FK)   │──────┐                    │   │ shipping_address│
│ product_id (FK) │──────┼────────────────────┘   │ payment_method  │
│ quantity        │      │                    │   │ created_at      │
│ price           │      │                    │   │ updated_at      │
│ subtotal        │      │                    │   └─────────────────┘
└─────────────────┘      │                    │
                   1:N   │                    │
                         │                    │
┌─────────────────┐      │                    │
│   Payment       │      │                    │
├─────────────────┤      │                    │
│ id (PK)         │      │                    │
│ order_id (FK)   │──────┘                    │
│ amount          │                           │
│ method          │                           │
│ status          │                           │
│ transaction_id  │                           │
│ created_at      │                           │
└─────────────────┘                           │
Models Description
1. User Model
Fields: id, email, password, first_name, last_name, phone, role (admin/customer)

Purpose: User authentication and role management

2. Product Model
Fields: id, name, description, price, stock, image, created_at, updated_at

Purpose: Product catalog management

3. Cart Model
Fields: id, user (FK), product (FK), quantity, created_at, updated_at

Purpose: Shopping cart functionality

4. Order Model
Fields: id, order_number, user (FK), total_amount, status, shipping_address, payment_method, created_at, updated_at

Purpose: Order management and tracking

5. OrderItem Model
Fields: id, order (FK), product (FK), quantity, price, subtotal

Purpose: Individual items within an order

🏗️ Key Architectural Decisions
1. App Separation
text
mini-ecommerce/
├── users/           # Authentication & user management
├── products/        # Product CRUD operations
├── cart/           # Shopping cart logic
├── orders/         # Order processing
└── config/         # Project configuration
Reason: Each feature is isolated for better maintainability and scalability.

2. JWT Authentication
Why: Stateless, scalable, and mobile-friendly

Implementation:

Access Token: 1 day expiry

Refresh Token: 7 days expiry

Token blacklisting for logout

3. Role-Based Access Control (RBAC)
Admin: Full access (product CRUD, user management)

Customer: Restricted access (cart, orders, profile)

4. Database Transactions
python
@transaction.atomic
def create_order():
    # Critical operations are atomic
    # Either all succeed or all fail
Reason: Prevents data inconsistency in order processing

5. RESTful API Design
Resource-based URLs (/api/products/, /api/cart/)

Proper HTTP methods (GET, POST, PUT, DELETE)

Standard HTTP status codes (200, 201, 400, 401, 403, 404)

6. Business Logic in Backend
Stock validation before order

Price calculation on server

Inventory management rules

📋 Assumptions Made
1. User Management
Email is the unique identifier (not username)

Phone number is optional

Users can be either 'admin' or 'customer'

Admin users are created via Django admin panel

2. Product Management
Products have unlimited categories (no category model for simplicity)

Product images are optional

Stock cannot be negative

Price is in decimal format (2 decimal places)

3. Cart Functionality
One user can have multiple cart items

Same product cannot be added twice (quantity updates instead)

Cart persists until order placement or manual clearance

4. Order Processing
Order cannot be placed with empty cart

Stock is checked at order creation time

Order total is calculated on backend

Order status flow: Pending → Confirmed → Shipped → Delivered

5. Payment System
Payment simulation only (no real payment gateway)

Default payment method: Cash on Delivery (COD)

Payment status not tracked in this version

6. Shipping & Delivery
No shipping cost calculation

No delivery time estimation

Shipping address is simple text field

7. Security
JWT tokens stored in localStorage (frontend responsibility)

No HTTPS in development

Password hashing handled by Django

No brute force protection (rate limiting not implemented)

📊 API Endpoints
Authentication
Method	Endpoint	Description	Access
POST	/api/auth/register/	User registration	Public
POST	/api/auth/login/	User login	Public
POST	/api/auth/logout/	User logout	Authenticated
GET	/api/auth/profile/	User profile	Authenticated
PUT	/api/auth/profile/	Update profile	Authenticated
Products
Method	Endpoint	Description	Access
GET	/api/products/	List all products	Authenticated
POST	/api/products/	Create product	Admin only
GET	/api/products/{id}/	Product details	Authenticated
PUT	/api/products/{id}/	Update product	Admin only
DELETE	/api/products/{id}/	Delete product	Admin only
Cart
Method	Endpoint	Description	Access
GET	/api/cart/	View cart	Customer
POST	/api/cart/	Add to cart	Customer
GET	/api/cart/{id}/	Cart item details	Customer
PUT	/api/cart/{id}/	Update quantity	Customer
DELETE	/api/cart/{id}/	Remove from cart	Customer
DELETE	/api/cart/clear/	Clear cart	Customer
Orders
Method	Endpoint	Description	Access
GET	/api/orders/	List orders	Customer
POST	/api/orders/create/	Place order	Customer
GET	/api/orders/{id}/	Order details	Customer
POST	/api/orders/{id}/cancel/	Cancel order	Customer
🧪 Testing the API
Using Postman
Sample Registration:
bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
Sample Login:
bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
Using the Access Token:
bash
curl -X GET http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
📝 Project Structure
text
mini-ecommerce/
├── config/                 # Project settings
│   ├── __init__.py
│   ├── settings.py        # All configurations
│   ├── urls.py            # URL routing
│   └── wsgi.py
├── users/                  # Authentication app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Custom User model
│   ├── serializers.py     # User serializers
│   ├── urls.py            # Auth endpoints
│   ├── views.py           # Auth views
│   └── permissions.py     # Role-based permissions
├── products/              # Product management
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Product model
│   ├── serializers.py     # Product serializers
│   ├── urls.py            # Product endpoints
│   └── views.py           # Product views
├── cart/                  # Shopping cart
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Cart model
│   ├── serializers.py     # Cart serializers
│   ├── urls.py            # Cart endpoints
│   └── views.py           # Cart views
├── orders/                # Order processing
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Order & OrderItem models
│   ├── serializers.py     # Order serializers
│   ├── urls.py            # Order endpoints
│   └── views.py           # Order views
├── manage.py
└── requirements.txt
🚨 Important Notes
Security Considerations
This is a development project, not production-ready

Use environment variables for sensitive data in production

Implement HTTPS in production

Add rate limiting for public endpoints

Scalability Considerations
Current implementation uses SQLite (suitable for development)

For production, use PostgreSQL or MySQL

Add caching for frequently accessed data

Future Enhancements
Payment Integration: Stripe, PayPal, or bKash

Email Notifications: Order confirmation, shipping updates

Search Functionality: Elasticsearch or Django Haystack

Product Reviews & Ratings: Customer feedback system

Wishlist: Save products for later

📄 License
This project is created for educational purposes as part of a technical assignment.

👥 Contributors
Developed as a backend assignment

Follows RESTful API design principles

Implements JWT authentication and role-based access control