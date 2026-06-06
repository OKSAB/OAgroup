# OA Group — Website

A bilingual (EN/AR) professional profile website for OA Group, built with Python/Django and MySQL.

---

## Prerequisites

Make sure you have the following installed before you start:

- Python 3.10+
- pip
- MySQL 8.0+
- Git

---

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd OAgroup
```

---

## 2. Set Up a Virtual Environment

```bash
python -m venv venv
```

Activate it:

- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `Django 4.2`
- `mysqlclient` — MySQL driver for Django
- `django-environ` — environment variable management

---

## 4. Set Up MySQL

Log into MySQL and create the database and user:

```sql
mysql -u root -p

CREATE DATABASE oagroup_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'oagroup_user'@'localhost' IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON oagroup_db.* TO 'oagroup_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 5. Configure Environment Variables

Copy the example env file and fill it in:

```bash
cp .env.example .env
```

Open `.env` and set your values:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=oagroup_db
DB_USER=oagroup_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=3306
```

> **Generating a SECRET_KEY:**
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

---

## 6. Run Migrations

Apply the database migrations to create the required tables:

```bash
python manage.py migrate
```

You should see output confirming the `core_contactenquiry` table and Django's default auth/session tables have been created.

---

## 7. Create an Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password. This account is used to access the admin panel at `/admin/`.

---

## 8. Collect Static Files (Production Only)

For local development, Django serves static files automatically. For production deployments, run:

```bash
python manage.py collectstatic
```

---

## 9. Run the Development Server

```bash
python manage.py runserver
```

The site will be available at:

```
http://127.0.0.1:8000/
```

---

## Pages

| URL | Page |
|---|---|
| `/` | Home |
| `/about/` | About |
| `/services/` | Services |
| `/contact/` | Contact |
| `/admin/` | Admin panel |

---

## Contact Enquiries (Admin)

All form submissions from the `/contact/` page are saved to the database. To view and manage them:

1. Go to `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials
3. Click **Contact Enquiries** under the **Core** section

From there you can:
- View all submissions with name, email, subject, and timestamp
- Mark enquiries as read/unread
- Search by name, email, or subject
- Filter by read status or date

---

## Project Structure

```
OAgroup/
├── manage.py
├── requirements.txt
├── .env.example
├── .env                        # Your local config (not committed)
│
├── oagroup/                    # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                       # Main application
│   ├── models.py               # ContactEnquiry model
│   ├── views.py                # Page views + form handling
│   ├── admin.py                # Admin configuration
│   ├── urls.py                 # URL routes
│   └── migrations/
│
├── templates/                  # HTML templates
│   ├── base.html               # Base layout with nav, fonts, JS
│   ├── home.html
│   ├── about.html
│   ├── services.html
│   ├── contact.html
│   └── partials/
│       ├── nav.html
│       ├── footer.html
│       └── cta_band.html
│
└── static/
    └── css/
        └── main.css            # Full design system
```

---

## Environment Variables Reference

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | — |
| `DEBUG` | Debug mode (`True`/`False`) | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` |
| `DB_NAME` | MySQL database name | `oagroup_db` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | — |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |

---

## Deploying to Production

A few things to change before going live:

1. Set `DEBUG=False` in `.env`
2. Set `ALLOWED_HOSTS` to your actual domain, e.g. `oagroup.com,www.oagroup.com`
3. Use a strong, unique `SECRET_KEY`
4. Run `python manage.py collectstatic` and serve the `staticfiles/` directory via Nginx or a CDN
5. Use a production WSGI server such as **Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn oagroup.wsgi:application --bind 0.0.0.0:8000
   ```
6. Put Nginx in front of Gunicorn to handle SSL and static file serving
