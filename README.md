# 🌍 Dreamy Vacations — Django Web Application

This is a Django-based web app for managing, browsing, and booking vacation packages.  
The project includes initial sample data, user authentication, an admin panel, and a test suite.

---

## 📖 What This Project Includes

- A vacation browsing and booking system
- Admin interface for managing vacations
- User authentication (email as username)
- Likes system for vacations
- Custom frontend with CSS styling and background imagery
- JSON fixture data for development and test environments
- Automated Django tests

---

## ⚙️ Project Setup (For Local Development)

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
````

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Load initial sample data:**

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

### Loading Custom Test Data for Tests

If the tests depend on specific test data (like `test_data.json`), it should be placed in the root directory (same as `manage.py`) and loaded inside the test class using:

```python
from django.test import TestCase
from django.core.management import call_command

class ExampleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'test_data.json')
```

Django automatically creates a **temporary test database** when running tests, so your main data is safe.

---

## 📌 Important Notes for New Developers

* **User authentication** is based on **email as username**.
* A **favicon request** may appear in the logs. You can optionally add a `favicon.ico` to `static/` if needed.
* All static files are in the `static/` directory and loaded via `{% static %}` tags in templates.
* **Admin users** have permissions to add, edit, and delete vacation packages.
* A **likes system** is implemented for vacations.
* Custom fonts and CSS are loaded via Google Fonts and local static files.
* Uses Django’s **messages framework** for success/error notifications.
* Data fixtures must be loaded before development or testing for proper functionality.

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
