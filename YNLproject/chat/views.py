
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

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from django.http import JsonResponse
from .models import Group, GroupMembership, GroupMessage, GroupJoinRequest
from .forms import GroupForm, GroupMessageForm, GroupJoinRequestForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,redirect
from .models import ChatMessage
from django.http import HttpResponse

def anonymous(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/anonymous/temp.html", context)

from django.http import JsonResponse
from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def load_messages(request, username):
    user = request.user
    try:
        recipient = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    messages = ChatMessage.objects.filter(
        sender__in=[user, recipient],
        recipient__in=[user, recipient]
    ).order_by('timestamp')

    messages_html = render_to_string('chat/messages.html', {
        'messages': messages,
        'user': user
    })

    return JsonResponse({"messages_html": messages_html})

@login_required
def fetch_messages(request, username):
    user = request.user
    try:
        recipient = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    messages = ChatMessage.objects.filter(
        sender__in=[user, recipient],
        recipient__in=[user, recipient]
    ).order_by('timestamp')

    message_data = [
        {
            "sender": message.sender.username,
            "recipient": message.recipient.username,
            "message": message.message,
            "image": message.image.url if message.image else None,
            "voice": message.voice.url if message.voice else None,
            "timestamp": message.timestamp.isoformat()
        }
        for message in messages
    ]
    return JsonResponse(message_data, safe=False)

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
        return redirect('chat:chat_page', username=username)

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

from django.db.models import Max

@login_required
def received_messages(request):
    user = request.user
    
    # Get the latest timestamp for each sender
    latest_messages = ChatMessage.objects.filter(
        recipient=user
    ).values('sender').annotate(
        latest_timestamp=Max('timestamp')
    )
    
    # Get the actual messages
    messages = ChatMessage.objects.filter(
        recipient=user,
        timestamp__in=[msg['latest_timestamp'] for msg in latest_messages]
    ).order_by('-timestamp')
    
    context = {
        'messages': messages
    }
    return render(request, 'chat/received_messages.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .models import Group, GroupMembership, GroupMessage
from .forms import GroupForm, GroupMessageForm

@login_required
def group_list(request):
    groups = Group.objects.all()
    user_groups = request.user.group_memberships.values_list('group_id', flat=True)
    
    # Simply check if user is a member, no permission checks
    for group in groups:
        group.is_member = group.id in user_groups
    
    return render(request, 'chat/group_list.html', {'groups': groups})
# views.py
@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    is_member = GroupMembership.objects.filter(group=group, user=request.user).exists()
    
    # Get messages ordered by timestamp (oldest first)
    messages_list = GroupMessage.objects.filter(group=group).order_by('timestamp')[:50]
    
    form = GroupMessageForm()

    if request.method == 'POST':
        if 'join_group' in request.POST and not is_member:
            GroupMembership.objects.create(group=group, user=request.user)
            messages.success(request, f"You've joined {group.name}")
            return redirect('chat:group_chat', pk=group.pk)
        
        if is_member and 'send_message' in request.POST:
            form = GroupMessageForm(request.POST, request.FILES)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.group = group
                message.save()
                return redirect('chat:group_chat', pk=group.pk)

    # Add WebSocket URL to context
    ws_scheme = "wss" if request.is_secure() else "ws"
    ws_url = f"{ws_scheme}://{request.get_host()}/ws/chat/{group.pk}/"

    return render(request, 'chat/group_chat.html', {
        'group': group,
        'is_member': is_member,
        'messages': messages_list,
        'form': form,
        'member_count': group.memberships.count(),
        'ws_url': ws_url  # Pass WebSocket URL to template
    })
    
@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            GroupMembership.objects.create(group=group, user=request.user)
            messages.success(request, 'Group created successfully!')
            return redirect(reverse('chat:group_chat', kwargs={'pk': group.pk}))
    else:
        form = GroupForm()
    
    return render(request, 'chat/create_group.html', {'form': form})

@login_required
def leave_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    membership = GroupMembership.objects.filter(group=group, user=request.user).first()
    
    if membership:
        membership.delete()
        messages.success(request, f"You've left {group.name}")
    
    return redirect('chat:group_list')

@login_required
def group_members(request, pk):
    group = get_object_or_404(Group, pk=pk)
    members = group.memberships.all().select_related('user')
    return render(request, 'chat/group_members.html', {
        'group': group,
        'members': members,
    })

def get_messages(request, pk):
    group = get_object_or_404(Group, pk=pk)
    messages = GroupMessage.objects.filter(group=group).order_by('timestamp')[:50]
    data = [{
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime("%b %d, %Y %I:%M %p"),
        'image': msg.image.url if msg.image else None,
    } for msg in messages]
    return JsonResponse(data, safe=False)


def websocket_test(request):
    return render(request, 'chat/websocket_test.html')