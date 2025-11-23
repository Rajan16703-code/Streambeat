from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember, ChatMessage, Room
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone



# Create your views here.

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = "469fbdf3aafd4991b7ef2b24c3b21c04"
    appCertificate = "c0e02daffb9a438f8d74f5d79b5d2fd9"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    try:
        # Get or create room by room_code or room_name
        room_identifier = data.get('room_name') or data.get('room_code')
        room = Room.objects.get(room_code=room_identifier)
        
        member, created = RoomMember.objects.get_or_create(
            room=room,
            uid=data['UID'],
            defaults={'name': data['name'], 'is_active': True}
        )
        
        return JsonResponse({'name': data['name'], 'status': 'success'}, safe=False)
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400, safe=False)


def getMember(request):
    try:
        uid = request.GET.get('UID')
        room_code = request.GET.get('room_name') or request.GET.get('room_code')
        
        room = Room.objects.get(room_code=room_code)
        member = RoomMember.objects.get(
            uid=uid,
            room=room
        )
        return JsonResponse({'name': member.name, 'status': 'success'}, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    try:
        room_identifier = data.get('room_name') or data.get('room_code')
        room = Room.objects.get(room_code=room_identifier)
        
        member = RoomMember.objects.get(
            uid=data['UID'],
            room=room
        )
        member.delete()
        return JsonResponse({'status': 'success', 'message': 'Member deleted'}, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400, safe=False)


# ==================== USER MANAGEMENT API ====================

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Get all users
@csrf_exempt
def get_users(request):
    """API: Get all users"""
    try:
        users = User.objects.all().values('id', 'username', 'email', 'is_staff', 'is_active', 'is_superuser', 'date_joined')
        return JsonResponse({'status': 'success', 'users': list(users)}, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Create new user
@csrf_exempt
def create_user(request):
    """API: Create new user"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if not username or not password:
            return JsonResponse({'status': 'error', 'message': 'Username and password required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Update user
@csrf_exempt
def update_user(request):
    """API: Update user details"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User ID required'}, status=400)
        
        user = User.objects.get(id=user_id)
        
        # Update fields if provided
        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'is_staff' in data:
            user.is_staff = data['is_staff']
        if 'is_superuser' in data:
            user.is_superuser = data['is_superuser']
        
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser
            }
        })
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Delete user
@csrf_exempt
def delete_user(request):
    """API: Delete user"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        if not user_id:
            return JsonResponse({'status': 'error', 'message': 'User ID required'}, status=400)
        
        user = User.objects.get(id=user_id)
        username = user.username
        user.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'User {username} deleted successfully'
        })
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Change password
@csrf_exempt
def change_password(request):
    """API: Change user password"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not all([user_id, old_password, new_password]):
            return JsonResponse({'status': 'error', 'message': 'All fields required'}, status=400)
        
        user = User.objects.get(id=user_id)
        
        if not user.check_password(old_password):
            return JsonResponse({'status': 'error', 'message': 'Old password is incorrect'}, status=400)
        
        user.set_password(new_password)
        user.save()
        
        return JsonResponse({'status': 'success', 'message': 'Password changed successfully'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# User management page
def user_management(request):
    """Render user management UI"""
    return render(request, 'base/user_management.html')


# ==================== ROOM MANAGEMENT & SHARING ====================

from .models import Room
import string

def generate_room_code():
    """Generate a unique 6-character room code"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Room.objects.filter(room_code=code).exists():
            return code


# Create a new room
@csrf_exempt
def create_room(request):
    """API: Create a new room with unique share link"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        room_name = data.get('name')
        description = data.get('description', '')
        max_members = data.get('max_members', 10)
        
        if not room_name:
            return JsonResponse({'status': 'error', 'message': 'Room name required'}, status=400)
        
        if Room.objects.filter(name=room_name).exists():
            return JsonResponse({'status': 'error', 'message': 'Room name already exists'}, status=400)
        
        room_code = generate_room_code()
        
        room = Room.objects.create(
            name=room_name,
            room_code=room_code,
            description=description,
            max_members=max_members
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Room created successfully',
            'room': {
                'id': room.id,
                'name': room.name,
                'room_code': room.room_code,
                'share_link': f'/join/{room.share_link_id}/',
                'share_link_id': str(room.share_link_id),
                'description': room.description,
                'created_at': room.created_at.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Get all rooms
@csrf_exempt
def get_rooms(request):
    """API: Get all active rooms"""
    try:
        rooms = Room.objects.filter(is_active=True).values(
            'id', 'name', 'room_code', 'share_link_id', 'description', 'max_members', 'created_at'
        ).order_by('-created_at')
        
        rooms_list = []
        for room in rooms:
            room['share_link'] = f'/join/{room["share_link_id"]}/'
            room['member_count'] = RoomMember.objects.filter(room_id=room['id'], is_active=True).count()
            rooms_list.append(room)
        
        return JsonResponse({'status': 'success', 'rooms': rooms_list}, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Get room by code
def get_room_by_code(request):
    """API: Get room details by room code"""
    try:
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'status': 'error', 'message': 'Room code required'}, status=400)
        
        room = Room.objects.get(room_code=code, is_active=True)
        members_count = RoomMember.objects.filter(room=room, is_active=True).count()
        
        return JsonResponse({
            'status': 'success',
            'room': {
                'id': room.id,
                'name': room.name,
                'room_code': room.room_code,
                'description': room.description,
                'max_members': room.max_members,
                'members_count': members_count,
                'created_at': room.created_at.isoformat()
            }
        })
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Get room by share link ID
def get_room_by_share_link(request, share_link_id):
    """API: Get room details by share link UUID"""
    try:
        room = Room.objects.get(share_link_id=share_link_id, is_active=True)
        members_count = RoomMember.objects.filter(room=room, is_active=True).count()
        
        return JsonResponse({
            'status': 'success',
            'room': {
                'id': room.id,
                'name': room.name,
                'room_code': room.room_code,
                'description': room.description,
                'max_members': room.max_members,
                'members_count': members_count,
                'created_at': room.created_at.isoformat()
            }
        })
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Join room
@csrf_exempt
def join_room(request, share_link_id=None):
    """UI: Join room by share link"""
    try:
        room = Room.objects.get(share_link_id=share_link_id, is_active=True)
        return render(request, 'base/join_room.html', {'room': room})
    except Room.DoesNotExist:
        return render(request, 'base/room_not_found.html', {'error': 'Room not found'}, status=404)


# Add member to room
@csrf_exempt
def add_room_member(request):
    """API: Add member to room"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        room_id = data.get('room_id')
        member_name = data.get('name')
        member_uid = data.get('uid')
        
        if not all([room_id, member_name, member_uid]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
        
        room = Room.objects.get(id=room_id)
        
        # Check member limit
        current_members = RoomMember.objects.filter(room=room, is_active=True).count()
        if current_members >= room.max_members:
            return JsonResponse({'status': 'error', 'message': 'Room is full'}, status=400)
        
        member, created = RoomMember.objects.get_or_create(
            room=room,
            uid=member_uid,
            defaults={'name': member_name, 'is_active': True}
        )
        
        if not created and not member.is_active:
            member.is_active = True
            member.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Member added to room',
            'member': {
                'id': member.id,
                'name': member.name,
                'uid': member.uid
            }
        })
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Get room members
def get_room_members(request):
    """API: Get all members in a room"""
    try:
        room_id = request.GET.get('room_id')
        if not room_id:
            return JsonResponse({'status': 'error', 'message': 'Room ID required'}, status=400)
        
        room = Room.objects.get(id=room_id)
        members = RoomMember.objects.filter(room=room, is_active=True).values(
            'id', 'name', 'uid', 'joined_at'
        )
        
        return JsonResponse({
            'status': 'success',
            'room': room.name,
            'members': list(members)
        }, safe=False)
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Remove member from room
@csrf_exempt
def remove_room_member(request):
    """API: Remove member from room"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        member_id = data.get('member_id')
        
        if not member_id:
            return JsonResponse({'status': 'error', 'message': 'Member ID required'}, status=400)
        
        member = RoomMember.objects.get(id=member_id)
        member.is_active = False
        member.save()
        
        return JsonResponse({'status': 'success', 'message': 'Member removed from room'})
    except RoomMember.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Member not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Room management page
def room_management(request):
    """Render room management UI"""
    return render(request, 'base/room_management.html')


# ==================== REAL-TIME CHAT (Socket.io) ====================

# Get chat messages for a room
def get_room_messages(request):
    """API: Get all messages in a room"""
    try:
        room_id = request.GET.get('room_id')
        if not room_id:
            return JsonResponse({'status': 'error', 'message': 'Room ID required'}, status=400)
        
        room = Room.objects.get(id=room_id)
        messages = ChatMessage.objects.filter(room=room).values(
            'id', 'sender_name', 'sender_uid', 'message', 'created_at', 'is_edited'
        ).order_by('created_at')
        
        return JsonResponse({
            'status': 'success',
            'room': room.name,
            'messages': list(messages)
        }, safe=False)
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Send chat message
@csrf_exempt
def send_chat_message(request):
    """API: Send chat message to room"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        room_id = data.get('room_id')
        sender_name = data.get('sender_name')
        sender_uid = data.get('sender_uid')
        message = data.get('message')
        
        if not all([room_id, sender_name, sender_uid, message]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
        
        if len(message.strip()) == 0:
            return JsonResponse({'status': 'error', 'message': 'Message cannot be empty'}, status=400)
        
        room = Room.objects.get(id=room_id)
        
        chat_msg = ChatMessage.objects.create(
            room=room,
            sender_name=sender_name,
            sender_uid=sender_uid,
            message=message
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Message sent',
            'data': {
                'id': chat_msg.id,
                'sender_name': chat_msg.sender_name,
                'message': chat_msg.message,
                'created_at': chat_msg.created_at.isoformat()
            }
        })
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Edit chat message
@csrf_exempt
def edit_chat_message(request):
    """API: Edit a chat message"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        new_message = data.get('message')
        
        if not all([message_id, new_message]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
        
        msg = ChatMessage.objects.get(id=message_id)
        msg.message = new_message
        msg.is_edited = True
        msg.edited_at = timezone.now()
        msg.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Message updated',
            'data': {
                'id': msg.id,
                'message': msg.message,
                'is_edited': msg.is_edited,
                'edited_at': msg.edited_at.isoformat()
            }
        })
    except ChatMessage.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Delete chat message
@csrf_exempt
def delete_chat_message(request):
    """API: Delete a chat message"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST method required'}, status=400)
    
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        
        if not message_id:
            return JsonResponse({'status': 'error', 'message': 'Message ID required'}, status=400)
        
        msg = ChatMessage.objects.get(id=message_id)
        msg.delete()
        
        return JsonResponse({'status': 'success', 'message': 'Message deleted'})
    except ChatMessage.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# Chat room UI
def chat_room(request, room_id=None):
    """Render chat room UI"""
    try:
        if room_id:
            room = Room.objects.get(id=room_id)
        else:
            room = None
        return render(request, 'base/chat_room.html', {'room': room})
    except Room.DoesNotExist:
        return render(request, 'base/room_not_found.html', {'error': 'Room not found'}, status=404)
