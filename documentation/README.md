# Maison des Fleurs

A premium, modern e-commerce web application for a boutique flower shop, built using Python (Flask) and SQLite.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [How to Run](#how-to-run)
- [Database Structure](#database-structure)

## Features
- **Sophisticated Design System**: Hand-crafted custom vanilla CSS with HSL coloring, modern Google Fonts, subtle hover zoom animations, and premium glassmorphic overlays.
- **Responsive Layout**: Fluid mobile navigation menu and adaptive grid structures for featured products and story/testimonial highlights.
- **User Authentication**: Secure sign-up, login, and logout routines powered by Flask-Login and password hashing.
- **Product Storefront**: Interactive product grid displaying named items, pricing in PHP (₱), and quick purchase flows.
- **Admin Dashboard**: Secure management interface for products and order tracking.

## Tech Stack
- **Backend**: Python 3, Flask framework
- **Database**: SQLite with SQLAlchemy ORM
- **Migrations**: Flask-Migrate
- **Frontend**: Vanilla HTML5, Custom CSS3, Boxicons, Bootstrap 5 (for structure & utility grid)

## Project Structure
```text
Flower-main/
│
├── app.py                  # Core Flask Application & Routes
├── instance/               # Database Instance Directory
│   └── flower.db           # SQLite Database File
│
├── static/                 # Static Assets
│   ├── css/
│   │   └── style.css       # Core Styled Design System
│   ├── image/              # Graphic & Flower Assets
│   ├── js/                 # Javascript files
│   └── uploads/            # Admin Uploaded Product Images
│
├── templates/              # Jinja2 HTML Templates
│   ├── Base/
│   │   └── layout.html     # Unified Shell Layout
│   ├── Users/              # Customer Front-facing Pages
│   └── Admin/              # Management Dashboard Panels
│
└── venv/                   # Python Virtual Environment
```

## Getting Started
To get the project set up on your local machine, ensure you have Python 3 installed.

## How to Run

1. **Activate the virtual environment**:
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Start the Flask server**:
   ```powershell
   python app.py
   ```

3. **Access in browser**:
   Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser.

## Deployment to Render

To deploy this project for free on Render:

1. **Push your code to GitHub**:
   - Create a repository on GitHub (e.g. `Flower-Shop`).
   - Push your project files to the repository. Make sure `requirements.txt` is in the root directory and your `.gitignore` excludes the `venv/` folder.

2. **Connect to Render**:
   - Log in to [Render](https://render.com/).
   - Click **New +** and select **Web Service**.
   - Connect your GitHub account and select your repository.

3. **Configure the Web Service**:
   - **Name**: `ray-flowers` (or any name you like)
   - **Region**: Select the closest region to your users
   - **Branch**: `main`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Select the **Free** plan.

4. **Click Deploy**:
   Render will build the project and provide a live URL (e.g., `https://ray-flowers.onrender.com`).

