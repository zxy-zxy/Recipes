from django.test import TestCase, Client
from django.urls import reverse

from .utils import create_superuser, create_user


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = create_superuser('admin@dev.com', 'GreaterThanEight')
        self.client.force_login(self.admin_user)
        self.user = create_user('test@dev.com', 'GreaterThanEight')

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_changed(self):
        """Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
