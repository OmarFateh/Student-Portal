"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from accounts.decorators import unauthenticated_user
from accounts.forms import (
        EmailValidationOnForgotPassword, 
        PasswordFieldsOnForgotPassword, 
        PasswordFieldsOnChangePassword,
    )

urlpatterns = [
    ## standard admin
    path('admin/', admin.site.urls),
    ## Regular Endpoints
    # Accounts
    path('', include(('accounts.urls', 'accounts'), namespace='accounts')),
    # Userprofile
    path('', include(('userprofile.urls', 'userprofile'), namespace='userprofile')),
    # Classroom 
    path('', include(('classroom.urls', 'classroom'), namespace='classroom')),
    # Module 
    path('', include(('module.urls', 'module'), namespace='module')),
    # Page
    path('', include(('page.urls', 'page'), namespace='page')),
    # Quiz
    path('', include(('quiz.urls', 'quiz'), namespace='quiz')),
    # Assignment
    path('', include(('assignment.urls', 'assignment'), namespace='assignment')),
    # Question
    path('', include(('question.urls', 'question'), namespace='question')),

    # Password reset
    # 1- Submit password form                     // PasswordResetView.as_view() 
    # 2- Email sent success message               // PasswordResetDoneView.as_view()  
    # 3- Link to password reset form in email     // PasswordResetConfirmView.as_view() 
    # 4- password successfully changed message    // PasswordResetCompleteView.as_view()

    path('password/reset/', unauthenticated_user(auth_views.PasswordResetView.as_view(
                                template_name='accounts/password_reset.html',
                                form_class=EmailValidationOnForgotPassword,)),
                                name='password_reset'),
    path('password/reset/sent/', unauthenticated_user(auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html',)), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', unauthenticated_user(auth_views.PasswordResetConfirmView.as_view(
                                template_name='accounts/password_reset_form.html',
                                form_class=PasswordFieldsOnForgotPassword,)),
                                name='password_reset_confirm'),
    # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),                            
    path('password/reset/complete/', unauthenticated_user(auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html',)), name='password_reset_complete'),

    # Password change
    path('password/change/', auth_views.PasswordChangeView.as_view(
                                template_name='accounts/password_change_form.html',
                                form_class=PasswordFieldsOnChangePassword,),
                                name='password_change'),
    path('password/change/complete/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html',), name='password_change_done'),

    # CKEditor 
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)