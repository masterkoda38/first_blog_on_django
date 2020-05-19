from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post

# Django имеет встроенный класс для постраничного отображения - Paginator,, который позволит нам легко управлять им.
# Отредактируйте views.py, импортируйте классы-пагинаторы из Django и добавьте их в обработчик post_list:

def post_list(request):
    # В этой функции мы запрашиваем из базы данных все опубликованные статьи с помощью менеджера published.
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # По 3 статьи на каждой странице.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
        # Функция render() использует переданный контекст {'page': page, 'posts': posts} при формировании
        #  шаблона 'blog/post/list.html', поэтому любая переменная контекста будет доступна в этом шаблоне.
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


# Это обработчик страницы статьи. Он принимает на вход аргументы year, month, day и post
# для получения статьи по указанным слагу и дате.
def post_detail(request, year, month, day, post):
    # Функция get_object_or_404 возвращает объект, который подходит по указанным параметрам
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    # Функцию render() используем для формирования HTML - шаблона. При этом передаём саму статью в виде словаря,
    # значения полей этого словаря будут доступны в шаблонах html по названию словаря post, например, чтобы получить
    # имя автора в шаблоне 'blog/post/detail.html' используем post.author.
    return render(request, 'blog/post/detail.html', {'post': post})


# Мы заменим наш post_list на класс-наследник ListView Django. Этот базовый
# класс обработчика списков позволяет отображать несколько объектов любого
# типа
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'