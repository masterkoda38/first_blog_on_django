"""Новый шаблон, добавленный с помощью include, подключит конфигурацию
приложения блога. Все его адреса будут начинаться с blog/. Мы будем об-
ращаться к шаблонам приложения по пространству имен, например blog:post_list, blog:post_detail.
"""
from django.urls import path, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

#мы подключили необходимые модули и определили словарь карт сайта.
# Добавили шаблон URL’а, который соответствует адресу sitemap.xml и обработчику sitemap.
sitemaps = {'posts': PostSitemap, }

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]
