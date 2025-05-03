from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.forms import PasswordResetForm
from .models import Poll, Choice,Event,Post,Profile,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import StaffApplication
from .models import Announcement
from ckeditor.widgets import CKEditorWidget



class AnnouncementForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Announcement
        fields = ['title', 'description', 'image', 'is_active']

    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Skip styling for CheckboxInput and CKEditorWidget
            if field.widget.__class__.__name__ not in ['CheckboxInput', 'CKEditorWidget']:
                field.widget.attrs.update({
                    'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
                })



class StaffApplicationForm(forms.ModelForm):
    class Meta:
        model = StaffApplication
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class StaffApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = StaffApplication
        fields = ['status', 'admin_message']
        widgets = {
            'admin_message': forms.Textarea(attrs={'rows': 3}),
        }
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'state', 'phone_number', 'date_of_birth', 'local_government', 'bio', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']
        widgets = {
            'description': CKEditorWidget(),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['name', 'description']

class ChoiceForm(forms.Form):
    choice_text = forms.CharField(label='Choice Text', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter choice'}))


class StaffApplicationForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    comments = forms.CharField(widget=forms.Textarea, required=False)
    agreement = forms.BooleanField(required=True, label='I agree to the terms and conditions')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', validators=[EmailValidator()])

class OTPVerificationForm(forms.Form):
    email = forms.EmailField(label='Email', validators=[EmailValidator()])
    otp = forms.CharField(label='OTP', max_length=6)

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', validators=[EmailValidator()])
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'state', 'phone_number', 'date_of_birth', 'local_government', 'bio', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
# forms.py
from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'message']

from django import forms
from .models import StaffApplication

from django import forms
from .models import StaffApplication

class StaffApplicationForm(forms.ModelForm):
    class Meta:
        model = StaffApplication
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }


# app/forms.py
from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'state', 'level', 'position', 'email', 'image', 'priority']


# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['comment']

