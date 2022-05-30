from django.contrib import admin
from .models import Posts, UserReactions


@admin.register(Posts)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'slug', 'content', 'view_count',
        'date_create',
    )
    ordering = ('id',)
    list_display_links = ('id', 'title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(UserReactions)
class UserRatingsOfArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'reaction',)
    ordering = ('id',)
    list_display_links = ('id', 'post',)
    list_filter = ('post',)

