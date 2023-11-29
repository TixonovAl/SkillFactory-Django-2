from django.db import models
from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    rating = models.IntegerField(default=0)  # Рейтинг автора

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # Ключ к юзеру

    def update_rating(self):
        post_rating = Post.objects.filter(author_id=self.pk).\
            aggregate(sum_rating=Coalesce(Sum("rating")*3, 0))['sum_rating']

        comments_rating = Comment.objects.filter(user=self.user).\
            aggregate(sum_rating=Coalesce(Sum('rating'), 0))['sum_rating']

        comments_post_rating = Comment.objects.filter(post__author__user=self.user).\
            aggregate(sum_posts=Coalesce(Sum('rating'), 0))['sum_posts']

        self.rating = post_rating + comments_rating + comments_post_rating
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)  # Категории новостей/статей


class Post(models.Model):
    class TypePost(models.TextChoices):  # Определение типов постов, формат "Статья" или "Новость"
        article = "ART", _("Статья")
        news = "NWS", _("Новость")

    type_post = models.CharField(max_length=3,  # Тип поста
                                 choices=TypePost.choices,
                                 default=TypePost.news,
                                 )
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата и время создания поста
    title = models.CharField(max_length=255)  # Заголовок статьи/новости
    text = models.TextField()  # Текст статьи/новости
    rating = models.IntegerField(default=0)  # Рейтинг статьи/новости

    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь мн-к-од с моделью Author
    categories = models.ManyToManyField(Category, through="PostCategory")  # связь мн-к-мн с моделью Category

    def like(self, x=1):
        self.rating += x
        self.save()

    def dislike(self, x=1):
        self.rating -= x
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'


class PostCategory(models.Model):  # модель для связи мн-к-мн
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):  # Комментарии под статьёй/новостью
    comment = models.TextField()  # Текст комментария
    date_of_writing = models.DateTimeField(auto_now_add=True)  # Дата написания комментария
    rating = models.IntegerField(default=0)  # Рейтинг комментария

    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь мн-к-одн с моделью Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь мн-к-одн с моделью User

    def like(self, x=1):
        self.rating += x
        self.save()

    def dislike(self, x=1):
        self.rating -= x
        self.save()
