from django.test import TestCase, Client, RequestFactory
from django.core import mail
from django.urls import reverse
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import get_user_model

from accounts.views import validate_email

User = get_user_model()


class TestUserViewResponses(TestCase):
    
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='admin@gmail.com', password='admin1600', is_active=True)

    def test_user_register_func(self):
        """
        Test user register response status.
        """
        # Get data
        response = self.c.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        # Post data
        data = {
            'full_name': 'test',
            'email': 'test@gmail.com',
            'email2': 'test@gmail.com',
            'password1': 'admin160',
            'password2': 'admin160',
        }
        response = self.c.post(reverse("accounts:register"), data=data)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response, reverse("accounts:login"), status_code=302)

    def test_user_login_func(self):
        """
        Test user login response status.
        """
        # Get data
        response = self.c.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        # login success
        data = {'email': 'admin@gmail.com', 'password': 'admin1600'}
        response = self.c.post(reverse("accounts:login"), data=data)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('classroom:categories'), status_code=302)
        # user is inactive and send activation mail
        self.c.logout()
        self.user.is_active = False
        self.user.save()
        response = self.c.post(reverse("accounts:login"), data=data)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertEqual(len(mail.outbox), 1)
        # email or password is incorrect
        data = {'email': 'admin@gmail.com', 'password': 'admin160'}
        response = self.c.post(reverse("accounts:login"), data=data)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        # email or password is not given
        data = {'email': '', 'password': 'admin1600'}
        response = self.c.post(reverse("accounts:login"), data=data)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_logout_func(self):
        """
        Test user logout response status.
        """
        # login user 
        self.c.force_login(self.user)
        # logout user
        response = self.c.get(reverse("accounts:logout"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse("accounts:login"), status_code=302)

    def test_validate_email_func(self):
        """
        Test validate email response status.
        """
        # registering new user
        data = {'email': 'admin@gmail.com'}
        response = self.c.get(reverse("accounts:js-validate-email"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'is_email_taken': True, 'error_message': 'An account with this Email already exists.'})
        # editing user's profile.
        request = self.factory.get(reverse("accounts:js-validate-email"), data=data)
        request.user = self.user
        response = validate_email(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'is_email_taken': False})
        