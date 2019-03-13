from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.tests.utils import create_user, create_superuser
from core import models

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
        user = create_superuser(email, password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the string representation"""
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        user = create_user(email, password)
        tag = models.Tag.objects.create(user=user, name='Vegan')
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        user = create_user(email, password)
        ingredient = models.Ingredient.objects.create(name='Cucumber', user=user)

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        email = 'test@dev.com'
        password = 'GreaterThanEight'
        user = create_user(email, password)
        recipe = models.Recipe.objects.create(
            title='Meat on skewer', user=user, time_minutes=5, price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'my_image.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
