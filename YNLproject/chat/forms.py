from django import forms
from .models import Group, GroupMessage, GroupJoinRequest

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'profile_image']  # Removed required_permission
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['content', 'image', 'video', 'voice_note']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Type your message here...'
            }),
        }

class GroupJoinRequestForm(forms.ModelForm):
    class Meta:
        model = GroupJoinRequest
        fields = []