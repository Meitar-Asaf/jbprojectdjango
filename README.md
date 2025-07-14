# 🌍 Dreamy Vacations — Django Web Application

This is a Django-based web app for managing, browsing, and booking vacation packages.
The project includes initial sample data, user authentication, an admin panel, and a test suite.

---

## 📖 What This Project Includes

* A vacation browsing and booking system
* Admin interface for managing vacations
* User authentication (email as username)
* Likes system for vacations
* Custom frontend with CSS styling and background imagery
* JSON fixture data for development and test environments
* Automated Django tests

---

## ⚙️ Project Setup (For Local Development)

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure PostgreSQL database:**
   Make sure you have PostgreSQL installed and running.
   Create the database if it doesn’t exist:

   ```sql
   CREATE DATABASE vacations_db;
   ```

   Update your `settings.py` with the following database settings:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'vacations_db',
           'USER': 'postgres',
           'PASSWORD': 'Meitar1997!',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Load initial sample data:**

   ```bash
   python manage.py loaddata initial_data.json
   ```

---

## 👥 Test User Accounts (Already Included)

**Regular User**

* Email: `testuser@example.com`
* Password: `UserPass123`

**Superuser (Admin Access)**

* Email: `admin@example.com`
* Password: `Admin456!`

To access the Django admin panel:
[http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 📦 Included Data

After loading `initial_data.json`, the database will include:

* 10 countries
* 12 vacation packages
* 2 user accounts

---

## 🧪 Running the Test Suite

To run all Django tests:

```bash
python manage.py test
```

---

## 📌 Important Notes for New Developers

* User authentication is based on email as username.
* A favicon request may appear in the logs; optionally add a `favicon.ico` to `static/`.
* Static files are in the `static/` directory and loaded via `{% static %}` tags.
* Admin users can add/edit/delete vacations.
* Likes system implemented for vacations.
* Uses Django’s messages framework for notifications.
* Data fixtures must be loaded before development/testing.

---

## ✅ Quick Start Commands Summary

```bash
# Virtual environment setup
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Load initial data
python manage.py loaddata initial_data.json

# Run server
python manage.py runserver

# Run tests
python manage.py test
```

---

## 📩 Questions?

If you’re new to this project or Django, feel free to contact the original developer or project maintainer for clarifications.

Happy coding ✈️

---

רוצה שאכין לך את הקובץ בפורמט `.md` מוכן להורדה?

