from django_filters import rest_framework as filters

from core.models import Tag, Ingredient, Recipe


class TagFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ('name',)


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'ingredients')
