from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import UserRegisterForm 
from .decorators import unauthenticated_user
from .utils import send_activation_email

User = get_user_model()


# Restrict the authenticated user from visiting this page and redirect to home page. 
@unauthenticated_user
def user_register(request):
    """
    Create new user.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # fetch submitted data
            full_name = form.cleaned_data.get("full_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            # create new user
            new_user = User.objects.create(full_name=full_name, email=email)
            new_user.set_password(password)
            new_user.save()
            # sent activation email
            send_activation_email(request, new_user)
            # Display success message
            messages.success(request, f"New Account has been created successfully for {email}. Please check your email, We've emailed you instructions for activating your account.", extra_tags='activation-valid')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()    
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def validate_email(request):
    """
    Validate email asynchronously by ajax, and check if it's already been taken or not.
    """
    # get submitted email.
    email = request.GET.get('email', None)
    try:
        # check if an account with this email already exists, in case of editing user's profile.
        is_email_taken = User.objects.filter(email__iexact=email).exclude(email__iexact=request.user.email).exists()
    except:    
        # check if an account with this email already exists, in case of registering new user.
        is_email_taken = User.objects.filter(email__iexact=email).exists()
    data = {'is_email_taken':is_email_taken}
    if data['is_email_taken']:
        data['error_message'] = 'An account with this Email already exists.'
    return JsonResponse(data)

def account_activate(request, uidb64, token):
    """
    Take user's id and token, and activate user's account.
    """
    try:
        # decode the user's id and get the user by id.
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, id=user_id)
        if user.is_active:
            # Display already activated account message
            messages.success(request, f'Your Account already activated. You can login.', extra_tags='activation-valid')
        # check if the token is valid.
        elif account_activation_token.check_token(user, token):
            user.is_active = True
            # user.previously_logged_in = True
            user.save()
            # Display activation success message
            messages.success(request, f'Your Account has been activated successfully. Now you can login.', extra_tags='activation-valid') 
        else:
            # Display error message.
            messages.error(request, f'The activation link is invalid. Please request a new one.', extra_tags='activation-invalid') 
    except DjangoUnicodeDecodeError:
        # Display error message.
        messages.error(request, f'The activation link is invalid. Please request a new one.', extra_tags='activation-invalid') 
    return redirect('accounts:login')

@unauthenticated_user
def user_login(request):
    """
    Take request and login user.
    """
    if request.method == "POST":
        # fetch submitted data.
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            # check if the entered email exists.
            user = authenticate(username=email, password=password)
            # Email and Password are correct. 
            if user:
                if user.is_active:
                    # login user.
                    login(request, user)   
                    return redirect(reverse('classroom:categories'))
                # user is not active.
                else:
                    # sent activation email
                    send_activation_email(request, user)
                    # Display error message.
                    messages.error(request, f'Account is not active. Please check your email.', extra_tags='login')              
            # Email or Password doesn't exist. 
            else:
                # Display error message.
                messages.error(request, f'Email or Passowrd is incorrect.', extra_tags='login')
        # Email or Password are is empty.
        else:
            # Display error message.
            messages.error(request, f'Please fill all the fields.', extra_tags='login')        
    return render(request, 'accounts/login.html', {})

def user_logout(request):
    """
    Take request and logout user.
    """
    logout(request)
    return redirect('accounts:login')