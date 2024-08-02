from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import user_list, chat_page, received_messages
from .views import anonymous
# urlpatterns = [
#     path("", chat_views.chatPage, name="chat-page"),
#     path('create/', views.create_room, name='create_room'),
#     path('chat/<str:room_name>/', views.chat_room, name='room'),
# ]


from django.urls import path
from .views import user_list, chat_page

urlpatterns = [
    path('users/', user_list, name='user_list'),
    path('chat/<str:username>/', chat_page, name='chat_page'),
    path('received-messages/', received_messages, name='received_messages'),
    path("anonymous", views.anonymous, name="chat-page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

