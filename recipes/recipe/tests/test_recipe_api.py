from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from core.tests.utils import create_user
from recipe.serializers import RecipeSerializer

from recipe.tests.utils import sample_recipe

RECIPES_URL = reverse('recipe:recipe-list')


class PublicRecipeApiTest(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.email = 'test@dev.com'
        self.password = 'GreaterThanEight'
        self.user = create_user(email=self.email, password=self.password)
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes_list(self):
        """Test retrieving recipes"""
        sample_recipe(self.user)
        sample_recipe(self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_are_limited_to_user(self):
        recipe_by_user = sample_recipe(self.user, title='Meat on skewer.')

        user2 = create_user('other@dev.com', 'OtherPassword')
        recipe_by_user_2 = sample_recipe(user2)

        recipes = Recipe.objects.filter(user=self.user)

        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], recipe_by_user.title)
        self.assertEqual(res.data, serializer.data)
