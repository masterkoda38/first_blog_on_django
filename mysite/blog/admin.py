# Настроим отображение сайта администрирования.
from django.contrib import admin
from .models import Post

# Атрибут list_display позволяет перечислить поля модели, которые мы хотим отображать на странице списка.
# Декоратор @admin.register() выполняет те же действия, что и функция admin.site.register: регистрирует
# декорируемый класс – наследник ModelAdmin.

# Добавляем модель на сайт администрирования:
# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # Справа на странице появится блок фильтрации списка, который фильтрует статьи по полям.
    list_filter = ('status', 'created', 'publish', 'author')
    # Строка поиска, она добавится для моделей, которые перечислены в виде аргументов.
    search_fields = ('title', 'body')
    # slug будет генерироваться автоматически из поля title с помощью данного атрибута.
    prepopulated_fields = {'slug': ('title',)}
    # теперь поле author содержит поле поиска, что значительно упрощает выбор автора из выпадающего списка,
    # когда в системе сотни пользователей
    raw_id_fields = ('author',)
    # Под поиском добавлены ссылки для навигации по датам.
    date_hierarchy = 'publish'
    # Сортировка списка статей по умолчанию по агрументам:
    ordering = ('status', 'publish')

