
# def chatPage(request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         return redirect("login")
#     context = {}
#     return render(request, "chat/chat_page.html", context)


# # from django.urls import reverse

# def create_room(request):
#     if request.method == 'POST':
#         room_name = request.POST.get('room_name')
#         return redirect(reverse('room', kwargs={'room_name': room_name}))
#     return render(request, 'chat/create_room.html')


# def chat_room(request, room_name):
#     return render(request, 'chat/room.html', {'room_name': room_name})


from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from django.http import HttpResponse

def anonymous(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/anonymous/temp.html", context)

@login_required
def chat_page(request, username):
    user = request.user
    try:
        recipient = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)
    
    if request.method == 'POST':
        message_content = request.POST.get('message')
        image = request.FILES.get('image')
        voice = request.FILES.get('voice')
        ChatMessage.objects.create(
            sender=user,
            recipient=recipient,
            message=message_content,
            image=image,
            voice=voice
        )
        return redirect('chat_page', username=username)

    messages = ChatMessage.objects.filter(
        sender__in=[user, recipient],
        recipient__in=[user, recipient]
    ).order_by('timestamp')

    context = {
        'recipient': recipient,
        'messages': messages
    }
    return render(request, 'chat/chat_page.html', context)


def get_users(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=403)
    users = User.objects.exclude(id=request.user.id)
    user_list = [{"username": user.username} for user in users]
    return JsonResponse(user_list, safe=False)

def user_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user
    context = {'users': users}
    return render(request, "chat/user_list.html", context)


@login_required
def received_messages(request):
    user = request.user

    # Get all messages where the current user is the recipient
    messages = ChatMessage.objects.filter(recipient=user).order_by('-timestamp')

    context = {
        'messages': messages
    }
    return render(request, 'chat/received_messages.html', context)


@login_required
def chat_page(request, username):
    user = request.user
    recipient = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        message_content = request.POST.get('message')
        image = request.FILES.get('image')
        voice = request.FILES.get('voice')
        ChatMessage.objects.create(
            sender=user,
            recipient=recipient,
            message=message_content,
            image=image,
            voice=voice
        )
        return redirect('chat_page', username=username)

    messages = ChatMessage.objects.filter(
        sender__in=[user, recipient],
        recipient__in=[user, recipient]
    ).order_by('timestamp')

    context = {
        'recipient': recipient,
        'messages': messages
    }
    return render(request, 'chat/chat_page.html', context)
