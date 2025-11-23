# 🎨 Frontend Documentation - Vartalap

## Overview

The frontend is built with **Vanilla JavaScript (ES6+)**, **HTML5**, and **CSS3**. It provides a modern, responsive user interface for real-time chat and video conferencing.

## 🏗️ Architecture

```
User Actions → Event Listeners → API Calls → DOM Updates → Real-time Display
```

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Vanilla JavaScript (ES6+) |
| Styling | CSS3 with CSS Grid/Flexbox |
| DOM | HTML5 with Django Templates |
| Real-time | Fetch API with Polling (2s) |
| Video | Agora RTC SDK v4.20.2 |
| Icons | Unicode Emojis |
| Responsive | Mobile-first design |

---

## 📁 File Structure

```
static/
├── js/
│   ├── main.js              # Main JavaScript (legacy video code)
│   └── streams.js           # Agora stream handling
├── styles/
│   └── main.css             # Global styles
├── assets/
│   └── AgoraRTC_N-*.js      # Agora SDK library
└── images/
    └── (SVG icons)

templates/base/
├── main.html                # Base template with navbar
├── lobby.html               # Homepage with features
├── room.html                # Video conferencing page
├── chat_room.html           # Real-time chat interface
├── room_management.html     # Room CRUD UI
├── user_management.html     # User CRUD UI
└── join_room.html           # Join room via share link
```

---

## 🎨 Design System

### Color Palette

```css
:root {
    --primary: #6366f1;          /* Indigo */
    --primary-dark: #4f46e5;     /* Dark Indigo */
    --secondary: #ec4899;        /* Pink */
    --success: #10b981;          /* Green */
    --danger: #ef4444;           /* Red */
    --warning: #f59e0b;          /* Amber */
    --dark: #1f2937;             /* Dark Gray */
    --light: #f9fafb;            /* Light Gray */
    --border: #e5e7eb;           /* Border Gray */
}
```

### Typography

```css
Body Font: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto'
Font Sizes:
  - h1: 32px-48px (headings)
  - h2: 18px-28px (section titles)
  - Body: 14px-16px
  - Small: 12px-13px
```

### Spacing

```css
8px   - xs (margins, padding)
12px  - sm
16px  - md
20px  - lg
24px  - xl
32px  - 2xl
40px  - 3xl
```

---

## 🧩 Key Components

### 1. Navbar Component

**File**: `base/templates/base/main.html`

**Features**:
- Sticky positioning (top: 0, z-index: 1000)
- Brand logo with hover effect
- Dropdown menus for Chat, Video, Users
- "+ New Chat" CTA button
- Mobile hamburger menu
- Auto-close on outside click

**HTML Structure**:
```html
<nav class="navbar">
    <div class="navbar-container">
        <a href="/" class="navbar-brand">💬 Vartalap</a>
        <ul class="nav-menu">
            <!-- Menu items -->
        </ul>
    </div>
</nav>
```

**Key JavaScript**:
```javascript
function toggleMenu() {
    const menu = document.querySelector('.nav-menu');
    menu.classList.toggle('active');
}

document.addEventListener('click', function(e) {
    const navbar = document.querySelector('.navbar');
    if (!navbar.contains(e.target)) {
        menu.classList.remove('active');
    }
});
```

---

### 2. Chat Room Component

**File**: `base/templates/base/chat_room.html`

**Features**:
- Real-time message display
- Message polling every 2 seconds
- Gradient message bubbles
- Sender name and timestamp
- Smooth scroll to latest message
- Shared room link display
- Responsive layout

**State Management**:
```javascript
// User state in localStorage
localStorage.getItem('currentUserName')
localStorage.getItem('currentUserId')
localStorage.setItem('currentUserName', name)
localStorage.setItem('currentUserId', id)
```

