from django.contrib import admin

# Register your models here.

from chat.models import ChatMessage

admin.site.register(ChatMessage)