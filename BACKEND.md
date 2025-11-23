# 🔧 Backend Documentation - Vartalap

## Overview

The backend is built with **Django 3.2.12** and provides RESTful APIs for chat, video, room management, and user operations. All endpoints return JSON responses with consistent status fields.

## 📊 Technology Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | Django 3.2.12 |
| Language | Python 3.12 |
| Database | SQLite (Dev) / PostgreSQL (Prod) |
| API Style | REST with JSON |
| Authentication | Django User Model |
| Video SDK | Agora RTC |
| Token Gen | Agora Token Builder |

## 🏗️ Architecture

```
Request → URLs Router → Views → Models → Database
                ↓
         Serialization
                ↓
             JSON Response
```

### Request Flow

1. **URL Routing** (`base/urls.py`)
   - Routes incoming requests to appropriate views

2. **Views** (`base/views.py`)
   - Process business logic
   - Interact with database
   - Return JSON responses

3. **Models** (`base/models.py`)
   - Define database schema
   - Enforce constraints
   - Handle relationships

4. **Database**
   - Store and retrieve data
   - Maintain data integrity

## 🔌 API Endpoints

### Authentication

All endpoints use `@csrf_exempt` decorator for JSON requests.

```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_endpoint(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Process data
    return JsonResponse({'status': 'success', 'data': {...}})
```

### Base Response Format

All API responses follow this format:

```json
{
    "status": "success|error",
    "message": "Description",
    "data": {}
}
```

## 💬 Chat APIs

### 1. Get Room Messages

**Endpoint**: `GET /chat/messages/`

**Query Parameters**:
```
room_id (required): integer
```

**Request**:
```bash
GET /chat/messages/?room_id=1
```

**Response**:
```json
{
    "status": "success",
    "messages": [
        {
            "id": 1,
            "room": 1,
            "sender_name": "John Doe",
            "sender_uid": "user123",
            "message": "Hello everyone!",
            "created_at": "2025-11-23T14:30:00Z",
            "is_edited": false,
            "edited_at": null
        }
    ]
}
```

**Error**:
```json
{
    "status": "error",
    "message": "Room not found"
}
```

---

### 2. Send Message

**Endpoint**: `POST /chat/send/`

**Request Body**:
```json
{
    "room_id": 1,
    "sender_name": "John Doe",
    "sender_uid": "user123",
    "message": "Hello everyone!"
}
```

**Response**:
```json
{
    "status": "success",
    "message": "Message sent",
    "data": {
        "id": 1,
        "room_id": 1,
        "sender_name": "John Doe",
        "message": "Hello everyone!",
        "created_at": "2025-11-23T14:30:00Z"
    }
}
```

---

### 3. Edit Message

**Endpoint**: `POST /chat/edit/`

**Request Body**:
```json
{
    "message_id": 1,
    "new_message": "Updated message"
}
```

**Response**:
```json
{
    "status": "success",
    "message": "Message updated",
    "data": {
        "id": 1,
        "message": "Updated message",
        "is_edited": true,
        "edited_at": "2025-11-23T14:35:00Z"
    }
}
```

---

### 4. Delete Message

**Endpoint**: `POST /chat/delete/`

**Request Body**:
```json
{
    "message_id": 1
}
```

**Response**:
```json
{
    "status": "success",
    "message": "Message deleted"
}
```

---

## 🎥 Room APIs

### 1. Get All Rooms

**Endpoint**: `GET /rooms/`

**Response**:
```json
{
    "status": "success",
    "rooms": [
        {
            "id": 1,
            "name": "General Chat",
            "room_code": "ABC123",
            "share_link_id": "550e8400-e29b-41d4-a716-446655440000",
            "description": "General discussion room",
            "max_members": 10,
            "member_count": 3,
            "created_at": "2025-11-23T14:00:00Z",
            "share_link": "/join/550e8400-e29b-41d4-a716-446655440000/"
        }
    ]
}
```

---

### 2. Create Room

**Endpoint**: `POST /rooms/create/`

