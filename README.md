# SheConnect AI

A modern Django-based AI platform for intelligent conversations and AI-powered services.

## 🚀 Features

- **Modern Django Architecture** - Built with Django 5.2.5 and Python 3.13
- **Custom User Management** - Extended user model with profiles and subscription tiers
- **AI Service Integration** - Ready for OpenAI, Anthropic, and other AI providers
- **Conversation Management** - Track and manage AI conversations
- **Usage Analytics** - Monitor user service usage and token consumption
- **Beautiful UI** - Modern, responsive design with gradient backgrounds
- **Environment Configuration** - Flexible database setup (SQLite/MySQL)
- **Admin Interface** - Comprehensive Django admin for data management

## 🛠️ Tech Stack

- **Backend**: Django 5.2.5, Python 3.13
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in auth with custom user model
- **Image Handling**: Pillow for profile pictures
- **Environment**: django-environ for configuration management

## 📋 Prerequisites

- Python 3.13+
- pip (Python package manager)
- Git
- MySQL (optional, for production)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yathushakulenthiran/SheConnect-AI.git
cd SheConnect-AI
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Start Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see your application!

## 📁 Project Structure

```
sheconnect-ai/
├── core/                    # Core app with home page and health checks
├── users/                   # Custom user management
├── ai_services/            # AI service models and management
├── sheconnect_ai/          # Main project settings
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=UTC

# Database Configuration
DB_ENGINE=sqlite  # or mysql
DB_NAME=sheconnect_ai
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### MySQL Setup (Production)
1. Install MySQL
2. Create database: `CREATE DATABASE sheconnect_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
3. Update `.env` with MySQL credentials
4. Run migrations: `python manage.py migrate`

## 🎯 Available URLs

- **Home Page**: `http://127.0.0.1:8000/` - Beautiful landing page
- **Admin Panel**: `http://127.0.0.1:8000/admin/` - Django admin interface
- **Health Check**: `http://127.0.0.1:8000/health/` - API health endpoint

## 📊 Models Overview

### Users App
- **User**: Extended user model with email, phone, profile picture, bio
- **UserProfile**: Additional profile data with interests, preferences, subscription tiers

### AI Services App
- **AIService**: Available AI services (chat, image generation, text analysis)
- **Conversation**: User conversations with AI
- **Message**: Individual messages in conversations
- **UserServiceUsage**: Track user usage and token consumption

## 🔒 Security Features

- Custom user model with email authentication
- Environment-based configuration
- CSRF protection enabled
- Secure password validation
- Admin interface with proper permissions

## 🚀 Deployment

### Local Development
```bash
python manage.py runserver
```

### Production (Recommended)
1. Set `DEBUG=False` in `.env`
2. Configure MySQL database
3. Set up static file serving
4. Use Gunicorn or uWSGI
5. Configure reverse proxy (Nginx)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django Framework
- Python Community
- Modern web development practices

## 📞 Support

For support, email admin@sheconnect.ai or create an issue in this repository.

---

**Built with ❤️ using Django and Python**