**Message Display**:
```javascript
function displayMessages(messages) {
    const container = document.getElementById('messagesContainer');
    
    container.innerHTML = messages.map(msg => {
        const isOwn = msg.sender_uid === currentUserId;
        return `
            <div class="message ${isOwn ? 'own' : ''}">
                <div class="message-bubble">
                    ${!isOwn ? `<div class="message-sender">${msg.sender_name}</div>` : ''}
                    <div>${msg.message}</div>
                    <div class="message-time">${msgTime}</div>
                </div>
            </div>
        `;
    }).join('');
    
    container.scrollTop = container.scrollHeight;
}
```

**Real-time Polling**:
```javascript
// Poll every 2 seconds
setInterval(loadMessages, 2000);

function loadMessages() {
    fetch(`/chat/messages/?room_id=${currentRoomId}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                displayMessages(data.messages);
            }
        });
}
```

---

### 3. Room Management Component

**File**: `base/templates/base/room_management.html`

**Features**:
- Create new chat rooms
- Display room cards in grid
- Copy share link button
- Delete room functionality
- Search/filter rooms
- Member count display

**Form Handling**:
```javascript
document.getElementById('createRoomForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('roomName').value,
        description: document.getElementById('roomDesc').value,
        max_members: parseInt(document.getElementById('maxMembers').value)
    };

    fetch('/rooms/create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            alert('✅ Room created!');
            loadRooms();
        }
    });
});
```

**Room Cards Grid**:
```css
.rooms-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 24px;
}

.room-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    transition: all 0.3s;
}

.room-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
```

---

### 4. User Management Component

**File**: `base/templates/base/user_management.html`

**Features**:
- Create, edit, delete users
- Search users table
- Role badges (Superuser, Staff, Active/Inactive)
- Password change form
- Real-time user list

**Table Rendering**:
```javascript
function loadUsers() {
    fetch('/users/')
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                displayUsersTable(data.users);
            }
        });
}

function displayUsersTable(users) {
    const table = document.getElementById('usersTable');
    table.innerHTML = users.map(user => `
        <tr>
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td>
                ${user.is_superuser ? '<span class="badge badge-admin">👑 Admin</span>' : ''}
                ${user.is_active ? '<span class="badge badge-active">✓ Active</span>' : ''}
            </td>
            <td>
                <button onclick="editUser(${user.id})">Edit</button>
                <button onclick="deleteUser(${user.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}
```

---

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile First */
@media (max-width: 640px) {
    /* Small phones */
}

@media (max-width: 768px) {
    /* Tablets & large phones */
}

@media (max-width: 1024px) {
    /* Small desktops */
}

@media (min-width: 1200px) {
    /* Large desktops */
}
```

### Mobile-Specific Changes

**Navbar on Mobile**:
```css
@media (max-width: 768px) {
    .nav-menu {
        position: absolute;
        top: 64px;
        left: 0;
        width: 100%;
        flex-direction: column;
    }
    
    .hamburger {
        display: flex;  /* Show hamburger */
    }
}
```

**Chat Layout on Mobile**:
```css
@media (max-width: 768px) {
    .chat-wrapper {
        flex-direction: column;  /* Stack vertically */
    }
    
    .chat-sidebar {
        height: 120px;  /* Reduce sidebar height */
    }
    
    .message-bubble {
        max-width: 85%;  /* Wider messages */
    }
}
```

---

## 🎬 Video Component

**File**: `base/templates/base/room.html`

**Features**:
- Agora RTC SDK integration
- HD video streaming
- Screen sharing support
- Mute/unmute audio
- Mute/unmute video
- Leave room button

**Initialization**:
```javascript
// Agora setup
const APP_ID = "469fbdf3aafd4991b7ef2b24c3b21c04";
let rtc = {
    local: {
        id: Math.floor(Math.random() * 100000),
        mediaStream: undefined,
        audioTrack: undefined,
        videoTrack: undefined,
    },
    remote: {},
};

// Get token and join channel
async function joinChannel(channelName, userName) {
    const response = await fetch(`/get_token/?channel=${channelName}`);
    const data = await response.json();
    
    rtc.client.uid = data.uid;
    await rtc.client.join(APP_ID, channelName, data.token, data.uid);
}
```

---

## 🔄 API Communication

### Fetch Pattern

All API calls use this standardized pattern:

```javascript
fetch('/endpoint/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
})
.then(res => {
    if (!res.ok) throw new Error('Network response failed');
    return res.json();
})
.then(data => {
    if (data.status === 'success') {
        // Handle success
        console.log(data.data);
    } else {
        // Handle error
        console.error(data.message);
    }
})
.catch(error => {
    console.error('Error:', error);
    alert('❌ An error occurred');
});
```

### Request Examples

**Get Messages**:
```javascript
fetch(`/chat/messages/?room_id=${roomId}`)
    .then(res => res.json())
    .then(data => console.log(data.messages));
```

**Send Message**:
```javascript
fetch('/chat/send/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        room_id: roomId,
        sender_name: userName,
        sender_uid: userId,
        message: messageText
    })
});
```

**Create Room**:
```javascript
fetch('/rooms/create/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'Room Name',
        description: 'Description',
        max_members: 10
    })
});
```

---

## 🎨 CSS Organization

### Layout Patterns

**CSS Grid Layout**:
```css
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 32px;
}
```

**Flexbox Layout**:
```css
.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
```

**Two-Column Layout**:
```css
.main-grid {
    display: grid;
    grid-template-columns: 350px 1fr;  /* Fixed sidebar + flexible content */
    gap: 32px;
}
```

### Animations

**Slide Down**:
```css
@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.dropdown-content {
    animation: slideDown 0.2s ease;
}
```

**Fade In**:
```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

