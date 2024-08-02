from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import (
    Profile, Poll, ContactMessage, GroupJoinRequest, Vote, StaffApplication,
    Choice, Post, Event, LiveChatSession, Group, GroupMembership, GroupMessage
)

# Unregister the default UserAdmin
admin.site.unregister(User)

# Define your custom UserAdmin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')  # Customize as needed

# Register your custom UserAdmin
admin.site.register(User, UserAdmin)

# Define and register other model admins
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_by', 'created_at', 'updated_at')

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_by', 'created_at', 'updated_at', 'start_time', 'end_time', 'location')

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'message', 'timestamp')

class LiveChatSessionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by', 'created_at')

class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'joined_at')

class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'group', 'message', 'timestamp')

class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice', 'timestamp')

# Register models with admin site
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Event, EventAdmin)
# admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(LiveChatSession, LiveChatSessionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMembership, GroupMembershipAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(GroupJoinRequest)
admin.site.register(StaffApplication)
admin.site.register(ContactMessage)
admin.site.register(Choice)
admin.site.register(Poll)
