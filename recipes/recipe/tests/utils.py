from django.urls import reverse
from core.models import Tag, Ingredient, Recipe


def detail_url(recipe_id):
    """Return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def image_upload_url(recipe_id):
    """Return url for recipe image upload"""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


def sample_recipe(user, **kwargs):
    """Create and return sample recipe"""
    defaults = {'title': 'Sample recipe', 'time_minutes': 10, 'price': 5.00}
    tags = kwargs.pop('tags') if 'tags' in kwargs else None
    ingredients = kwargs.pop('ingredients') if 'ingredients' in kwargs else None
    defaults.update(kwargs)
    recipe = Recipe.objects.create(user=user, **defaults)
    if tags:
        for tag in tags:
            recipe.tags.add(tag)
    if ingredients:
        for ingredient in ingredients:
            recipe.ingredients.add(ingredient)
    recipe.save()
    return recipe


def sample_tag(user, name='Sample tag'):
    """Create and return sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Sample ingredient'):
    """Create and return sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)
