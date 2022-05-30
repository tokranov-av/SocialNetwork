from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify
from rest_framework.reverse import reverse

User = get_user_model()


class Posts(models.Model):
    title = models.CharField(
        max_length=55, verbose_name='Заголовок', unique=True
    )
    content = models.TextField(verbose_name='Содержание')
    slug = models.SlugField(max_length=55, unique=True, verbose_name='Слаг')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор поста')
    view_count = models.PositiveIntegerField(
        verbose_name='Количество просмотров', default=0)
    date_create = models.DateField(
        auto_now_add=True, verbose_name='Дата добавления')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Posts, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['id']


class UserReactions(models.Model):
    VALUE_REACTION = (
        ('-1', 'Не нравится'),
        ('0', 'Нейтрально'),
        ('1', 'Нравится'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name='user_ratings',
        verbose_name='Пост'
    )
    reaction = models.CharField(
        max_length=20, choices=VALUE_REACTION, default='0',
        verbose_name='Реакция'
    )

    class Meta:
        verbose_name = 'Пользовательские оценки'
        verbose_name_plural = 'Пользовательские оценки'
        ordering = ['id']
