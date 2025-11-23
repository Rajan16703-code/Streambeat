from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

class Room(models.Model):
    """Room model with unique share link"""
    name = models.CharField(max_length=200, unique=True)
    room_code = models.CharField(max_length=10, unique=True, db_index=True)  # Unique code for sharing
    share_link_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4)  # For unique URLs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    max_members = models.IntegerField(default=10)
    
    def __str__(self):
        return f"{self.name} ({self.room_code})"
    
    class Meta:
        ordering = ['-created_at']


class RoomMember(models.Model):
    """Members in a room"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} in {self.room.name}"
    
    class Meta:
        unique_together = ['room', 'uid']
        ordering = ['-joined_at']


class ChatMessage(models.Model):
    """Real-time chat messages"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField(max_length=200)
    sender_uid = models.CharField(max_length=1000)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.sender_name}: {self.message[:50]}"
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room', '-created_at']),
        ]
