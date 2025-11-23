from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby),
    path('room/', views.room),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
    
    # User Management Routes
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/', views.update_user, name='update_user'),
    path('users/delete/', views.delete_user, name='delete_user'),
    path('users/change-password/', views.change_password, name='change_password'),
    path('manage-users/', views.user_management, name='user_management'),
    
    # Room Management Routes
    path('rooms/', views.get_rooms, name='get_rooms'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/by-code/', views.get_room_by_code, name='get_room_by_code'),
    path('rooms/<str:share_link_id>/', views.get_room_by_share_link, name='get_room_by_share_link'),
    path('join/<str:share_link_id>/', views.join_room, name='join_room'),
    path('rooms/members/add/', views.add_room_member, name='add_room_member'),
    path('rooms/members/', views.get_room_members, name='get_room_members'),
    path('rooms/members/remove/', views.remove_room_member, name='remove_room_member'),
    path('manage-rooms/', views.room_management, name='room_management'),
    
    # Chat Routes
    path('chat/room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('chat/messages/', views.get_room_messages, name='get_room_messages'),
    path('chat/send/', views.send_chat_message, name='send_chat_message'),
    path('chat/edit/', views.edit_chat_message, name='edit_chat_message'),
    path('chat/delete/', views.delete_chat_message, name='delete_chat_message'),
]