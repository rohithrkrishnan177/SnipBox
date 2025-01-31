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
    tag = TagSerializer()

    class Meta:
        model = Snippet
        fields = ['id', 'snippet_title', 'note', 'created_at', 'updated_at', 'user', 'tag']

    def create(self, validated_data):
        # Extract the tag data
        tag_data = validated_data.pop('tag', None)

        # Ensure that the tag exists or is created
        if tag_data:
            tag, created = Tag.objects.get_or_create(tag_title=tag_data['title'])
            validated_data['tag'] = tag

        # Create the snippet and return it
        return Snippet.objects.create(**validated_data)



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
