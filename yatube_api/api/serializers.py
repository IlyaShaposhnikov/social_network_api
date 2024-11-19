from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя."
            )
        if Follow.objects.filter(
            user=self.context['request'].user,
            following=value
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя."
            )
        return value
