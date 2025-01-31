from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator

from .models import Snippet, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_title']
        extra_kwargs = {'tag_title': {'validators': [UniqueValidator(queryset=Tag.objects.all())]}}  # Ensures title uniqueness


class SnippetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Snippet
        fields = ['id', 'snippet_title', 'note', 'tags', 'created_at', 'updated_at']
        extra_kwargs = {'created_by': {'read_only': True}}  # Exclude from input

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])

        # Get the logged-in user from context
        user = self.context['request'].user

        snippet = Snippet.objects.create(created_by=user, **validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(tag_title=tag_data['tag_title'])
            snippet.tags.add(tag)

        return snippet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create user and hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class SnippetOverViewSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        # Return the absolute URL for the snippet detail view
        return reverse('snippet-detail', kwargs={'pk': obj.pk}, request=request) if request else None


class SnippetViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'snippet_title', 'note', 'created_at', 'updated_at']


class TagListSerializer(serializers.ModelSerializer):
    snippets = SnippetSerializer(many=True)

    class Meta:
        model = Tag
        fields = ['id', 'tag_title', 'snippets']