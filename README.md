# 🛒 Mini E-Commerce API

A complete backend system for an online shopping platform built with **Django REST Framework**.  
This project implements user authentication, product management, shopping cart functionality, and order processing with proper business logic and data consistency.

---

## 📋 Table of Contents
- Quick Start
- Tech Stack
- Database Schema
- Architectural Decisions
- Assumptions
- API Endpoints
- Testing
- Project Structure

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

#### 1. Clone the Repository

git clone <repository-url>
cd mini-ecommerce

### 2. Create and Activate Virtual Environment

python -m venv venv

## Windows
venv\Scripts\activate

## Mac/Linux
source venv/bin/activate

###3. Install Dependencies
pip install django djangorestframework djangorestframework-simplejwt pillow


###4. Configure Database
python manage.py makemigrations
python manage.py migrate


###5. Create Superuser (Admin)
python manage.py createsuperuser


###6. Run Development Server
python manage.py runserver
Server will run at:
http://127.0.0.1:8000/


###🛠️ Tech Stack
Backend
Django 4.2.7
Django REST Framework 3.14.0
JWT Authentication (Simple JWT 5.3.0)
SQLite (Development)
PostgreSQL (Production ready)
Pillow 10.0.0


###Architecture
Design Pattern: MVT
API Style: RESTful
Authentication: Token-based (JWT)
ORM: Django ORM


###🗃️ Database Schema
ER Diagram
text
Copy code
User ────< Cart >──── Product
  │                      │
  └────< Order >────< OrderItem >


###Models Description

##User
email (unique)
password
first_name
last_name
phone
role (admin, customer)


##Product
name
description
price
stock
image
created_at
updated_at


##Cart
user (FK)
product (FK)
quantity
created_at
updated_at


##Order
order_number
user (FK)
total_amount
status
shipping_address
payment_method
created_at
updated_at


##OrderItem
order (FK)
product (FK)
quantity
price
subtotal


###🏗️ Architectural Decision

##1. App Separation
text
Copy code
mini-ecommerce/
├── users/
├── products/
├── cart/
├── orders/
└── config/
Each feature is separated for better maintainability and scalability.

##2. JWT Authentication
Access Token: 1 day
Refresh Token: 7 days
Stateless and scalable

##3. Role-Based Access Control
Admin: Full access
Customer: Cart and order access only

##4. Database Transactions
@transaction.atomic
def create_order():
    pass
Ensures data consistency during order creation.


###📋 Assumptions

##User
Email is unique
Two roles: admin and customer
Admin created from Django admin

##Product
No category system
Image is optional
Stock cannot be negative

##Cart
One user can have multiple cart items
Same product updates quantity
Cart clears after order

##Order
Cart must not be empty
Stock checked before order

##Status flow:
Pending → Confirmed → Shipped → Delivered

##Payment
Payment simulation only
Default: Cash on Delivery
No real payment gateway

###📊 API Endpoints

##Authentication
Method	Endpoint	Description	Access
POST	/api/auth/register/	Register user	Public
POST	/api/auth/login/	Login user	Public
POST	/api/auth/logout/	Logout	Authenticated
GET	/api/auth/profile/	View profile	Authenticated
PUT	/api/auth/profile/	Update profile	Authenticated

##Products
Method	Endpoint	Description	Access
GET	/api/products/	List products	Authenticated
POST	/api/products/	Create product	Admin
GET	/api/products/{id}/	Product details	Authenticated
PUT	/api/products/{id}/	Update product	Admin
DELETE	/api/products/{id}/	Delete product	Admin

##Cart
Method	Endpoint	Description
GET	/api/cart/	View cart
POST	/api/cart/	Add to cart
PUT	/api/cart/{id}/	Update cart
DELETE	/api/cart/{id}/	Remove item
DELETE	/api/cart/clear/	Clear cart

##Orders
Method	Endpoint	Description
GET	/api/orders/	List orders
POST	/api/orders/create/	Place order
GET	/api/orders/{id}/	Order details
POST	/api/orders/{id}/cancel/	Cancel order