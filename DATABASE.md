# 💾 Database Documentation - Vartalap

## Overview

The Vartalap application uses a relational database with 4 main models. The database uses **SQLite for development** and **PostgreSQL for production**.

---

## 🗄️ Database Configuration

### Development (SQLite)

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**File**: `/workspaces/Streambeat/db.sqlite3`

### Production (PostgreSQL)

```python
# settings.py
if os.environ.get('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_USER_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
```

**Environment Variables**:
```bash
DB_HOST=your-postgres-host.com
DB_NAME=vartalap_db
DB_USER=postgres_user
DB_USER_PASSWORD=secure_password
DB_PORT=5432
```

---

## 📊 Data Models

### 1. User Model (Django Built-in)

**Description**: Represents application users with authentication

**Fields**:

| Field | Type | Constraints | Purpose |
|-------|------|-----------|---------|
| id | AutoField (PK) | Primary Key | Unique identifier |
| username | CharField(150) | Unique, Required | Login username |
| email | EmailField | Unique, Optional | User email |
| password | CharField | Hashed | Bcrypt hashed password |
| first_name | CharField(150) | Optional | User's first name |
| last_name | CharField(150) | Optional | User's last name |
| is_staff | BooleanField | Default: False | Admin access flag |
| is_active | BooleanField | Default: True | Account active status |
| is_superuser | BooleanField | Default: False | Superuser flag |
| date_joined | DateTimeField | Auto | Account creation time |
| last_login | DateTimeField | Optional | Last login time |

**SQL Schema**:
```sql
CREATE TABLE auth_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL
);

CREATE INDEX auth_user_username ON auth_user(username);
```

**Example Data**:
```json
{
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_superuser": true,
    "is_staff": true,
    "is_active": true,
    "date_joined": "2025-11-23T10:00:00Z"
}
```

---

### 2. Room Model

**Description**: Represents chat rooms where multiple users can communicate

**Location**: `base/models.py`

**Fields**:

| Field | Type | Constraints | Purpose |
|-------|------|-----------|---------|
| id | AutoField (PK) | Primary Key | Unique identifier |
| name | CharField(200) | Unique, Required, Indexed | Room display name |
| room_code | CharField(20) | Unique, Required, Indexed | Unique room code |
| share_link_id | UUIDField | Unique, Required | URL-safe share link |
| description | TextField | Optional | Room description |
| max_members | IntegerField | Default: 10 | Max user capacity |
| created_at | DateTimeField | Auto, Read-only | Creation timestamp |
| updated_at | DateTimeField | Auto | Last update timestamp |

**SQL Schema**:
```sql
CREATE TABLE base_room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL UNIQUE,
    room_code VARCHAR(20) NOT NULL UNIQUE,
    share_link_id CHAR(36) NOT NULL UNIQUE,
    description TEXT,
    max_members INTEGER DEFAULT 10 CHECK(max_members > 0),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE INDEX base_room_room_code ON base_room(room_code);
CREATE INDEX base_room_share_link_id ON base_room(share_link_id);
CREATE INDEX base_room_created_at ON base_room(created_at DESC);
```

**Indexes**:
- `room_code` - Fast lookup by code
- `share_link_id` - URL routing
- `created_at` - Sorting by date

**Example Data**:
```json
{
    "id": 1,
    "name": "General Chat",
    "room_code": "GEN001",
    "share_link_id": "550e8400-e29b-41d4-a716-446655440000",
    "description": "General discussion for all users",
    "max_members": 10,
    "created_at": "2025-11-23T14:00:00Z",
    "updated_at": "2025-11-23T14:30:00Z"
}
```

**Room Code Generation**:
```python
import random
import string

room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
# Example: 'A7K9M2'
```

---

### 3. RoomMember Model

**Description**: Tracks users who have joined a specific room

**Location**: `base/models.py`

**Fields**:

| Field | Type | Constraints | Purpose |
|-------|------|-----------|---------|
| id | AutoField (PK) | Primary Key | Unique identifier |
| room | ForeignKey | FK to Room, ON CASCADE | Room reference |
| name | CharField(200) | Required | Member display name |
| uid | CharField(1000) | Required | Unique user identifier |
| joined_at | DateTimeField | Auto, Read-only | Join timestamp |
| is_active | BooleanField | Default: True | Active status |

**Constraints**:
- **Unique Together**: (room, uid) - Prevents duplicate joins

**SQL Schema**:
```sql
CREATE TABLE base_roommember (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    uid VARCHAR(1000) NOT NULL,
    joined_at DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(room_id, uid),
    FOREIGN KEY (room_id) REFERENCES base_room(id) ON DELETE CASCADE
);

CREATE INDEX base_roommember_room_id ON base_roommember(room_id);
CREATE INDEX base_roommember_uid ON base_roommember(uid);
```

