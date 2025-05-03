# SaaS Template Backend

A Django-based backend template for SaaS applications with authentication, user management, and subscription features.

## Features

- User authentication (email/password)
- Google OAuth2 authentication
- Password reset functionality with OTP
- JWT token-based authentication
- User profile management
- Subscription management
- Email notifications
- Celery task queue
- Redis caching
- CORS support
- Swagger/OpenAPI documentation

## Prerequisites

- Python 3.8+
- Redis
- PostgreSQL (optional, SQLite by default)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Polyakiv-Andrey/Saas-template-backend.git
cd Saas-template-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email Settings
SENDGRID_API_KEY=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=your-email@example.com

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:5174
CORS_ALLOW_ALL_ORIGINS=True

# Celery Settings
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Start Celery worker (in a separate terminal):
```bash
celery -A saas_template_backend worker -l info
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Project Structure

```
saas_template_backend/
├── api/
│   ├── api/
│   ├── authentication/
│   └── subscription/
├── saas_template_backend/
├── .env
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 