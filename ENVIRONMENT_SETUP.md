# Environment Setup Instructions for CarpatiNest

## Security Configuration

This project now uses environment variables to protect sensitive information like email credentials and secret keys from being exposed in version control.

## Setup Instructions

### 1. Environment Variables Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your actual values:
   ```
   SECRET_KEY=your-actual-django-secret-key
   EMAIL_HOST_USER=your-gmail-address@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   DEFAULT_FROM_EMAIL=your-gmail-address@gmail.com
   DEBUG=True
   ```

### 2. Gmail App Password Setup

For EMAIL_HOST_PASSWORD, you need to create a Gmail App Password:

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. At the bottom, select "App passwords"
4. Generate a new app password for "Mail"
5. Use this 16-character password in your `.env` file

### 3. Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Security Features

- ✅ **Email credentials protected** - No longer hardcoded in settings.py
- ✅ **Secret key secured** - Stored in environment variables
- ✅ **Comprehensive .gitignore** - Prevents accidental exposure of sensitive files
- ✅ **Environment template** - .env.example shows required variables without exposing values

## Important Security Notes

⚠️ **Never commit the `.env` file to version control**
⚠️ **Always use App Passwords for Gmail, never your regular password**
⚠️ **Generate a new SECRET_KEY for production environments**
⚠️ **Set DEBUG=False in production**

## Files Protected by .gitignore

- `.env` files (all variations)
- Database files (`db.sqlite3`)
- Python cache files (`__pycache__/`, `*.pyc`)
- Media and static files directories
- IDE configuration files
- Virtual environment directories

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key for cryptographic signing | `django-insecure-xyz...` |
| `EMAIL_HOST_USER` | Gmail address for sending emails | `yourapp@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Gmail app password (16 characters) | `abcd efgh ijkl mnop` |
| `DEFAULT_FROM_EMAIL` | Default sender email address | `yourapp@gmail.com` |
| `DEBUG` | Enable/disable debug mode | `True` or `False` |

Your SMTP credentials and other sensitive data are now secure! 🔒
