from django.contrib import admin
from .models import Group, GroupMembership, GroupMessage, GroupJoinRequest

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0
    raw_id_fields = ('user',)
    readonly_fields = ('joined_at',)

class GroupMessageInline(admin.TabularInline):
    model = GroupMessage
    extra = 0
    readonly_fields = ('timestamp', 'sender')
    fields = ('sender', 'content', 'timestamp', 'image', 'video', 'voice_note')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'member_count')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'member_count')
    inlines = [GroupMembershipInline, GroupMessageInline]
    
    def member_count(self, obj):
        return obj.memberships.count()
    member_count.short_description = 'Members'

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'joined_at')
    list_filter = ('group', 'joined_at')
    search_fields = ('group__name', 'user__username')

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'content_preview', 'timestamp')
    list_filter = ('group', 'sender', 'timestamp')
    search_fields = ('content', 'group__name', 'sender__username')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(GroupJoinRequest)
class GroupJoinRequestAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'status', 'requested_at')
    list_filter = ('status', 'group', 'requested_at')