# Каждый атрибут представляет собой поле в базе данных. Django создает таблицу в базе данных для каждой
# модели, определенной в models.py.

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Собственный менеджер для получения всех опубликованных статей.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # slug – это поле будет использоваться для формирования URL’ов.
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # author – это поле является внешним ключом и определяет отношение «один ко многим».
    # Мы также указали имя обратной связи от User к Post– параметр related_name. Так мы с легкостью
    # получим доступ к связанным объектам автора.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # поле отображает статус статьи. Мы использовали параметр CHOICES, для того чтобы ограничить
    # возможные значения из указанного выше списка STATUS_CHOICES.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # Менеджер по умолчанию, Он возвращает все объекты из базы.
    published = PublishedManager() # Наш новый менеджер.

    # В Django метод модели get_absolute_url() должен возвращать канонический URL объекта.
    # Для реализации этого поведения мы будем использовать функцию reverse(),
    # которая дает возможность получать URL, указав имя шаблона и параметры.
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


    # Класс Meta внутри модели содержит метаданные. Мы указали Django порядок сортировки статей по умолчанию
    #  – по убыванию даты публикации О том, что порядок убывающий, говорит префикс «-».
    class Meta:
        ordering = ('-publish',)

    # Метод _возвращает отображение объекта, понятное человеку.
    # Django использует его во многих случаях, например на сайте администрирования.
    def __str__(self):
        return self.title
