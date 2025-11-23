# 🤝 Contributing to Vartalap

Thank you for your interest in contributing to Vartalap! This guide will help you understand our development process and how you can help make this project better.

---

## 🎯 Before You Start

1. **Read the Code of Conduct**: [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
2. **Review Project Docs**: Check [README.md](./README.md), [BACKEND.md](./BACKEND.md), [FRONTEND.md](./FRONTEND.md), [DATABASE.md](./DATABASE.md)
3. **Check Existing Issues**: Don't duplicate work

---

## 🏗️ Development Setup

### 1. Fork & Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Vartalap.git
cd Vartalap
git remote add upstream https://github.com/Ajoe62/Vartalap.git
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

```bash
# Create .env file
echo "SECRET_KEY=dev-key-for-testing" > .env
echo "DEBUG=True" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
```

### 5. Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # admin / admin123
```

### 6. Run Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Visit: http://localhost:8000

---

## 🌿 Workflow

### 1. Create Feature Branch

```bash
# Update main branch
git fetch upstream
git checkout upstream/master

# Create feature branch
git checkout -b feature/amazing-feature
```

**Branch Naming**:
- `feature/feature-name` - New features
- `fix/bug-name` - Bug fixes
- `docs/doc-name` - Documentation
- `refactor/refactor-name` - Code refactoring

### 2. Make Changes

```bash
# Edit files
nano file.py

# Test changes
python manage.py test

# Check code quality
python -m flake8 base/
```

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add real-time chat notifications

- Add notification API endpoint
- Update frontend to show notifications
- Add tests for notification system

Closes #123"
```

**Commit Message Format**:
```
type: short description (50 chars max)

longer description explaining the changes
and why they were made

- Bullet point 1
- Bullet point 2

Closes #issue_number
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style (formatting)
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Build tools, dependencies

### 4. Push & Create Pull Request

```bash
# Push to your fork
git push origin feature/amazing-feature

# Create PR on GitHub
# Fill in PR template with:
# - What does this PR do?
# - Why is it needed?
# - Testing done
# - Screenshots (if UI change)
```

**PR Template**:
```markdown
## Description
Brief description of changes

## Related Issue
Closes #123

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Code refactoring

## Testing Done
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] No breaking changes

## Screenshots (if applicable)
[Add images here]

## Checklist
- [ ] Code follows project style
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings
```

### 5. Code Review

- Address reviewer feedback
- Push updates to same branch
- Maintainer will merge when approved

---

## 📝 Code Standards

### Python Code Style

We follow **PEP 8** with these tools:

```bash
# Format code
python -m black base/

# Lint code
python -m flake8 base/

# Type checking
python -m mypy base/
```

**Guidelines**:
```python
# ✅ Good
def calculate_total(items: list) -> float:
    """Calculate total price of items."""
    return sum(item.price for item in items)

# ❌ Bad
def calc(x):
    return sum([i.p for i in x])
```

### JavaScript Code Style

We follow **ES6+ standards**:

```javascript
// ✅ Good
const fetchMessages = async (roomId) => {
    try {
        const response = await fetch(`/chat/messages/?room_id=${roomId}`);
        const data = await response.json();
        displayMessages(data.messages);
    } catch (error) {
        console.error('Failed to fetch messages:', error);
    }
};

// ❌ Bad
function fetch_messages(room_id){
var data = fetch('/chat/messages/?room_id='+room_id);
console.log(data);
}
```

### HTML/CSS Guidelines

```html
<!-- ✅ Good -->
<div class="chat-container">
    <header class="chat-header">
        <h2>Room Name</h2>
    </header>
    <div class="messages-container">
        <!-- Content -->
    </div>
</div>

<!-- ❌ Bad -->
<div style="width:100%">
    <h1 style="color:blue">Room Name</h1>
    <div style="overflow:auto">
        <!-- Content -->
    </div>
</div>
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test base.tests.ChatMessageTest

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests

