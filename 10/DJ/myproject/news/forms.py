# news/forms.py
from .models import News_post
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

class NewsPostForm(ModelForm):
    class Meta:
        model = News_post
        fields = ['title', 'short_description', 'text', 'pub_date']  # автор будет устанавливаться автоматически
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок новости'
            }),
            'short_description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание новости'
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Содержание новости',
                'rows': 5
            }),
            'pub_date': DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            })
        }
        labels = {
            'title': 'Заголовок новости',
            'short_description': 'Краткое описание',
            'text': 'Полный текст новости',
            'pub_date': 'Дата и время публикации'
        }