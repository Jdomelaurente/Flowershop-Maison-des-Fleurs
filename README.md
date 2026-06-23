# Maison des Fleurs

Flask-based flower shop application with authentication, product browsing, cart flow, and admin management tools.

Commissioned project by a student of Father Saturnino Urios University, Butuan City.

## Overview

- Flask for the web app
- SQLite for storage
- SQLAlchemy and Flask-Migrate for database access and migrations
- Flask-Login for authentication
- Bootstrap and custom CSS for the UI

## Features

- Customer landing page and informational pages
- User registration and login
- Session-based cart
- Purchase flow for items
- Admin dashboard for managing products
- Admin view for orders and users
- Upload support for product images

## Project Structure

```text
Flower-main/
|-- app.py
|-- requirements.txt
|-- instance/
|   `-- flower.db
|-- migrations/
|-- static/
|-- templates/
`-- venv/
```

## Requirements

- Python 3.10+ recommended
- A local virtual environment

## Quick Start

```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

## Default Admin

The app creates a default admin user on first startup if one does not already exist:

- Username: `admin`
- Password: `admin123`

Change this immediately if you plan to use the app beyond local testing.

## Main Routes

- `/` - Home page
- `/login` - Login form
- `/register` - Registration form
- `/logout` - Log out
- `/admin/dashboard` - Admin product dashboard
- `/admin_orders` - Admin orders page
- `/user-dashboard` - Logged-in user dashboard
- `/user_product_dashboard` - Product listing and cart actions
- `/view_cart` - Cart page
- `/checkout` - Checkout page
- `/payment` - Payment page
- `/add` - Add new item for admin
- `/manage_users` - User management page

## Database Models

- `User`
- `Item`
- `Cart`
- `Order`

## Database Notes

- On local development, the database file lives at `instance/flower.db`
- Uploaded product images are saved in `static/uploads/`
- If the app is deployed on Render, it uses `/tmp/flower.db` and `/tmp/uploads`

## Deployment Notes

For Render or another Linux host:

- Install dependencies with `pip install -r requirements.txt`
- Start the app with `gunicorn app:app`
- Set `SECRET_KEY` in the environment for production use

## Known Project Notes

- Some routes and templates are still rough around the edges and may need cleanup for production use
- The app currently relies on the bundled SQLite database
- The admin password is hardcoded for first-time setup, so it should be changed before real use
