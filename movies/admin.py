from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from . models import Category, Genre, Movie, MovieShots, Actor, RatingStar, Rating, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #какие поля показывать в админке
    list_display = ('id', 'name', 'url')
    #по каким полям можно перейти в объект
    list_display_links = ('id', 'name', 'url')

#Класс, который позволит выводить модель комментариев в модели Фильмов
class ReviewInLines(admin.TabularInline): #либо admin.StackedInline. Отличается видом
    model = Reviews
    #сколько пустых отзывов добавить
    extra = 1
    #определение полей, который нельзя редактировать
    readonly_fields = ('name', 'email', 'parent')

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="80">')

    get_image.short_description = 'Изображение'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm

    list_display = ('title', 'year', 'category', 'url', 'draft', 'get_image')
    #добавляет фильтр по категории и году
    list_filter = ('category', 'year')
    #доабвляет поиск по названию и категории
    search_fields = ('title', 'category__name')
    #вывод комментариев
    inlines = [MovieShotsInline, ReviewInLines]
    actions = ['publish', 'unpublish']
    #перенести кнопку сохранения наверх
    save_on_top = True
    #меняет кнопку "Сохранить и добавить новый объект" на "Сохранить как новый объект"
    # save_as = True
    #позволяет добавлять в черновик прям из списка не заходя в детальный просмотр
    list_editable = ('draft',)

    #вывод полей, которые мы ходим использовать 2 способа:
    #чтобы поместить поля в одну строку, нужно поместить кортеж внутрь кортежа
    # fields = (('actors', 'directors', 'genres'),)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': (('description', 'poster'),)
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors, directors, genres and category', {
            'classes': ('collapse',), #скрывает поля
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Опции', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60">')

    # функция публикации
    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записи обновлены'
        self.message_user(request, f'{message_bit}')

    #функция снятия с публикации
    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записи обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    #определение полей, который нельзя редактировать
    readonly_fields = ('name', 'email', 'parent')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="80">')
    get_image.short_description = 'Изображение'

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)
    #метод, который будет выводить изображение в админку
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')
    get_image.short_description = 'Изображение'

@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    pass

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass

#заголовок в админке
admin.site.site_title = 'Киносайт'
admin.site.site_header = 'Киносайт'