**Example Data**:
```json
{
    "id": 1,
    "room": 1,
    "name": "John Doe",
    "uid": "user123abc",
    "joined_at": "2025-11-23T14:15:00Z",
    "is_active": true
}
```

**Relationships**:
```
One Room → Many RoomMembers
One Member per (Room, UID) combination
```

---

### 4. ChatMessage Model

**Description**: Stores individual messages sent in a room

**Location**: `base/models.py`

**Fields**:

| Field | Type | Constraints | Purpose |
|-------|------|-----------|---------|
| id | AutoField (PK) | Primary Key | Unique identifier |
| room | ForeignKey | FK to Room, ON CASCADE | Room reference |
| sender_name | CharField(200) | Required | Display name of sender |
| sender_uid | CharField(1000) | Required | Unique sender ID |
| message | TextField | Required | Message content |
| created_at | DateTimeField | Auto, Read-only, Indexed | Message timestamp |
| is_edited | BooleanField | Default: False | Edit flag |
| edited_at | DateTimeField | Optional | Edit timestamp |

**Indexes**:
- Composite: (room_id, -created_at) DESC - Efficient message queries

**SQL Schema**:
```sql
CREATE TABLE base_chatmessage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    sender_name VARCHAR(200) NOT NULL,
    sender_uid VARCHAR(1000) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    is_edited BOOLEAN DEFAULT FALSE,
    edited_at DATETIME,
    FOREIGN KEY (room_id) REFERENCES base_room(id) ON DELETE CASCADE
);

CREATE INDEX base_chatmessage_room_created ON base_chatmessage(room_id, created_at DESC);
CREATE INDEX base_chatmessage_created_at ON base_chatmessage(created_at DESC);
CREATE INDEX base_chatmessage_room_id ON base_chatmessage(room_id);
```

**Example Data**:
```json
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
```

**Relationships**:
```
One Room → Many ChatMessages
Messages automatically deleted when room is deleted
```

---

## 🔗 Entity Relationship Diagram

```
┌─────────────────┐
│   auth_user     │
└────────┬────────┘
         │
         │ (1:N relationship via RoomMember.name)
         │
    ┌────▼────────────────┐
    │   base_room         │
    │ ─────────────────── │
    │ id (PK)             │
    │ name (UNIQUE)       │
    │ room_code (UNIQUE)  │
    │ share_link_id (FK)  │
    │ max_members         │
    └────┬────────────────┘
         │
         ├──────(1:N)──────────┐
         │                     │
    ┌────▼──────────────┐  ┌───▼────────────────┐
    │ base_roommember   │  │ base_chatmessage   │
    │ ──────────────── │  │ ──────────────────│
    │ id (PK)          │  │ id (PK)            │
    │ room_id (FK)     │  │ room_id (FK)       │
    │ name             │  │ sender_name        │
    │ uid              │  │ sender_uid         │
    │ joined_at        │  │ message            │
    │ is_active        │  │ created_at (INDEX) │
    └──────────────────┘  │ is_edited          │
                          │ edited_at          │
                          └────────────────────┘

Constraints:
- Room.name: UNIQUE
- Room.room_code: UNIQUE
- Room.share_link_id: UNIQUE
- RoomMember: UNIQUE(room_id, uid)
- ChatMessage.room_id: CASCADE ON DELETE
```

---

## 📈 Database Queries

### Common SELECT Queries

**Get All Rooms**:
```sql
SELECT id, name, room_code, share_link_id, 
       description, max_members, created_at
FROM base_room
ORDER BY created_at DESC;
```

**Get Recent Messages in Room**:
```sql
SELECT id, sender_name, sender_uid, message, 
       created_at, is_edited
FROM base_chatmessage
WHERE room_id = ?
ORDER BY created_at DESC
LIMIT 50;
```

**Get Room with Member Count**:
```sql
SELECT r.id, r.name, r.room_code,
       COUNT(rm.id) as member_count,
       r.max_members
FROM base_room r
LEFT JOIN base_roommember rm ON r.id = rm.room_id
WHERE r.id = ?
GROUP BY r.id;
```

**Get Active Members in Room**:
```sql
SELECT id, name, uid, joined_at
FROM base_roommember
WHERE room_id = ? AND is_active = TRUE
ORDER BY joined_at;
```

### INSERT/UPDATE/DELETE Examples

