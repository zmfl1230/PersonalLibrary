from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance, Language, Already_read


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


class BookInline(admin.TabularInline):
    model = Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('bookname', 'author', 'display_genre', 'wrote_language')

    inlines = [BooksInstanceInline]

    def display_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status')
    list_filter = ('status', 'due_back')

    fieldsets = (

        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Language)
admin.site.register(Already_read)
