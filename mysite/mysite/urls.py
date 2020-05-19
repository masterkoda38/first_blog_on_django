"""Новый шаблон, добавленный с помощью include, подключит конфигурацию
приложения блога. Все его адреса будут начинаться с blog/. Мы будем об-
ращаться к шаблонам приложения по пространству имен, например blog:post_list, blog:post_detail.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
]