**Request Body**:
```json
{
    "name": "Project Discussion",
    "description": "For project team discussions",
    "max_members": 15
}
```

**Response**:
```json
{
    "status": "success",
    "message": "Room created",
    "data": {
        "id": 2,
        "name": "Project Discussion",
        "room_code": "XYZ789",
        "share_link_id": "new-uuid-here",
        "max_members": 15,
        "created_at": "2025-11-23T14:45:00Z"
    }
}
```

**Errors**:
```json
{
    "status": "error",
    "message": "Room name already exists"
}
```

---

### 3. Get Room by Share Link

**Endpoint**: `GET /rooms/<share_link_id>/`

**Response**:
```json
{
    "status": "success",
    "room": {
        "id": 1,
        "name": "General Chat",
        "room_code": "ABC123",
        "description": "General discussion room",
        "member_count": 3,
        "max_members": 10,
        "share_link": "/join/550e8400-e29b-41d4-a716-446655440000/"
    }
}
```

---

### 4. Add Room Member

**Endpoint**: `POST /rooms/members/add/`

**Request Body**:
```json
{
    "room_id": 1,
    "name": "John Doe",
    "uid": "user123"
}
```

**Response**:
```json
{
    "status": "success",
    "message": "Member added",
    "data": {
        "id": 1,
        "room_id": 1,
        "name": "John Doe",
        "uid": "user123",
        "joined_at": "2025-11-23T14:50:00Z"
    }
}
```

---

### 5. Get Room Members

**Endpoint**: `GET /rooms/members/?room_id=1`

**Response**:
```json
{
    "status": "success",
    "members": [
        {
            "id": 1,
            "name": "John Doe",
            "uid": "user123",
            "joined_at": "2025-11-23T14:50:00Z",
            "is_active": true
        }
    ]
}
```

---

## 👥 User APIs

### 1. Get All Users

**Endpoint**: `GET /users/`

**Response**:
```json
{
    "status": "success",
    "users": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false,
            "date_joined": "2025-11-23T10:00:00Z"
        }
    ]
}
```

---

### 2. Create User

**Endpoint**: `POST /users/create/`

**Request Body**:
```json
{
    "username": "jane_doe",
    "email": "jane@example.com",
    "password": "securepassword123"
}
```

**Response**:
```json
{
    "status": "success",
    "message": "User created",
    "data": {
        "id": 2,
        "username": "jane_doe",
        "email": "jane@example.com"
    }
}
```

---

### 3. Update User

**Endpoint**: `POST /users/update/`

**Request Body**:
```json
{
    "user_id": 1,
    "username": "john_updated",
    "email": "john.new@example.com"
}
```

**Response**:
```json
{
    "status": "success",
    "message": "User updated"
}
```

---

### 4. Delete User

**Endpoint**: `POST /users/delete/`

**Request Body**:
```json
{
    "user_id": 1
}
```

**Response**:
```json
{
    "status": "success",
    "message": "User deleted"
}
```

---

### 5. Change Password

**Endpoint**: `POST /users/change-password/`

**Request Body**:
```json
{
    "user_id": 1,
    "old_password": "currentpassword",
    "new_password": "newpassword123"
}
```

**Response**:
```json
{
    "status": "success",
    "message": "Password changed"
}
```

---

## 🎥 Video APIs

### Get Agora Token

**Endpoint**: `GET /get_token/?channel=ROOM_NAME`

**Query Parameters**:
```
channel (required): string - Room name
```

**Response**:
```json
{
    "token": "token_string_here",
    "uid": 123456
}
```

**Example**:
```bash
GET /get_token/?channel=general_chat
```

---

## 📊 Models Overview

### 1. Room Model

```python
class Room(models.Model):
    name = CharField(max_length=200, unique=True)
    room_code = CharField(max_length=20, unique=True, db_index=True)
    share_link_id = UUIDField(default=uuid4, unique=True)
    description = TextField(blank=True, null=True)
    max_members = IntegerField(default=10)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Indexes**:
- `room_code` (indexed for fast lookup)
- `share_link_id` (unique for URL routing)

---

### 2. RoomMember Model

```python
class RoomMember(models.Model):
    room = ForeignKey(Room, on_delete=CASCADE)
    name = CharField(max_length=200)
    uid = CharField(max_length=1000)
    joined_at = DateTimeField(auto_now_add=True)
    is_active = BooleanField(default=True)
    
    class Meta:
        unique_together = ('room', 'uid')
