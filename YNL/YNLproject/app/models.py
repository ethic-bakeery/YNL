from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.conf import settings  
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    local_government = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='media/uploads/images', blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Profile"

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

class StaffApplication(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved')])

    def save(self, *args, **kwargs):
        if self.user and StaffApplication.objects.filter(user=self.user).exists():
            raise ValueError("User has already submitted a request.")
        super().save(*args, **kwargs)

    
class Poll(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE) 
    text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)  
    poll = models.ForeignKey(
        Poll, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True)
    choice = models.ForeignKey(
        Choice, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now())

    class Meta:
        unique_together = ('user', 'poll')  

    def __str__(self):
        poll_name = self.poll.name if self.poll else 'No Poll'
        choice_name = self.choice.text if self.choice else 'No Choice'
        return f"{poll_name} - {choice_name}"


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}..."

class Event(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    attendees = models.ManyToManyField(User, related_name='event_attendees', blank=True)

    def __str__(self):
        return self.title

# class ChatMessage(models.Model):
#     sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
#     recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
#     message = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
#     video = models.FileField(upload_to='chat_videos/', blank=True, null=True)
#     voice = models.FileField(upload_to='chat_voices/', blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message from {self.sender.email} to {self.recipient.email} at {self.timestamp}"

class LiveChatSession(models.Model):
    participants = models.ManyToManyField(User, related_name='live_chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat Session created at {self.created_at}"
    
class Group(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_groups', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(upload_to='group_profiles/', blank=True, null=True)
    memberships = models.ManyToManyField(User, through='GroupMembership')


    def __str__(self):
        return self.name

class GroupMembership(models.Model):  
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_memberships')
    user = models.ForeignKey(User, related_name='group_memberships', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} in {self.group.name}"

class GroupMessage(models.Model):
    sender = models.ForeignKey(User, related_name='group_sent_messages', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='group_chat_images/', blank=True, null=True)
    video = models.FileField(upload_to='group_chat_videos/', blank=True, null=True)
    voice = models.FileField(upload_to='group_chat_voices/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} in {self.group.name} at {self.timestamp}"

class GroupJoinRequest(models.Model):
    user = models.ForeignKey(User, related_name='group_join_requests', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='join_requests', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.email} requested to join {self.group.name}"

