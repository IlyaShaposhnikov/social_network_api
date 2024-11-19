from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Слаг группы')
    description = models.TextField(verbose_name='Описание группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации поста'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор поста'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True,
        verbose_name='Изображение поста'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name='posts', blank=True,
        null=True, verbose_name='Группа поста'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:20] + '...' if len(self.text) > 20 else self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Пост комментария'
    )
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name='Дата добавления комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:20] + '...' if len(self.text) > 20 else self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
        verbose_name='Подписан на'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
