from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'user')
        read_only_fields = ('id',)

    @classmethod
    def setup_eager_loading(cls, queryset):
        """Perform neccessary eager loading of data"""
        queryset = queryset.select_related('user')
        return queryset


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes', 'price', 'link',)
        read_only_fields = ('id',)
