#!/bin/bash


# App files
touch app/admin.py app/apps.py app/forms.py app/models.py app/serializers.py app/tests.py app/urls.py app/views.py
touch app/templates/admin/add_questions.html app/templates/admin/admin_contact_messages.html app/templates/admin/admin_navbar.html app/templates/admin/admin_staff_application.html app/templates/admin/application_success.html app/templates/admin/approved_staff.html app/templates/admin/view_contact_message.html
touch app/templates/app/application_success.html app/templates/app/apply_for_admin.html app/templates/app/base.html app/templates/app/confirm_delete.html app/templates/app/create_post.html app/templates/app/create_profile.html app/templates/app/delete_account.html app/templates/app/details.html app/templates/app/event_create.html app/templates/app/event.html app/templates/app/feedback.html app/templates/app/home.html app/templates/app/index.html app/templates/app/manage_polls.html app/templates/app/poll_create.html app/templates/app/poll_home.html app/templates/app/poll.html app/templates/app/poll_list.html app/templates/app/profile_detail.html app/templates/app/profile.html app/templates/app/profile_list.html app/templates/app/style.css app/templates/app/submit_feedback.html app/templates/app/test.html app/templates/app/tobecheck.html app/templates/app/update_profile.html app/templates/app/user_navbar.html
touch app/templates/home/base.html app/templates/home/contact_us.html app/templates/home/contact_us_success.html app/templates/home/forgot_password.html app/templates/home/game.html app/templates/home/index.html app/templates/home/login.html app/templates/home/members.html app/templates/home/otp_verification.html app/templates/home/our_team.html app/templates/home/register.html app/templates/home/reset_password.html app/templates/home/states.html app/templates/home/terms_and_conditions.html
touch app/static/app/styles.css

# Chat files
touch chat/admin.py chat/apps.py chat/consumers.py chat/models.py chat/routing.py chat/tests.py chat/urls.py chat/views.py
touch chat/templates/chat/chat.js chat/templates/chat/chat_page.html chat/templates/chat/create_room.html chat/templates/chat/index.html chat/templates/chat/messages.html chat/templates/chat/received_messages.html chat/templates/chat/room.html chat/templates/chat/user_list.html
touch chat/templates/chat/anonymous/temp.html


echo "All necessary files created successfully!"
