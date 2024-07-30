from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Profile, Poll,ContactMessage,GroupJoinRequest, Question, StaffApplication, Choice, Feedback, Post, Event, ChatMessage, LiveChatSession, Group, GroupMembership, GroupMessage

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

class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_by', 'created_at', 'updated_at')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'text')

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'votes')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('poll', 'user', 'comment')

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

admin.site.register(GroupJoinRequest)
admin.site.register(StaffApplication)
admin.site.register(ContactMessage)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(LiveChatSession, LiveChatSessionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMembership, GroupMembershipAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)
