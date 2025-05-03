from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.contrib.auth import logout as auth_logout
from app.models import Post
from django.views import View
from app.models import Poll, Choice, Vote
from django.utils.decorators import method_decorator
from .forms import PollForm, ChoiceForm
from django.db.models import Q 
from app.forms import StaffApplicationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import StaffApplication
from .forms import StaffApplicationForm
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.http import JsonResponse
from .forms import ProfileUpdateForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .forms import ForgotPasswordForm, OTPVerificationForm, ResetPasswordForm
import random
from django.contrib.auth.decorators import login_required
from .forms import PostForm  
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db.models import Count, Q
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from .models import ContactMessage
from .forms import ContactMessageForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event
from .forms import EventForm
from .models import Member
from django.shortcuts import render
from .models import Member
from django.contrib.auth.decorators import user_passes_test
from .forms import MemberForm


from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StaffApplicationForm, StaffApplicationAdminForm
from .models import StaffApplication

@login_required
def staff_application(request):
    if request.user.is_staff:
        return redirect('home')
    
    try:
        existing_application = StaffApplication.objects.get(user=request.user)
        return render(request, 'staff/application_status.html', {'application': existing_application})
    except StaffApplication.DoesNotExist:
        pass

    if request.method == 'POST':
        form = StaffApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('staff_application_status')
    else:
        form = StaffApplicationForm()

    return render(request, 'staff/application_form.html', {'form': form})

@login_required
def staff_application_status(request):
    application = get_object_or_404(StaffApplication, user=request.user)
    return render(request, 'staff/application_status.html', {'application': application})

@user_passes_test(lambda u: u.is_superuser)
def staff_application_list(request):
    applications = StaffApplication.objects.all().order_by('-id')
    return render(request, 'staff/admin/application_list.html', {'applications': applications})

@user_passes_test(lambda u: u.is_superuser)
def staff_application_review(request, pk):
    application = get_object_or_404(StaffApplication, pk=pk)
    
    if request.method == 'POST':
        form = StaffApplicationAdminForm(request.POST, instance=application)
        if form.is_valid():
            # Get the form data without saving yet
            app = form.save(commit=False)
            
            # Check which button was clicked
            if 'approve' in request.POST:
                app.status = 'Approved'
                if app.user:  # Make sure there's a user associated
                    app.user.is_staff = True
                    app.user.is_active = True  # Ensure account is active
                    app.user.save()
                    print(f"DEBUG: Granted staff access to {app.user.username}")  # Debug line
            
            elif 'reject' in request.POST:
                app.status = 'Rejected'
                if app.user:
                    app.user.is_staff = False
                    app.user.save()
            
            app.save()
            
            messages.success(request, f'Application has been {app.status.lower()}')
            return redirect('staff_application_list')
    else:
        form = StaffApplicationAdminForm(instance=application)
    
    return render(request, 'staff/admin/application_review.html', {
        'application': application,
        'form': form,
        'is_staff': application.user.is_staff if application.user else False
    })
    
from django.contrib import admin
from .models import StaffApplication

@admin.register(StaffApplication)
class StaffApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user', 'status', 'created_at', 'is_staff_user')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_applications', 'reject_applications']
    
    def is_staff_user(self, obj):
        return obj.user.is_staff if obj.user else False
    is_staff_user.boolean = True
    is_staff_user.short_description = 'Has Staff Access'

    def approve_applications(self, request, queryset):
        for application in queryset.filter(status='Pending'):
            application.status = 'Approved'
            if application.user:
                application.user.is_staff = True
                application.user.save()
            application.save()
        self.message_user(request, f"{queryset.count()} applications approved.")

    def reject_applications(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, f"{queryset.count()} applications rejected.")

    approve_applications.short_description = "Approve selected applications"
    reject_applications.short_description = "Reject selected applications"


def state(request):
    return render(request,'home/states.html')

def is_admin(user):
    return user.is_superuser 

