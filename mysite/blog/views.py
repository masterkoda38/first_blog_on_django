from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag
from django.db.models import Count
# Это функция агрегации Count из Django. Она позволяет выполнять агрегирующий запрос
#  для подсчета количества тегов на уровне базы данных.


# Django имеет встроенный класс для постраничного отображения - Paginator,, который позволит нам легко управлять им.
# Отредактируйте views.py, импортируйте классы-пагинаторы из Django и добавьте их в обработчик post_list:

# Принимаем необязательный аргумент tag_slug, который по умолчанию равен None.
# Этот параметр будет задаваться в URL’е.
def post_list(request, tag_slug=None):
    # В этой функции мы запрашиваем из базы данных все опубликованные статьи с помощью менеджера published.
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        # находим все опубликованные статьи и, если указан слаг тега,
        #  получаем соответствующий объект модели Tag
        tag = get_object_or_404(Tag, slug=tag_slug)
        # фильтруем изначальный список статей и оставляем только те, которые связаны с полученным тегом.
        object_list = object_list.filter(tags__in=[tag])

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
        # шаблона 'blog/post/list.html', поэтому любая переменная контекста будет доступна в этом шаблоне.
        # Отредактируйте вызов функции render() в конце обработчика и передайте дополнительную переменную контекста.
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


# Это обработчик страницы статьи. Он принимает на вход аргументы year, month, day и post
# для получения статьи по указанным слагу и дате.
def post_detail(request, year, month, day, post):
    # Функция get_object_or_404 возвращает объект, который подходит по указанным параметрам
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    # Список активных комментариев к этой записи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Комментарий был опубликован
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создайте объект Comment, но пока не сохраняйте в базу данных
            new_comment = comment_form.save(commit=False)
            # Назначить текущий пост комментарию
            new_comment.post = post
            # Сохранить комментарий в базе данных
            new_comment.save()
    else:
        comment_form = CommentForm()
    # Формирование списка похожих статей
    # Получает все ID тегов текущей статьи. Метод QuerySet’а values_list() возвращает кортежи со значениями
    # заданного поля. Мы указали flat=True, чтобы получить список вида [1, 2, 3, ...];
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Получает все статьи, содержащие хоть один тег из полученных ранее, исключая текущую статью;
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Функция агрегации Count формирует поле same_tags, которое содержит количество совпадающих тегов;
    # Сортируем список опубликованных статей в убывающем порядке по количеству совпадающих тегов для отображения
    # первыми максимально похожих статей и делает срез результата для отображения только четырех статей
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    # Функцию render() используем для формирования HTML - шаблона. При этом передаём саму статью в виде словаря,
    # значения полей этого словаря будут доступны в шаблонах html по названию словаря post, например, чтобы получить
    # имя автора в шаблоне 'blog/post/detail.html' используем post.author.
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment,
        'similar_posts': similar_posts
    })


# Мы заменим наш post_list на класс-наследник ListView Django. Этот базовый
# класс обработчика списков позволяет отображать несколько объектов любого
# типа
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# определяем функцию post_share, которая принимает объект запроса request и параметр post_id
def post_share(request, post_id):
    # Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # ... Отправка электронной почты.
# Нам нужно добавить в сообщение абсолютную ссылку на статью, мы используем метод объекта запроса
#  request.build_absolute_uri() и передаем в него результат выполнения get_absolute_url() статьи.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "' \
                      '{} "'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:' \
                      '{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
