
from django.urls import path
from . import views
from .views import submit_staff_application, admin_staff_applications, approve_application
from .views import application_success
from .views import forgot_password, otp_verification, reset_password

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
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
    path('admin/applications/', admin_staff_applications, name='admin_staff_applications'),
    path('admin/approve/<int:application_id>/', approve_application, name='approve_application'),
    path('application-success/', application_success, name='application_success'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp-verification/', otp_verification, name='otp_verification'),
    path('reset-password/', reset_password, name='reset_password'),
    # other url patterns
]

 
