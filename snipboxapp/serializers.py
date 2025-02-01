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
    tags = serializers.ListField(child=serializers.CharField(), write_only=True)
    tag_details = TagSerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = Snippet
        fields = ['id', 'snippet_title', 'note', 'tags', 'tag_details', 'created_at', 'updated_at']
        extra_kwargs = {'created_by': {'read_only': True}}  # Prevent input

    def create(self, validated_data):
        tag_titles = validated_data.pop('tags', [])  # Extract tag titles

        user = self.context['request'].user  # Get logged-in user

        snippet = Snippet.objects.create(created_by=user, **validated_data)  # Create snippet

        for title in tag_titles:
            tag, created = Tag.objects.get_or_create(tag_title=title)  # Get or create tag
            snippet.tags.add(tag)  # Link tag to snippet

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