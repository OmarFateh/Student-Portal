from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(email='admin@gmail.com', full_name='admin')

    def test_user_model_entry(self):
        """
        Test User model data insertion/types/field attributes.
        """
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(str(self.user), 'admin@gmail.com')
        self.assertEqual(self.user.get_full_name(), 'admin')
        self.assertEqual(self.user.get_short_name(), 'admin')

    def test_user_model_manager_entry(self):
        """
        Test User model manager data insertion/types/field attributes.
        """
        # test staffuser
        User.objects.create_staffuser(email='admin1@gmail.com', password='admin')
        self.assertEqual(User.objects.filter(is_staff=True).count(), 1)
        # test superuser
        User.objects.create_superuser(email='admin2@gmail.com', password='admin')
        self.assertEqual(User.objects.filter(is_superuser=True).count(), 1)
    
    def test_createuser_error(self):
        """
        Test value errors in createuser method.
        """    
        # password is empty
        with self.assertRaises(ValueError) as e:
            user1 = User.objects.create_user(email='admin3@gmail.com')
        self.assertEqual(str(e.exception), 'Users must have a password')
        # email is empty
        with self.assertRaises(ValueError) as e:
            user2 = User.objects.create_user(email='', password='admin')
        self.assertEqual(str(e.exception), 'Users must have an email address')
        # email is invalid
        with self.assertRaises(ValueError) as e:
            user2 = User.objects.create_user(email='ahmad', password='admin')
        self.assertEqual(str(e.exception), 'You must provide a valid email address.')

    def test_send_email(self):
        """
        Test send email method.
        """
        self.user.email_user(subject='subject test', message='message test')
        self.assertEqual(len(mail.outbox), 1)