from django.contrib import admin
from .models import Snippet, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_title',)
    search_fields = ('tag_title',)


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('snippet_title', 'created_by', 'created_at', 'updated_at')
    search_fields = ('snippet_title', 'note', 'created_by__username')
    list_filter = ('created_by', 'tags', 'created_at')
    raw_id_fields = ('created_by',)

