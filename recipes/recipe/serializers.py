from rest_framework import serializers
from rest_framework.serializers import ImageField
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
        """Perform necessary eager loading of data"""
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
        many=True, queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = ImageField(allow_null=True, max_length=100, required=False, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'ingredients',
            'tags',
            'time_minutes',
            'price',
            'link',
            'image',
        )
        read_only_fields = ('id',)

    @classmethod
    def setup_eager_loading(cls, queryset):
        """Perform necessary eager loading of data"""
        queryset = queryset.prefetch_related('tags', 'ingredients')
        return queryset

    def validate_tags(self, tags):
        error_tags_id = [
            str(tag.id) for tag in tags if tag.user != self.context['request'].user
        ]
        if error_tags_id:
            error_tags_id_str = ','.join(error_tags_id)
            raise serializers.ValidationError(
                'Its not allowed to use tags with id: {}, which are created by other user.'.format(
                    error_tags_id_str
                )
            )
        return tags

    def validate_ingredients(self, ingredients):
        error_ingredients_id = [
            str(ingredient.id)
            for ingredient in ingredients
            if ingredient.user != self.context['request'].user
        ]

        if error_ingredients_id:
            error_ingredients_id_str = ','.join(error_ingredients_id)
            raise serializers.ValidationError(
                'Its not allowed to user ingredients with id: {}, which are created by other user'.format(
                    error_ingredients_id_str
                )
            )
        return ingredients


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe details"""

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes"""

    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