**Create Message**:
```sql
INSERT INTO base_chatmessage 
(room_id, sender_name, sender_uid, message, created_at)
VALUES (?, ?, ?, ?, datetime('now'));
```

**Update Message**:
```sql
UPDATE base_chatmessage
SET message = ?, is_edited = TRUE, edited_at = datetime('now')
WHERE id = ? AND sender_uid = ?;
```

**Delete Message**:
```sql
DELETE FROM base_chatmessage
WHERE id = ? AND sender_uid = ?;
```

**Add Room Member**:
```sql
INSERT INTO base_roommember 
(room_id, name, uid, joined_at, is_active)
VALUES (?, ?, ?, datetime('now'), TRUE)
ON CONFLICT(room_id, uid) DO UPDATE SET is_active = TRUE;
```

---

## 🔄 Database Migrations

### Migration Files

**Location**: `base/migrations/`

**0001_initial.py**: Initial schema
- Creates Room, RoomMember models
- Sets up indexes

**0002_auto_*.py**: ChatMessage addition
- Creates ChatMessage model
- Adds composite index on (room_id, -created_at)

### Running Migrations

```bash
# Create migrations for model changes
python manage.py makemigrations base

# Apply pending migrations
python manage.py migrate

# View migration history
python manage.py showmigrations

# Rollback specific migration
python manage.py migrate base 0001
```

### Creating Custom Migration

```bash
# Create empty migration
python manage.py makemigrations base --empty --name add_new_field

# Edit migration file and add operations
```

---

## 🔍 Database Optimization

### Index Strategy

**Primary Indexes** (for fast lookups):
- `room.room_code` - Lookup by code
- `room.share_link_id` - URL routing
- `chatmessage.created_at` - Time-based sorting

**Foreign Key Indexes** (auto-created):
- `roommember.room_id` - Filter by room
- `chatmessage.room_id` - Filter by room

**Composite Indexes** (common patterns):
- `(room_id, -created_at)` - Get recent room messages

### Query Performance

**Efficient**:
```python
# Single query with select_related
messages = ChatMessage.objects.select_related('room').filter(room_id=1)

# Bulk operations
ChatMessage.objects.bulk_create([msg1, msg2, msg3])
```

**Inefficient** (N+1 problem):
```python
# Don't use in loops!
for room in rooms:
    messages = ChatMessage.objects.filter(room_id=room.id)
```

---

## 🔐 Data Integrity

### Constraints

**Unique Constraints**:
```sql
UNIQUE(room.name)           -- One room per name
UNIQUE(room.room_code)      -- One code per room
UNIQUE(room.share_link_id)  -- One share link
UNIQUE(roommember.room_id, roommember.uid)  -- Prevent duplicate joins
```

**Foreign Key Constraints**:
```sql
FOREIGN KEY(roommember.room_id) REFERENCES room(id) ON DELETE CASCADE
FOREIGN KEY(chatmessage.room_id) REFERENCES room(id) ON DELETE CASCADE
```

**Check Constraints**:
```sql
CHECK(room.max_members > 0)  -- Positive capacity
```

### Cascade Behavior

When a room is deleted:
- ✅ All RoomMembers are deleted
- ✅ All ChatMessages are deleted
- ✅ Automatic cleanup (ON DELETE CASCADE)

---

## 📊 Database Statistics

### Table Sizes (Typical)

```
Room Table:         ~1KB per 100 rooms
RoomMember Table:   ~2KB per 1000 members
ChatMessage Table:  ~3KB per 1000 messages
Auth_User Table:    ~5KB per 1000 users
```

### Growth Projections

```
10 Rooms:           10KB
100 Users:          50KB
10,000 Messages:    30KB
Total (1000 active): ~100KB
```

---

## 🚀 Backup & Recovery

### Backup SQLite

```bash
# Copy database file
cp db.sqlite3 db.sqlite3.backup

# Or use Django management command
python manage.py dumpdata > backup.json
```

### Restore from Backup

```bash
# From JSON backup
python manage.py loaddata backup.json

# From SQLite backup
cp db.sqlite3.backup db.sqlite3
```

### PostgreSQL Backup (Production)

```bash
# Backup database
pg_dump -U username -d database_name > backup.sql

# Restore database
psql -U username -d database_name < backup.sql
```

---

## 🔍 Database Monitoring

### Check Table Sizes

```bash
# SQLite
sqlite3 db.sqlite3 "SELECT name, COUNT(*) FROM sqlite_master GROUP BY type;"

# PostgreSQL
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Monitor Connections

```bash
# PostgreSQL active connections
SELECT count(*) FROM pg_stat_activity;
```

---

**Last Updated**: November 23, 2025
