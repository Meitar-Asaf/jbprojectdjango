בשמחה מיתר! הנה **קובץ README מלא ומוכן** — כולל הכל: הוראות התקנה, טעינת נתונים, והרשאות התחברות עם אימייל וסיסמה של המשתמשים שהכנסת בקובץ ה־JSON שלך. את יכולה פשוט **להעתיק את כל זה לקובץ בשם `README.md`** בפרויקט:

```markdown
# 🌍 Vacation Booking Project

This is a Django-based web application for managing and browsing vacation packages. It includes sample data such as countries, vacations, and test user accounts for development.

---

## ⚙️ Setup Instructions

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Load initial data from the provided fixture file:

   ```bash
   python manage.py loaddata initial_data.json
   ```

---

## 👥 Test Users

After loading the data, you can log in using these accounts:

### Regular User
- **Email (used as username):** `testuser@example.com`  
- **Password:** `UserPass123`

### Admin User
- **Email (used as username):** `admin@example.com`  
- **Password:** `Admin456!`

To access the Django admin panel, go to:  
[http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 📦 Included Sample Data

- 10 countries
- 12 vacation packages
- 2 user accounts (see above)

---
