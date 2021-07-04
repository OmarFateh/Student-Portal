from django.urls import path

from .views import (
    user_register,
    account_activate,
    # email_activation_sent,
    user_login, 
    user_logout, 
    validate_email,
)

# namespace = accounts

urlpatterns = [
    # Authentication
    path('register/', user_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate-account'),
    # path('email/activate/sent/', email_activation_sent, name='activation-email-sent'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # js validations
    path('ajax/validate/email/', validate_email, name='js-validate-email'),
]    