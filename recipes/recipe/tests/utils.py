from core.models import Recipe


def sample_recipe(user, **kwargs):
    """Create and return sample recipe"""
    defaults = {'title': 'Sample recipe', 'time_minutes': 10, 'price': 5.00}

    defaults.update(kwargs)

    return Recipe.objects.create(user=user, **defaults)
