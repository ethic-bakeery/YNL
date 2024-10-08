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
from django.contrib import messages
from .models import StaffApplication
from .forms import StaffApplicationForm
from .forms import ProfileForm
from .models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile
from .forms import ProfileUpdateForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

from .models import Post, Comment
from .forms import CommentForm

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    return redirect('home')  

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST' and comment.user == request.user:
        comment.delete()
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})

def login(request):
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

# @login_required
# def submit_staff_application(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         terms = request.POST.get('terms')

#         if terms == 'agree':
#             StaffApplication.objects.create(
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 message=message,
#                 status='Pending'
#             )
#             return redirect('application_success')  # Redirect to a success page
#         else:
#             return redirect('application_error')  # Redirect to an error page

#     return render(request, 'app/apply_for_admin.html')

@login_required
def admin_staff_applications(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    applications = StaffApplication.objects.all()
    return render(request, 'admin/admin_staff_application.html', {'applications': applications})

@user_passes_test(lambda u: u.is_superuser)
def approve_application(request, application_id):
    if not request.user.is_superuser:
        return redirect('home') 
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
    return render(request, 'admin/application_success.html')

# def submit_staff_application(request):
#     if request.method == 'POST':
#         form = StaffApplicationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('application_success')
#     else:
#         form = StaffApplicationForm()
#     return render(request, 'app/apply_for_admin.html', {'form': form})


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


@login_required
def apply_for_staff(request):
    if StaffApplication.objects.filter(user=request.user).exists():
        messages.info(request, 'You have already submitted an application or you are already a staff member.')
        return redirect('home')  
    
    if request.method == 'POST':
        form = StaffApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.status = 'Pending' 
            application.save()
            messages.success(request, 'Your application has been submitted.')
            return redirect('application_success') 
    else:
        form = StaffApplicationForm()
    
    return render(request, 'app/apply_for_admin.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    applications = StaffApplication.objects.all()
    return render(request, 'admin/approved_staff.html', {'applications': applications})

@user_passes_test(lambda u: u.is_superuser)
def approve_request(request, request_id):
    application = get_object_or_404(StaffApplication, id=request_id)
    if not application.user:
        messages.error(request, 'Application user not found.')
        return redirect('make_staff')
    
    application.status = 'Approved'
    application.save()
    
    user = application.user
    user.is_staff = True
    user.save()
    
    messages.success(request, f'Request from {user.username} has been approved.')
    return redirect('make_staff')

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


@user_passes_test(lambda u: u.is_superuser)
def reject_request(request, request_id):
    application = get_object_or_404(StaffApplication, id=request_id)
    application.status = 'Rejected'
    application.save()
    messages.success(request, 'Request has been rejected.')
    return redirect('make_staff')


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