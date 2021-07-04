from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.forms import UserRegisterForm, EmailValidationOnForgotPassword

User = get_user_model()


class TestAccountsFormValidation(TestCase):
    
    def setUp(self):
        self.data = {
            'full_name': 'test',
            'email': 'test@gmail.com',
            'email2': 'test@gmail.com',
            'password1': 'admin160',
            'password2': 'admin160',
        }
        self.user = User.objects.create_user(email='test1@gmail.com', password='admin1600', is_active=True)

    def test_register_user_form(self):
        """
        Test register user form validation.
        """
        form = UserRegisterForm(data=self.data)
        self.assertTrue(form.is_valid())
    
    def test_fullname_validation(self):
        """
        Test full name validation error.
        """
        # test reserved word
        self.data['full_name'] = 'admin'
        self.data['email'] = 'test1@gmail.com'
        self.data['email2'] = 'test1@gmail.com'
        form = UserRegisterForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('full_name', code='reserved word'))
        # test invalid name
        self.data['full_name'] = 'test@'
        form = UserRegisterForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('full_name', code='invalid'))

    def test_email_validation(self):
        """
        Test email validation error.
        """
        # test emails don't match
        self.data['email'] = 'test2@gmail.com'
        self.data['email2'] = 'test3@gmail.com'
        form = UserRegisterForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('email2', code="emails don't match"))
        # test invalid name
        self.data['email'] = 'test1@gmail.com'
        self.data['email2'] = 'test1@gmail.com'
        form = UserRegisterForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('email2', code="email exists"))

    def test_forget_password_email_validation(self):
        """
        Test email validation on forget password error.
        """
        # email doesn't exist
        data = {'email': 'admin5@gmail.com'}
        form = EmailValidationOnForgotPassword(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('email', code='incorrect email'))
        # email exists
        data = {'email': 'test1@gmail.com'}
        form = EmailValidationOnForgotPassword(data=data)
        self.assertTrue(form.is_valid())
