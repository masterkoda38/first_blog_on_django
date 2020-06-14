# Мы объявили два шаблона, используя функцию path(). Первый шаблон не принимает
# никаких аргументов. Он сопоставляется с обработчиком post_list. Второй вызывает
# функцию post_detail и принимает в качестве параметров 4 элемента.

from django.urls import path
from . import views

# Мы определили пространство имен приложения в переменной app_name.
app_name = 'blog'

urlpatterns = [
    # закомментируйте шаблон для обработчика PostListView и раскомментируйте шаблон для post_list
    path('', views.post_list, name='post_list'),
    # Добавьте дополнительный URL-шаблон, чтобы была возможность обратиться к списку статей,
    # связанных с определенным тегом
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]