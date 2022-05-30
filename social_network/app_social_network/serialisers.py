from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from app_social_network.models import Posts

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор, используемый при регистрации пользователей."""
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def validate_password(self, value: str) -> str:
        """Хеширование пароля."""
        return make_password(value)


class PostsSerializer(serializers.ModelSerializer):
    """Сериализатор, используемый при отображении постов."""
    url = serializers.HyperlinkedIdentityField(
        view_name='posts-detail', lookup_field='slug')

    class Meta:
        model = Posts
        fields = (
            'title', 'date_create', 'view_count', 'url',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор, используемый при отображении детальной информации о новости.
    """
    vote = serializers.HyperlinkedIdentityField(
        view_name='posts-vote', lookup_field='slug')
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Posts
        fields = '__all__'


class PostAddSerializer(serializers.ModelSerializer):
    """Сериализатор, используемый при добавлении новости."""
    class Meta:
        model = Posts
        fields = (
            'title', 'content',
        )

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super(PostAddSerializer, self).create(validated_data)
