from django import forms
from .models import Profile
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'state', 'phone_number', 'date_of_birth', 'local_government', 'bio', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }


from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback'}),
        }

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
