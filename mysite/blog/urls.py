# Мы объявили два шаблона, используя функцию path(). Первый шаблон не принимает
# никаких аргументов. Он сопоставляется с обработчиком post_list. Второй вызывает
# функцию post_detail и принимает в качестве параметров 4 элемента.

from django.urls import path
from . import views

# Мы определили пространство имен приложения в переменной app_name.
app_name = 'blog'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),

    # Поскольку обработчик был заменен необходимо заменить взаимосвязь основного пути и обработчика во views
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
]