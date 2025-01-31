from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    tag_title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag_title


class Snippet(models.Model):
    snippet_title = models.CharField(max_length=255)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='snippets')

    def __str__(self):
        return self.snippet_title