```python
from django.test import TestCase
from base.models import Room, ChatMessage

class ChatMessageTest(TestCase):
    def setUp(self):
        """Create test data"""
        self.room = Room.objects.create(
            name="Test Room",
            room_code="TEST01"
        )
    
    def test_message_creation(self):
        """Test creating a message"""
        message = ChatMessage.objects.create(
            room=self.room,
            sender_name="Test User",
            sender_uid="test123",
            message="Hello"
        )
        self.assertEqual(message.sender_name, "Test User")
        self.assertFalse(message.is_edited)
    
    def test_message_editing(self):
        """Test editing a message"""
        message = ChatMessage.objects.create(
            room=self.room,
            sender_name="Test User",
            sender_uid="test123",
            message="Original"
        )
        message.message = "Edited"
        message.is_edited = True
        message.save()
        
        updated = ChatMessage.objects.get(id=message.id)
        self.assertEqual(updated.message, "Edited")
        self.assertTrue(updated.is_edited)
```

---

## 📚 Documentation

### Docstrings

```python
# Function docstring
def send_message(room_id: int, sender_uid: str, message: str) -> dict:
    """
    Send a message to a room.
    
    Args:
        room_id: ID of the room
        sender_uid: Unique ID of sender
        message: Message content
    
    Returns:
        dict: Response with status and message data
    
    Raises:
        Room.DoesNotExist: If room not found
        ValueError: If message is empty
    
    Example:
        >>> send_message(1, "user123", "Hello")
        {'status': 'success', 'data': {...}}
    """
    # Implementation
```

### README Updates

If adding a feature, update relevant documentation:
- [README.md](./README.md) - Features section
- [BACKEND.md](./BACKEND.md) - API endpoints
- [FRONTEND.md](./FRONTEND.md) - UI components
- [DATABASE.md](./DATABASE.md) - Models

---

## 🐛 Reporting Issues

### Issue Template

```markdown
## Description
Clear and concise description of the issue

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Environment
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 96]
- Python version: [e.g., 3.9]

## Screenshots
[If applicable]

## Additional Context
[Any other context]
```

---

## 🎉 Suggestion Guidelines

Have a great idea? Share it!

1. **Open a Discussion**: Use GitHub Discussions for ideas
2. **Search First**: Check if someone already suggested it
3. **Be Specific**: Explain what and why
4. **Provide Examples**: Show use cases

---

## 📋 Checklist Before Submitting PR

- [ ] Code follows project style guidelines
- [ ] Self-reviewed code for obvious errors
- [ ] Added/updated documentation
- [ ] Added tests for new features
- [ ] Tests pass locally (`python manage.py test`)
- [ ] No unnecessary console logs left
- [ ] Branch is up-to-date with master
- [ ] Commits are squashed if appropriate
- [ ] PR description is clear and complete

---

## 🚀 What We're Looking For

### High Priority
- 🎯 Real-time chat improvements
- 🎥 Video conferencing enhancements
- 🔒 Security improvements
- 🐛 Bug fixes
- 📱 Mobile optimization

### Medium Priority
- ✨ UI/UX improvements
- 📚 Documentation
- 🧪 Tests
- ⚡ Performance optimization

### Good for Beginners
- 📝 Documentation improvements
- 🎨 CSS/UI enhancements
- 🧪 Writing tests
- 🔍 Code cleanup

---

## 💡 Tips for Success

### Before Starting Work
1. Comment on issue expressing interest
2. Wait for maintainer approval
3. Discuss approach if complex
4. Check if anyone is already working

### While Working
1. Commit frequently with good messages
2. Push to keep others updated
3. Keep PRs focused and small
4. Test thoroughly before submitting

### Code Review Tips
1. Respond promptly to feedback
2. Ask for clarification if confused
3. Explain your reasoning
4. Accept criticism gracefully

---

## 🏆 Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](./CONTRIBUTORS.md)
- GitHub contributors page
- Monthly contributor highlights

---

## 📞 Need Help?

- **Questions?** Open a GitHub Discussion
- **Issue?** [Open a bug report](https://github.com/Ajoe62/Vartalap/issues)
- **Code Review?** Ask in the PR comments
- **Email**: ajoe62@example.com

---

## 🙏 Thank You!

Your contributions make Vartalap better for everyone. We truly appreciate your time and effort!

**Happy contributing! 🎉**

---

Last Updated: November 23, 2025
