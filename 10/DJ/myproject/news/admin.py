# news/admin.py (с полем автора)
from django.contrib import admin
from .models import News_post


@admin.register(News_post)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'pub_date', 'created_at']
    list_filter = ['author', 'pub_date', 'created_at']
    search_fields = ['title', 'short_description', 'author__username']
    date_hierarchy = 'pub_date'
    ordering = ['-pub_date']

    # Делаем поля только для чтения
    readonly_fields = ['created_at', 'updated_at']

    # Автоматически заполняем автора текущим пользователем
    def save_model(self, request, obj, form, change):
        if not change:  # Только при создании новой записи
            obj.author = request.user
        super().save_model(request, obj, form, change)

    # Группировка полей в админке
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'short_description', 'text', 'author')
        }),
        ('Дата и время', {
            'fields': ('pub_date', 'created_at', 'updated_at')
        }),
    )