@user_passes_test(is_admin)
def create_member_view(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create-member')  # Redirect after saving
    else:
        form = MemberForm()

    return render(request, 'home/create_member.html', {'form': form})

def state_team_view(request, state_name):
    members = Member.objects.filter(state__iexact=state_name).order_by('priority')
    context = {
        'members': members,
        'state_name': state_name.title(),
    }
    return render(request, 'home/states-team.html', context)


def user_is_staff(user):
    return user.is_staff

@login_required
def profile_list(request):
    query = request.GET.get('q', '')
    profiles = Profile.objects.filter(
        Q(user__username__icontains=query) | 
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query)
    )
    return render(request, 'app/profile_list.html', {'profiles': profiles, 'query': query})


@login_required
def profile_detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'app/profile_detail.html', {'profile': profile})

def index(request):
    return render(request, 'home/index.html')

@login_required(login_url='/login/')
def home(request):
    q = request.POST.get('q', '')
    post = Post.objects.all()
    
    if q:
        post = post.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        ).annotate(
            likes_count=Count('likes'),
            dislikes_count=Count('dislikes')
        )
    else:
        post = post.annotate(
            likes_count=Count('likes'),
            dislikes_count=Count('dislikes')
        )
    
    context = {'post': post, 'query': q}
    return render(request, 'app/home.html', context)

@login_required
def create_post(request):
    if not request.user.is_staff:  
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')  
    else:
        form = PostForm()

    return render(request, 'app/create_post.html', {'form': form})
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Comment
from django.contrib.auth.decorators import login_required
import json

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(
                user=request.user,
                post=post,
                content=data.get('content')
            )
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'username': request.user.username
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            if comment.user == request.user:
                comment.delete()
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

def register(request):
    if request.method == 'POST':
        # Create a custom form instance with the POST data
        form = UserCreationForm(request.POST)
        
        # Manually validate email (since UserCreationForm doesn't include it by default)
        email = request.POST.get('email', '').strip()
        if not email:
            form.add_error(None, ValidationError("Email address is required."))
        
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email  # Save the email to the user model
            user.save()
            
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            # Add specific error messages for common cases
            for field, errors in form.errors.items():
                for error in errors:
                    if field == 'username' and 'already exists' in error.lower():
                        messages.error(request, 'Username already exists. Please choose a different one.')
                    elif field == 'password2' and 'too short' in error.lower():
                        messages.error(request, 'Password is too short. It must contain at least 8 characters.')
                    elif field == 'password2' and 'mismatch' in error.lower():
                        messages.error(request, 'Passwords do not match.')
                    else:
                        messages.error(request, f'Error in {field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'home/register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            # Check if the user has a profile
            if not Profile.objects.filter(user=user).exists():
                # Redirect to create profile page if profile does not exist
                return redirect('create_profile')
                
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'home/login.html', {'form': form})


@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('create_profile')  # or wherever users can create one
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
from django.http import JsonResponse

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        # Remove dislike if user had disliked before
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count(),
        'dislikes_count': post.dislikes.count()
    })

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        post.dislikes.add(request.user)
        disliked = True
        # Remove like if user had liked before
        if request.user in post.likes.all():
            post.likes.remove(request.user)
    
    return JsonResponse({
        'disliked': disliked,
        'likes_count': post.likes.count(),
        'dislikes_count': post.dislikes.count()
    })

def application_success(request):
    return render(request, 'admin/application_success.html')

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


User = get_user_model()
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
    return render(request, 'home/forgot_password.html', {'form': form})

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
    return render(request, 'home/otp_verification.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return redirect('login')  #
    else:
        form = ResetPasswordForm()
    return render(request, 'home/reset_password.html', {'form': form})

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')  
    else:
        form = ProfileForm()

    return render(request, 'app/create_profile.html', {'form': form})


def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_us_success')
    else:
        form = ContactMessageForm()
    
    return render(request, 'home/contact_us.html', {'form': form})

def contact_us_success(request):
    return render(request, 'home/contact_us_success.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_contact_messages(request):
    messages = ContactMessage.objects.all()
    return render(request, 'admin/admin_contact_messages.html', {'messages': messages})

@user_passes_test(lambda u: u.is_superuser)
def view_contact_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'admin/view_contact_message.html', {'message': message})

@user_passes_test(lambda u: u.is_superuser)
def delete_contact_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    if request.method == 'POST':
        message.delete()
        return redirect('admin_contact_messages')
    return render(request, 'app/confirm_delete.html', {'message': message})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'app/details.html', {'event': event})


