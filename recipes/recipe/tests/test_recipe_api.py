import os
import tempfile

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from PIL import Image

from core.models import Recipe
from core.tests.utils import create_user
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
from recipe.tests.utils import (
    sample_recipe,
    sample_tag,
    sample_ingredient,
    detail_url,
    image_upload_url,
)

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

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        tag = sample_tag(user=self.user)
        ingredient = sample_ingredient(user=self.user)
        recipe = sample_recipe(user=self.user, tags=[tag], ingredients=[ingredient])

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe"""
        payload = {'title': 'Cheesecake', 'time_minutes': 30, 'price': 5.00}
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """Test creating recipe with tags"""
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Dessert')

        payload = {
            'title': 'Avocado lime cheesecake',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 20.00,
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()

        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_other_users_tags(self):
        """Test creating recipe with other's user tags"""
        user2 = create_user('other@dev.com', 'OtherPassword')
        tag1 = sample_tag(user=self.user, name='Beef')
        tag2 = sample_tag(user=user2, name='Mutton')

        payload = {
            'title': 'Meat stew',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 60,
            'price': 100,
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(str(tag2.id), res.content.decode())

    def test_create_recipe_with_other_user_ingredients(self):
        """Test creating recipe with other's user ingredients"""
        user2 = create_user('other@dev.com', 'OtherPassword')
        ingredient1 = sample_ingredient(user=self.user, name='Tomato')
        ingredient2 = sample_ingredient(user=user2, name='Potato')
        payload = {
            'title': 'Vegetable stew',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 60,
            'price': 100,
        }
        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(str(ingredient2.id), res.content.decode())

    def test_create_recipe_with_ingredients(self):
        """Test creating recipe with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Prawns')
        ingredient2 = sample_ingredient(user=self.user, name='Ginger')

        payload = {
            'title': 'Thai prawn red curry',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 20,
            'price': 7.00,
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()

        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user)

        payload = {'title': 'Title', 'tags': [new_tag.id]}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """Test updating a recipe with put"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        payload = {'title': 'Title', 'time_minutes': 25, 'price': 5.00}
        url = detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)


class RecipeImageUploadTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.email = 'test@dev.com'
        self.password = 'GreaterThanEight'
        self.user = create_user(email=self.email, password=self.password)
        self.client.force_authenticate(self.user)
        self.recipe = sample_recipe(user=self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image_to_recip(self):
        """Test uploading image to recipe"""
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
