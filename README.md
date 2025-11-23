# 💬 Vartalap - Real-time Chat & Video Conferencing Platform

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Django](https://img.shields.io/badge/Django-3.2.12-darkgreen)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

A modern, real-time chat and video conferencing application built with Django, JavaScript, and Agora SDK. Connect with users instantly through shared chat rooms and video calls.

## 🎯 Overview

**Vartalap** (वर्तालाप - meaning "Conversation" in Hindi) is a web-based communication platform that enables:
- 💬 Real-time text messaging
- 🎥 HD video conferencing
- 🔗 Shareable chat room links
- 👥 User management system
- 📱 Mobile-responsive design
- 🔒 Secure room-based communication

## 🚀 Features

### Chat System
- ✅ Real-time message synchronization (2-second polling)
- ✅ Shareable room links for easy access
- ✅ Message timestamps and sender identification
- ✅ Support for unlimited messages per room
- ✅ Room capacity management

### Video Conferencing
- ✅ HD video calls via Agora SDK
- ✅ Multi-user support (up to 10 users per room)
- ✅ Automatic token generation
- ✅ Screen sharing ready

### Room Management
- ✅ Create custom chat rooms
- ✅ Room code generation
- ✅ Member limit configuration
- ✅ Room description
- ✅ Share links via UUID

### User Management
- ✅ User CRUD operations
- ✅ Admin panel access
- ✅ Password management
- ✅ User role management
- ✅ Superuser support

## 📊 Tech Stack

### Backend
- **Framework**: Django 3.2.12 (Python Web Framework)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **API**: REST API with JSON responses
- **Token Generation**: Agora Token Builder
- **Authentication**: Django Built-in User Model

### Frontend
- **Language**: Vanilla JavaScript (ES6+)
- **Styling**: CSS3 with responsive design
- **Icons**: Unicode emojis
- **Real-time**: Fetch API with polling
- **Video SDK**: Agora RTC SDK (v4.20.2)

### Deployment
- **Server**: Django Development Server / Gunicorn
- **Hosting**: Vercel / Render / Local
- **Database**: PostgreSQL on cloud
- **Static Files**: CloudFront / Vercel

## 📁 Project Structure

```
Vartalap/
├── base/                           # Main Django app
│   ├── migrations/                 # Database migrations
│   │   ├── 0001_initial.py
│   │   └── 0002_auto_*.py
│   ├── templates/base/             # HTML templates
│   │   ├── main.html              # Base navbar template
│   │   ├── lobby.html             # Homepage
│   │   ├── room.html              # Video room
│   │   ├── chat_room.html         # Chat interface
│   │   ├── room_management.html   # Room CRUD UI
│   │   ├── user_management.html   # User CRUD UI
│   │   └── join_room.html         # Join room page
│   ├── models.py                  # Database models
│   ├── views.py                   # API views & logic
│   ├── urls.py                    # URL routing
│   ├── admin.py                   # Admin configuration
│   └── apps.py                    # App configuration
│
├── mychat/                         # Django project settings
│   ├── settings.py                # Configuration
│   ├── urls.py                    # Main URL router
│   ├── wsgi.py                    # WSGI config
│   └── asgi.py                    # ASGI config
│
├── static/                         # Static files
│   ├── assets/                    # JavaScript libraries
│   │   └── AgoraRTC_N-*.js
│   ├── images/                    # Icons & images
│   ├── js/                        # Custom JavaScript
│   │   ├── main.js
│   │   └── streams.js
│   └── styles/                    # CSS files
│       └── main.css
│
├── manage.py                       # Django management
├── requirements.txt               # Python dependencies
├── db.sqlite3                     # Development database
├── README.md                      # This file
├── BACKEND.md                     # Backend documentation
├── FRONTEND.md                    # Frontend documentation
├── DATABASE.md                    # Database schema
├── CODE_OF_CONDUCT.md            # Code of conduct
└── CONTRIBUTING.md               # Contributing guide
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git
- Modern web browser

### Backend Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/Ajoe62/Vartalap.git
   cd Vartalap
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "DEBUG=True" >> .env
   echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
   ```

5. **Database Migration**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   # Username: admin
   # Password: admin123
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

   Server will be available at: `http://localhost:8000`

### Frontend Setup

The frontend is fully integrated with Django templates. No separate build process needed!

## 🔐 Admin Access

- **URL**: `http://localhost:8000/admin/`
- **Username**: admin
- **Password**: admin123

## 📱 Main Routes

| Route | Purpose | Method |
|-------|---------|--------|
| `/` | Homepage | GET |
| `/room/` | Video room | GET |
| `/manage-rooms/` | Room management | GET |
| `/chat/room/<id>/` | Chat interface | GET |
| `/manage-users/` | User management | GET |
| `/join/<share_link_id>/` | Join room via link | GET |

## 🔌 API Endpoints

### Chat APIs
- `GET /chat/messages/` - Fetch room messages
- `POST /chat/send/` - Send message
- `POST /chat/edit/` - Edit message
- `POST /chat/delete/` - Delete message

### Room APIs
- `GET /rooms/` - List all rooms
- `POST /rooms/create/` - Create room
- `GET /rooms/<share_link_id>/` - Get room details
- `POST /rooms/members/add/` - Add member
- `GET /rooms/members/` - Get room members

### User APIs
- `GET /users/` - List users
- `POST /users/create/` - Create user
- `POST /users/update/` - Update user
- `POST /users/delete/` - Delete user
- `POST /users/change-password/` - Change password

### Video APIs
- `GET /get_token/` - Generate Agora token

For detailed API documentation, see [BACKEND.md](./BACKEND.md)

## 💾 Database Models

The application uses 3 main database models:

1. **User** (Django Built-in)
   - username, email, password
   - is_staff, is_superuser, is_active

2. **Room**
   - name, room_code, share_link_id
   - description, max_members
   - created_at, updated_at

3. **RoomMember**
   - room (FK), name, uid
   - joined_at, is_active

4. **ChatMessage**
   - room (FK), sender_name, sender_uid
   - message, created_at
   - is_edited, edited_at

For detailed schema, see [DATABASE.md](./DATABASE.md)

## 🎨 Frontend Architecture

The frontend uses a **component-based approach** with:
- Responsive CSS Grid layouts
- Real-time message polling (2-second intervals)
- Local storage for user persistence
- Dynamic form validation
- Smooth animations

See [FRONTEND.md](./FRONTEND.md) for detailed UI documentation.

## 🚀 Deployment

### For Vercel
```bash
vercel --prod
```

### For Render
1. Connect GitHub repository
2. Set environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`
   - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_USER_PASSWORD`

3. Deploy

### For Local Gunicorn
```bash
gunicorn mychat.wsgi:application --bind 0.0.0.0:8000
```

## 📦 Dependencies

See [requirements.txt](./requirements.txt) for complete list:
- Django 3.2.12
- Agora-token-builder
- python-decouple
- dj-database-url

## 🤝 Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before contributing.

### Quick Start
1. Fork repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Rajan Yadav** ([@Ajoe62](https://github.com/Ajoe62))

## 🙏 Acknowledgments

- Agora.io for real-time communication SDK
- Django community for the excellent framework
- Contributors and testers

## 📞 Support

For issues, questions, or suggestions:
1. Open a GitHub Issue
2. Check existing documentation
3. Contact: your-email@example.com

## 🗺️ Roadmap

- [ ] Socket.io integration for true real-time chat
- [ ] Message search functionality
- [ ] User avatars and profiles
- [ ] Message reactions (emoji)
- [ ] File sharing
- [ ] End-to-end encryption
- [ ] Dark mode
- [ ] Mobile app (React Native)

---

**Made with ❤️ for seamless communication**

Last Updated: November 23, 2025
