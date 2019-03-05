from django.test import TestCase
from django.contrib.auth import get_user_model

from core.tests.utils import create_user

UserModel = get_user_model()


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        user = create_user(email, password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@DEV.com'
        password = 'GreaterThanEight'
        user = create_user(email, password)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            password = 'GreaterThanEight'
            create_user(None, password)

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        user = UserModel.objects.create_superuser(
            email,
            password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)