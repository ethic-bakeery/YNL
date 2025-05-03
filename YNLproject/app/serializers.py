from rest_framework import serializers
from .models import User, Profile, Poll, Question, Choice, Feedback, Post, Event, ChatMessage, LiveChatSession, Group, GroupMembership, GroupMessage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'state', 'phone_number', 'date_of_birth', 'local_government', 'is_volunteer')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'profile_picture')

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'created_by', 'created_at', 'updated_at', 'image')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'poll', 'text')

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'question', 'text', 'votes')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'poll', 'user', 'comment')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'image', 'created_by', 'created_at', 'updated_at', 'likes', 'dislikes')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'created_by', 'created_at', 'updated_at', 'start_time', 'end_time', 'location', 'attendees')

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'sender', 'recipient', 'message', 'image', 'video', 'voice', 'timestamp')

class LiveChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveChatSession
        fields = ('id', 'participants', 'created_at', 'updated_at')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description', 'created_by', 'created_at')

class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ('id', 'group', 'user', 'joined_at')

class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = ('id', 'sender', 'group', 'message', 'image', 'video', 'voice', 'timestamp')
