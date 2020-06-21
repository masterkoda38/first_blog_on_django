from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


# Мы унаследовали наш класс от Feed – класса подсистемы фидов Django. Атрибуты title, link и description
#  будут представлены в RSS элементами <title>, <link> и <description> соответственно.
class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    # Метод items() получает объекты, которые будут включены в рассылку. Мы берем только последние 5 статей.
    def items(self):
        return Post.published.all()[:5]

    # Методы item_title() и item_description() получают для каждого объекта из  items() заголовок и описание.
    def item_title(self, item):
        return item.title

    # Также мы используем встроенный шаблонный фильтр truncatewords, чтобы ограничить описание статей 30 словами/
    def item_description(self, item):
        return truncatewords(item.body, 30)
