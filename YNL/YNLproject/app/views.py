from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.contrib.auth import logout as auth_logout
from app.models import Post
from django.db.models import Q 
from app.forms import StaffApplicationForm

# @login_required
# def home(request):
#     return render(request, 'app/index.html', {'user': request.user})

def home(request):
    q = request.POST.get('q', '')  
    post = []
    if q:
        post = Post.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )
    context = {'post': post, 'query': q}
    return render(request, 'app/home.html', context)


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return redirect('register')
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')
    
    return render(request, 'app/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to their profile or another page
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    
    return render(request, 'app/login.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileUpdateForm

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'app/profile.html', {'profile': profile})

@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'app/update_profile.html', {'form': form})

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            profile.profile_picture = profile_picture
            profile.save()
            return redirect('profile')
    return redirect('profile')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return redirect('home')

from .models import StaffApplication

@login_required
def submit_staff_application(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        terms = request.POST.get('terms')

        if terms == 'agree':
            StaffApplication.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message,
                status='Pending'
            )
            return redirect('application_success')  # Redirect to a success page
        else:
            return redirect('application_error')  # Redirect to an error page

    return render(request, 'app/apply_for_admin.html')

from .models import StaffApplication

@login_required
def admin_staff_applications(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    applications = StaffApplication.objects.all()
    return render(request, 'app/admin_staff_application.html', {'applications': applications})

@login_required
def approve_application(request, application_id):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    application = get_object_or_404(StaffApplication, id=application_id)
    user = User.objects.get(email=application.email)

    user.is_staff = True
    user.save()

    from django.contrib.auth.models import Group
    staff_group, created = Group.objects.get_or_create(name='Staff')
    user.groups.add(staff_group)

    application.status = 'Approved'
    application.save()

    return redirect('admin_staff_applications')

def application_success(request):
    return render(request, 'app/application_success.html')

def submit_staff_application(request):
    if request.method == 'POST':
        form = StaffApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application_success')  # Ensure this name matches the URL pattern
    else:
        form = StaffApplicationForm()
    return render(request, 'app/apply_for_admin.html', {'form': form})

# # app/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Poll, Feedback
# from django.contrib.auth.decorators import login_required

# @login_required
# def feedback(request, poll_id):
#     poll = get_object_or_404(Poll, id=poll_id)

#     if request.method == 'POST':
#         comment = request.POST.get('comment')
        
#         # Check if user has already given feedback
#         if Feedback.objects.filter(poll=poll, user=request.user).exists():
#             return render(request, 'app/feedback.html', {'poll': poll, 'error': 'You have already given feedback for this poll.'})

#         # Create and save the feedback
#         Feedback.objects.create(poll=poll, user=request.user, comment=comment)
#         return redirect('home')  # Redirect to home page after submission

#     return render(request, 'app/feedback.html', {'poll': poll})
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from .forms import ForgotPasswordForm, OTPVerificationForm, ResetPasswordForm
import random

User = get_user_model()

# Store OTPs in-memory for this example; in production, use a persistent storage
otp_store = {}

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = get_random_string(length=6, allowed_chars='0123456789')
                otp_store[email] = otp

                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return redirect('otp_verification')
            except User.DoesNotExist:
                form.add_error('email', 'No user with this email address.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'app/forgot_password.html', {'form': form})

def otp_verification(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']

            if otp_store.get(email) == otp:
                return redirect('reset_password')
            else:
                form.add_error('otp', 'Invalid OTP.')
    else:
        form = OTPVerificationForm()
    return render(request, 'app/otp_verification.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return redirect('login')  # Redirect to login page or some success page
    else:
        form = ResetPasswordForm()
    return render(request, 'app/reset_password.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

def terms_and_conditions(request):
    return render(request, 'app/terms_and_conditions.html')

def our_team(request):
    return render(request, 'app/our_team.html')