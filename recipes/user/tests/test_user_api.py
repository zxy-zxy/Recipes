from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTest(TestCase):
    """
    Test the users API (public)
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        """
        Test creating user with valid payload is successful
        """
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        name = 'test'
        payload = {'email': email, 'password': password, 'name': name}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Test creating a user that already exists fails
        """
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        name = 'test'
        payload = {'email': email, 'password': password, 'name': name}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        email = 'test@dev.com'
        password = 'test'
        name = 'test'
        payload = {'email': email, 'password': password, 'name': name}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=email).exists()
        self.assertFalse(user_exists)

    def test_create_token_successful(self):
        """
        Test that a token create for a user
        """
        payload = {'email': 'test@dev.com', 'password': 'GreaterThanEight'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        create_user(email=email, password=password)
        payload = {'email': email, 'password': 'wrong_password'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_user_not_exists(self):
        """Test that token is not created if passed user is not exists"""
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        payload = {'email': email, 'password': password}
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'test@mail.com'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.email = 'test@dev.com'
        self.password = 'GreaterThanEight'
        self.user = create_user(email=self.email, password=self.password, name='name')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name': self.user.name, 'email': self.user.email})

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