@method_decorator(login_required, name='dispatch')
class PollView(View):

    def get(self, request, poll_id):
        poll = Poll.objects.get(id=poll_id)
        user_vote = Vote.objects.filter(user=request.user, poll=poll).first()  
        return render(
            request,
            template_name="app/poll.html",
            context={
                "poll": poll,
                "user_vote": user_vote,
            }
        )

    def post(self, request, poll_id):
        requestData = request.POST
        choice_id = requestData.get('choice_id')

        poll = Poll.objects.get(id=poll_id)
        choice = Choice.objects.get(id=choice_id)

        if Vote.objects.filter(user=request.user, poll=poll).exists():
            return render(
                request,
                template_name="app/poll.html",
                context={
                    "poll": poll,
                    "error_message": "You have already voted in this poll.",
                }
            )

     
        Vote.objects.create(
            user=request.user,  
            poll=poll,
            choice=choice,
        )

        poll_results = []
        for choice in poll.choices.all():
            voteCount = Vote.objects.filter(poll=poll, choice=choice).count()
            poll_results.append([choice.text, voteCount])

        return render(
            request,
            template_name="app/poll.html",
            context={
                "poll": poll,
                "success_message": "Voted Successfully",
                "poll_results": poll_results,
            }
        )

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_staff), name='dispatch')
class PollCreateView(View):
    def get(self, request):
        poll_form = PollForm()
        choice_form = ChoiceForm()
        return render(
            request,
            template_name="app/poll_create.html",
            context={
                'poll_form': poll_form,
                'choice_form': choice_form
            }
        )

    def post(self, request):
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save()

            choices = request.POST.getlist('choice_text')
            for choice_text in choices:
                if choice_text.strip(): 
                    Choice.objects.create(poll=poll, text=choice_text.strip())

            return redirect('single_poll', poll_id=poll.id)
        
        choice_form = ChoiceForm()
        return render(
            request,
            template_name="app/poll_create.html",
            context={
                'poll_form': poll_form,
                'choice_form': choice_form
            }
        )
@method_decorator(login_required, name='dispatch')
class PollListView(View):
    def get(self, request):
        polls = Poll.objects.all()
        return render(
            request,
            template_name="app/poll_list.html",
            context={
                "polls": polls
            }
        )


class EventListView(View):
    def get(self, request):
        q = request.GET.get('q', '')  
        events = Event.objects.all()
        
        if q:
            events = events.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        context = {
            'events': events,
            'query': q
        }
        return render(
            request,
            template_name="app/event.html",
            context=context
        )

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_staff), name='dispatch')
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'app/event_create.html'
    success_url = reverse_lazy('application_success')  

    def form_valid(self, form):
        form.instance.created_by = self.request.user  
        return super().form_valid(form)

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')  # Redirect to the home page or any other page after deletion

    return render(request, 'app/delete_account.html')


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def terms_and_conditions(request):
    return render(request, 'home/terms_and_conditions.html')

def our_team(request):
    return render(request, 'home/our_team.html')

from .models import Announcement
from .forms import AnnouncementForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            return redirect('announcements_list')
    else:
        form = AnnouncementForm()
    
    return render(request, 'announcements/create_announcement.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcements_list')
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'announcements/edit_announcement.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcements_list')
    return render(request, 'announcements/delete_announcement.html', {'announcement': announcement})

def announcements_list(request):
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'announcements/list.html', {'announcements': announcements})

from django.core.paginator import Paginator

@login_required
@user_passes_test(is_admin)
def manage_announcements(request):
    announcements_list = Announcement.objects.all().order_by('-created_at')
    
    # Pagination (10 items per page)
    paginator = Paginator(announcements_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'announcements/manage_announcements.html', {
        'announcements': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })