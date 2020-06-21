#Это наша первая Django-форма.
from django import forms
from .models import Comment



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
# Валидация поля также зависит от его типа. Например, поля email и to имеют
# тип EmailField. Оба могут получать только корректные e-mail-адреса
    email = forms.EmailField()
    to = forms.EmailField()
# Каждый тип по умолчанию имеет виджет для отображения
# в HTML. Виджет может быть изменен с помощью параметра widget.
    comments = forms.CharField(required=False, widget=forms.Textarea)


# Все, что нужно для создания формы из модели, – указать, какую модель использовать в опциях класса Meta.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# Пользователи будут использовать поле формы query для задания поискового запроса.
class SearchForm(forms.Form):
    query = forms.CharField()
