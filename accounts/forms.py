from django import forms
# from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm


User = get_user_model()

class UserRegisterForm(UserCreationForm):
    """
    User creation form class.
    """
    full_name = forms.CharField(
        label='',
        max_length=200,
        help_text = 'Required', 
        widget=forms.TextInput(attrs={'class':'validate js-validate-fullname', 'autofocus': True, 'name':'fullname'}),
    )
    email = forms.EmailField(
        label='',
        max_length=200,
        help_text = 'Required', 
        widget=forms.EmailInput(attrs={'class':'validate js-validate-email', 'name':'email'}),
    )
    email2 = forms.EmailField(
        label='',
        max_length=200,
        help_text = 'Required', 
        widget=forms.EmailInput(attrs={'class':'validate js-validate-email2', 'name':'confirm_email'}),
    )
    password1 = forms.CharField(
        label='', 
        help_text = 'Required',
        widget=forms.PasswordInput(attrs={'class':'validate js-validate-password1', 'name':'password'}),
        strip=False,
    )
    password2 = forms.CharField(
        label='',
        help_text = 'Required', 
        widget=forms.PasswordInput(attrs={'class':'validate js-validate-password2', 'name':'confirm_password'}),
        strip=False,
    )

    class Meta:
        model   = User
        fields  = ['full_name', 'email', 'email2', 'password1', 'password2']    

    def clean_full_name(self):
        """
        Validate fullname.
        """
        full_name = self.cleaned_data.get("full_name")
        forbidden_users = ['admin', 'user', 'login', 'authenticate', 'css', 'js', 'logout', 'adminstrator', 
            'root', 'email', 'join', 'sql', 'static', 'python', 'delete']    
        if full_name.lower() in forbidden_users:
            raise forms.ValidationError("This is a reserved word.", code='reserved word')
        if '@' in full_name or '-' in full_name or '+' in full_name or '=' in full_name:
            raise forms.ValidationError("This is an Invalid Name, Do not use these chars: @ , - , + , =", code='invalid')    
        return full_name

    def clean_email2(self):
        """
        Validate email 2.
        """
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get('email2') 
        # check if the two emails match.
        if email1 != email2:
            raise forms.ValidationError('The two email fields didn’t match.', code="emails don't match")
        # check if the email has already been used.  
        if User.objects.filter(email__iexact=email2).exists():
            raise forms.ValidationError("An account with this Email already exists.", code="email exists")
        return email2


class UpdateUserForm(forms.ModelForm):
    """
    Update User model form.
    """
    full_name = forms.CharField(
        label='Full name', 
        widget=forms.TextInput(attrs={'class':'validate', 'name':'full_name'}),
    )
    email = forms.EmailField(
        label='Email address', 
        widget=forms.EmailInput(attrs={'class':'validate js-validate-email-update', 'name':'email'}),
    )

    class Meta:
        model  = User
        fields = ['full_name', 'email']

    def __init__(self, *args, **kwargs):
        self.staff_student = kwargs.pop("staff_student", None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)    

    def clean_email(self):
        """
        Validate email.
        """
        email = self.cleaned_data.get("email")
        # check if the email has already been used.   
        if User.objects.filter(email__iexact=email).exclude(email__iexact=self.staff_student.user.email).exists():
            raise forms.ValidationError("An account with this Email already exists.")
        return email


class EmailValidationOnForgotPassword(PasswordResetForm):
    """
    Override password reset form email field and its validation.
    """
    email = forms.EmailField(
        label='',
        max_length=255,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'validate', 'name':'email', 'required':True})
    )

    def clean_email(self):
        """
        Validate email.
        """
        # fetch entered email.
        email = self.cleaned_data['email']
        # check if the entered email doesn't exist.
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Your email was entered incorrectly. Please enter it again.", code='incorrect email')
        return email


class PasswordFieldsOnForgotPassword(SetPasswordForm):
    """
    Override set password form password fields.
    """
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'validate js-validate-password1 mb-2', 'id':'id_password1', 'required':True}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'validate js-validate-password2', 'id':'id_password2', 'required':True}),
    )


class PasswordFieldsOnChangePassword(PasswordChangeForm):
    """
    Override password change form password fields.
    """
    old_password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'validate mb-2', 'required':True}),
    )
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'validate js-validate-password1 mb-2', 'id':'id_password1', 'required':True}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'validate js-validate-password2', 'id':'id_password2', 'required':True}),
    )
