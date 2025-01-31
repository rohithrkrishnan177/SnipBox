from django.contrib.auth.models import User
from rest_framework import serializers
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
        fields = ['id', 'snippet_title', 'note', 'tags', 'created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        # Extract tag data from validated_data
        tags_data = validated_data.pop('tags', [])

        # Create the snippet first
        snippet = Snippet.objects.create(**validated_data)

        # Loop through the tags and either create them or link existing ones
        for tag_data in tags_data:
            # Ensure the tag title is unique or use the existing tag
            tag, created = Tag.objects.get_or_create(tag_title=tag_data['title'])
            snippet.tags.add(tag)  # Add the tag to the snippet

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
