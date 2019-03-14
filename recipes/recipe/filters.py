from django_filters import rest_framework as filters

from core.models import Tag, Ingredient, Recipe


class BaseRecipeFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    assigned_to = filters.BooleanFilter(method='is_assigned', label='is assigned')

    def is_assigned(self, queryset, name, value):
        return queryset.filter(recipe__isnull=not value).distinct()


class TagFilter(BaseRecipeFilter):
    class Meta:
        model = Tag
        fields = ('name',)


class IngredientFilter(BaseRecipeFilter):
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
