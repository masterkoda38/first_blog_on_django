from django.contrib.sitemaps import Sitemap
from .models import Post


#Мы создали собственный объект карты сайта, унаследовав его от Sitemap модуля sitemaps.
class PostSitemap(Sitemap):
    #Атрибуты changefreq и priority показывают частоту обновления страниц статей
    # и степень их совпадения с тематикой сайта (максимальное значение – 1)
    changefreq = 'weekly'
    priority = 0.9

    # Метод items() возвращает QuerySet объектов, которые будут отображаться в карте сайта.
    def items(self):
        return Post.published.all()

    #Метод lastmod принимает каждый объект из результата вызова items()
    # и возвращает время последней модификации статьи.
    def lastmod(self, obj):
        return obj.updated
