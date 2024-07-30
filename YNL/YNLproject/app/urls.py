
from django.urls import path
from . import views
from .views import submit_staff_application, admin_staff_applications, approve_application
from .views import application_success
from .views import forgot_password, otp_verification, reset_password,create_profile
from .views import contact_us, contact_us_success, admin_contact_messages, view_contact_message, delete_contact_message
from .views import apply_for_staff, admin_dashboard, approve_request, reject_request

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('create_profile/', create_profile, name='create_profile'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('logout/',views.logout, name="logout"),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('apply/', submit_staff_application, name='submit_staff_application'),
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
    path('team/', views.our_team, name='our_team'),
    path('application-success/', application_success, name='application_success'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('reset-password/', reset_password, name='reset_password'),
    path('contact/', views.contact_us, name='contact_us'),
    path('apply/', apply_for_staff, name='apply_for_staff'),
    
    # ADMIN PAGES 
   
    path('contact/success/', contact_us_success, name='contact_us_success'),
    path('admin/contact-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('admin/contact-message/<int:message_id>/', view_contact_message, name='view_contact_message'),
    path('admin/contact-message/delete/<int:message_id>/', delete_contact_message, name='delete_contact_message'),
    path('admin/applications/', admin_staff_applications, name='admin_staff_applications'),
    path('admin/approve/<int:application_id>/', approve_application, name='approve_application'),
    path('admin/make_staff/', admin_dashboard, name='make_staff'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('application-success/', views.application_success, name='application_success')

]


