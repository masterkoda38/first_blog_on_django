from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
# Чтобы зарегистрировать наши теги, каждый модуль с функциями тегов должен определять переменную register.
register = template.Library()


# Начнем с реализации простого тега, который будет выводить количество опубликованных статей
@register.simple_tag
def total_posts():
    return Post.published.count()


# Cоздадим тег для добавления последних статей блога на боковую панель. На этот раз мы будем использовать
# инклюзивный тег, с помощью которого сможем задействовать переменные контекста, возвращаемые тегом,
# для формирования шаблона
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Мы формируем QuerySet, используя метод annotate() для добавления к каждой статье количества ее комментариев.
# Метод Count используется в качестве функции агрегации, которая вычисляет количество комментариев total_comments
# для каждого объекта Post. Также мы сортируем QuerySet поэтому полю в порядке убывания. Как и в предыдущем
# примере, тег принима-ет дополнительный аргумент count, чтобы ограничить количество выводимых статей.
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')
                                   ).order_by('-total_comments')[:count]


# Мы зарегистрировали фильтр так же, как регистрировали теги. при регистрации фильтра указали ее имя,
# которое будет использоваться в шаблонах: {{ variable|markdown }}. Мы используем функцию mark_safe,
# чтобы пометить результат работы фильтра как HTML-код, который нужно учитывать при построении шаблона/
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