**Scale on Hover**:
```css
.btn:hover {
    transform: scale(1.05);
}
```

---

## ♿ Accessibility

### Semantic HTML

```html
<nav class="navbar">           <!-- Navigation -->
<main class="container">       <!-- Main content -->
<header class="hero">          <!-- Hero section -->
<section class="features">     <!-- Feature section -->
<footer class="footer">        <!-- Footer -->
```

### ARIA Labels

```html
<button aria-label="Toggle menu">☰</button>
<div role="alert">Error message</div>
<img alt="Description" src="image.jpg">
```

### Keyboard Navigation

```javascript
// Listen for Enter key
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        sendMessage();
    }
});
```

---

## 🔒 Security Considerations

### XSS Prevention

Always escape user input:
```javascript
// ❌ DON'T - Can cause XSS
element.innerHTML = userInput;

// ✅ DO - Safe
element.textContent = userInput;
```

### LocalStorage Security

```javascript
// User data stored locally (no sensitive data)
localStorage.setItem('currentUserName', userName);
localStorage.setItem('currentUserId', userId);

// Generate random IDs on first visit
if (!userId) {
    userId = Math.random().toString(36).substr(2, 9);
    localStorage.setItem('currentUserId', userId);
}
```

---

## 🚀 Performance Tips

### Lazy Loading

```javascript
// Load data only when needed
if (chatVisible) {
    loadMessages();
}
```

### Event Delegation

```javascript
// Efficient - single listener
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('delete-btn')) {
        deleteItem(e.target.dataset.id);
    }
});
```

### Debouncing Search

```javascript
let searchTimeout;
searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        searchUsers(e.target.value);
    }, 300);
});
```

---

## 📊 Component State Management

### Centralized State

```javascript
// Global app state
const appState = {
    currentUser: {
        id: null,
        name: null
    },
    currentRoom: {
        id: null,
        code: null
    },
    messages: [],
    users: [],
    rooms: []
};

// Update state
function updateState(key, value) {
    appState[key] = value;
    renderUI();
}
```

---

## 🔧 Developer Tools

### Browser DevTools Console

```javascript
// Check current state
console.log(appState);

// Debug API calls
fetch('/rooms/')
    .then(r => r.json())
    .then(d => console.table(d.rooms));

// Test localStorage
localStorage.getItem('currentUserId');
```

---

**Last Updated**: November 23, 2025