```

**Constraints**:
- Unique constraint on (room, uid) to prevent duplicate joins

---

### 3. ChatMessage Model

```python
class ChatMessage(models.Model):
    room = ForeignKey(Room, on_delete=CASCADE, related_name='messages')
    sender_name = CharField(max_length=200)
    sender_uid = CharField(max_length=1000)
    message = TextField()
    created_at = DateTimeField(auto_now_add=True, db_index=True)
    is_edited = BooleanField(default=False)
    edited_at = DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room', '-created_at'])
        ]
```

**Indexes**:
- Composite index on (room, -created_at) for efficient queries
- created_at indexed for sorting

---

## 🔐 Security Features

### CSRF Protection
All POST endpoints use `@csrf_exempt` for JSON APIs, but CSRF tokens are validated for form submissions.

### SQL Injection Prevention
- Django ORM prevents SQL injection automatically
- All queries use parameterized statements

### Input Validation
- Username uniqueness check
- Email validation
- Room name uniqueness
- Member limit enforcement

### Database Constraints
- Unique constraints on sensitive fields
- Foreign key constraints
- Check constraints on max_members

---

## 📈 Performance Optimization

### Indexing Strategy

**Primary Indexes**:
- `room.room_code` - Fast room lookup
- `chatmessage.created_at` - Efficient message sorting
- `chatmessage.room` - Filter messages by room

**Composite Indexes**:
- `(room_id, -created_at)` - Common query pattern for recent messages

### Query Optimization

```python
# Efficient - uses select_related
messages = ChatMessage.objects.select_related('room').filter(room_id=1)

# Avoid N+1 queries
rooms = Room.objects.prefetch_related('messages')
```

---

## 🚀 Deployment Configurations

### Environment Variables

```bash
# Security
SECRET_KEY=your-secure-key-here
DEBUG=False

# Database (PostgreSQL)
DB_HOST=db.example.com
DB_NAME=vartalap_db
DB_USER=postgres_user
DB_USER_PASSWORD=secure_password
DB_PORT=5432

# Allowed Hosts
ALLOWED_HOSTS=example.com,www.example.com

# Agora SDK
AGORA_APP_ID=your-agora-app-id
AGORA_CERTIFICATE=your-agora-certificate
```

### Production Checklist

- [ ] `SECRET_KEY` set to strong random value
- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` configured
- [ ] Database migrated to PostgreSQL
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] HTTPS enabled
- [ ] CORS configured if needed

---

## 🐛 Debugging

### Enable Debug Logging

```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Common Errors

**TemplateDoesNotExist**
- Check template path in `base/templates/base/`

**Room not found**
- Verify room_id exists in database
- Check share_link_id format (UUID)

**CSRF token missing**
- Ensure `@csrf_exempt` decorator on JSON endpoints

---

## 📝 Code Examples

### Creating a Room Programmatically

```python
from base.models import Room
import uuid

room = Room.objects.create(
    name="Meeting Room",
    room_code="MR001",
    share_link_id=uuid.uuid4(),
    description="For team meetings",
    max_members=20
)
```

### Fetching Messages

```python
from base.models import ChatMessage

# Get recent messages
messages = ChatMessage.objects.filter(
    room_id=1
).order_by('-created_at')[:50]

# Convert to dict
data = [
    {
        'id': m.id,
        'sender_name': m.sender_name,
        'message': m.message,
        'created_at': m.created_at.isoformat(),
    }
    for m in messages
]
```

---

## 🔗 Dependencies

See `requirements.txt`:
- **Django 3.2.12** - Web framework
- **Agora-token-builder** - Token generation
- **python-decouple** - Environment variables
- **dj-database-url** - Database URL parsing

---

**Last Updated**: November 23, 2025
