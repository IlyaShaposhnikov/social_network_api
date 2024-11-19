from django.contrib import admin
from .models import Group, Post, Comment, Follow


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'author', 'group')
    list_filter = ('pub_date', 'author', 'group')
    search_fields = ('text', 'author__username', 'group__title')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created')
    list_filter = ('created', 'author', 'post')
    search_fields = ('text', 'author__username', 'post__text')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user__username', 'following__username')


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
