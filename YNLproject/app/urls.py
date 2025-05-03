from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import staff_application, staff_application_status, staff_application_list, staff_application_review
from .views import (
    application_success,
    forgot_password,
    otp_verification,
    reset_password,
    create_profile,
    contact_us,
    contact_us_success,
    admin_contact_messages,
    view_contact_message,
    delete_contact_message,
    PollCreateView,
    EventCreateView,
    EventListView,
    create_post,
    delete_account,
    add_comment,
    delete_comment,
    profile_list,
    profile_detail,
    index,
    create_member_view,
    state,
    login,
    profile
    
)


urlpatterns = [
    #unathenticated user

    path('', views.index, name='index'),
    path('members/',views.state, name='members'),
    path('create-member/', create_member_view, name='create-member'),
    path('state-team/<str:state_name>/', views.state_team_view, name='state_team'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
    path('team/', views.our_team, name='our_team'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('reset-password/', reset_password, name='reset_password'),
    path('contact/', views.contact_us, name='contact_us'),
    path('contact/success/', contact_us_success, name='contact_us_success'),

    #uthyenticated user
    # urls.py



    path('profiles/', profile_list, name='profile_list'),
    path('profiles/<str:username>/', profile_detail, name='profile_detail'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),

    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('create_profile/', create_profile, name='create_profile'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('logout/',views.logout, name="logout"),
    path('update-profile-picture/', views.update_profile, name='update_profile_picture'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('application-success/', application_success, name='application_success'),
    path('polls/', views.PollListView.as_view(), name='poll_list'),
    path("poll/<int:poll_id>/", views.PollView.as_view(), name="single_poll"),
    path('events/', EventListView.as_view(), name='event-detail'),
    path('delete-account/', delete_account, name='delete_account'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    #STAFF PAGES
    path('create-post/', create_post, name='create-post'),
    path('event/create/', EventCreateView.as_view(), name='create-event'),
    path('poll/create/', PollCreateView.as_view(), name='create_poll'),

    # Announcement
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/new/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:pk>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcements/<int:pk>/delete/', views.delete_announcement, name='delete_announcement'),
    path('announcements/manage/', views.manage_announcements, name='manage_announcements'),


    # ADMIN PAGES 
   
    path('admin/contact-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('admin/contact-message/<int:message_id>/', view_contact_message, name='view_contact_message'),
    path('admin/contact-message/delete/<int:message_id>/', delete_contact_message, name='delete_contact_message'),

    # New
    path('apply/', staff_application, name='staff_application'),
    path('application/status/', staff_application_status, name='staff_application_status'),
    path('staff/applications/', staff_application_list, name='staff_application_list'),
    path('staff/applications/<int:pk>/review/', staff_application_review, name='staff_application_review'),

]


